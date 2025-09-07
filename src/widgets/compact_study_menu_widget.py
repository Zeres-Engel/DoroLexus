"""
Compact Study Mode Menu Widget - smaller menu for deck gallery page
"""

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                               QPushButton, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QColor
from src.core.paths import asset_path


class CompactStudyModeButton(QPushButton):
    """Compact button for study modes"""
    
    def __init__(self, mode_type: str, title: str, icon: str = None, parent=None):
        super().__init__(parent)
        self.mode_type = mode_type
        self.title = title
        self.icon = icon
        self.is_active = False
        # Accent color matching the tomato theme
        self.accent = QColor(255, 99, 71)
        self._init_ui()
        # Outer shadow removed (keep only inner lighting via gradients)
        self._shadow = None
        # Low jump animation on hold
        self._jump_animation = QPropertyAnimation(self, b"geometry")
        self._jump_animation.setDuration(120)
        self._jump_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def _init_ui(self):
        self.setText(self.title)
        self.setFixedHeight(40)
        self.setMinimumWidth(120)
        
        # Icon setup if provided
        if self.icon and self.icon != "🔄":  # Skip if just emoji
            icon_path = asset_path("data", "images", "svg", f"{self.icon}-svgrepo-com.svg")
            if icon_path:
                from PySide6.QtGui import QIcon
                self.setIcon(QIcon(icon_path))
                self.setIconSize(self.size() * 0.4)  # Scale icon to 40% of button size
        
        self._apply_neumorphic_style()

    def _apply_neumorphic_style(self):
        """Apply simple flat style (no inner shadow/lighting)."""
        self.setStyleSheet("""
            QPushButton {
                background: rgba(40, 40, 50, 0.9);
                color: #ff6b6b;
                border: 2px solid rgba(255, 107, 107, 0.4);
                border-radius: 12px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 800;
                letter-spacing: 0.4px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                text-align: center;
            }
            QPushButton:hover {
                background: rgba(60, 60, 70, 0.95);
                border: 2px solid rgba(255, 107, 107, 0.8);
                color: #ffffff;
            }
            QPushButton:pressed {
                background: rgba(20, 20, 30, 0.95);
                border: 2px solid rgba(255, 150, 150, 0.9);
                color: #ffdddd;
            }
            QPushButton:disabled {
                background: rgba(50, 50, 50, 0.5);
                color: rgba(255, 255, 255, 0.3);
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
        """)

    def set_active(self, active: bool):
        """Apply active visual style to mimic selected deck glow (tomato fill)."""
        self.is_active = active
        if active:
            self.setStyleSheet(
                f"""
                QPushButton {{
                    background: rgba({self.accent.red()}, {self.accent.green()}, {self.accent.blue()}, 0.9);
                    color: #ffffff;
                    border: 2px solid rgba(255, 150, 150, 0.8);
                    border-radius: 12px;
                    padding: 10px 18px;
                    font-size: 13px;
                    font-weight: 900;
                    letter-spacing: 0.5px;
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                }}
                QPushButton:hover {{
                    background: rgba({self.accent.red()}, {self.accent.green()}, {self.accent.blue()}, 1.0);
                    border: 2px solid rgba(255, 200, 200, 1.0);
                }}
                """
            )
            # No outer shadow
        else:
            self._apply_neumorphic_style()
            # No outer shadow

    def enterEvent(self, event):
        """Glow on hover to echo deck card hover effect."""
        # No outer shadow on hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        # No outer shadow on leave
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Low jump animation on press"""
        if event.button() == Qt.LeftButton:
            self._jump_down()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Return to normal position on release"""
        if event.button() == Qt.LeftButton:
            self._jump_up()
        super().mouseReleaseEvent(event)

    def _jump_down(self):
        """Animate button down slightly when pressed"""
        current_rect = self.geometry()
        jump_rect = QRect(current_rect.x(), current_rect.y() + 2, current_rect.width(), current_rect.height())
        self._jump_animation.stop()
        self._jump_animation.setStartValue(current_rect)
        self._jump_animation.setEndValue(jump_rect)
        self._jump_animation.start()

    def _jump_up(self):
        """Return button to normal position"""
        current_rect = self.geometry()
        normal_rect = QRect(current_rect.x(), current_rect.y() - 2, current_rect.width(), current_rect.height())
        self._jump_animation.stop()
        self._jump_animation.setStartValue(current_rect)
        self._jump_animation.setEndValue(normal_rect)
        self._jump_animation.start()


class CompactStudyMenuWidget(QWidget):
    """
    Compact study mode selection menu for deck gallery page.
    Shows/hides when decks are selected.
    """
    
    mode_selected = Signal(str)  # Emits mode type when selected
    start_requested = Signal(str, list)  # mode_type, deck_ids
    cancel_requested = Signal()  # user cancelled selection
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_decks = []
        self.selected_mode = None
        self._init_ui()
        self.hide()  # Initially hidden
        
    def _init_ui(self):
        self.setStyleSheet("""
            CompactStudyMenuWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(20, 20, 26, 0.98),
                    stop:1 rgba(10, 10, 16, 0.98));
                border: 2px solid rgba(255, 107, 107, 0.6);
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("⚔️ Choose Your Battle Mode")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #ff6b6b;
                font-size: 16px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                background: transparent;
            }
        """)
        header_layout.addWidget(self.title_label)
        
        # Deck count info
        self.deck_info_label = QLabel("")
        self.deck_info_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 11px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                background: transparent;
            }
        """)
        header_layout.addWidget(self.deck_info_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Study mode buttons in horizontal layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        study_modes = [
            {"type": "flip", "title": "⚔️ Battle Cards", "icon": None},
            {"type": "multiple_choice", "title": "🎯 Arena Choice", "icon": None},
            {"type": "spelling", "title": "🖋️ Rune Spelling", "icon": None},
            {"type": "shuffle", "title": "🌪️ Chaos Mode", "icon": None}
        ]
        
        self.mode_buttons = {}
        for mode in study_modes:
            button = CompactStudyModeButton(
                mode["type"], 
                mode["title"], 
                mode["icon"]
            )
            button.clicked.connect(lambda checked, m=mode["type"]: self._on_mode_clicked(m))
            self.mode_buttons[mode["type"]] = button
            buttons_layout.addWidget(button)
        
        layout.addLayout(buttons_layout)
        
        # Action bar with Customize and Start buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        actions_layout.addStretch()

        self.cancel_btn = QPushButton("✖ Cancel")
        self.cancel_btn.setFixedHeight(36)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(210, 60, 76, 0.95),
                    stop:1 rgba(180, 30, 40, 0.95));
                color: #ffffff;
                border: 2px solid rgba(255, 120, 140, 0.85);
                border-radius: 10px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 0.3px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                border-color: rgba(255, 160, 170, 0.95);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(170, 30, 40, 0.95),
                    stop:1 rgba(140, 20, 28, 0.95));
            }
        """)
        self.cancel_btn.clicked.connect(self._emit_cancel)
        actions_layout.addWidget(self.cancel_btn)

        self.start_btn = QPushButton("▶ Start")
        self.start_btn.setFixedHeight(40)
        self.start_btn.setMinimumWidth(110)
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 230, 100, 0.98),
                    stop:1 rgba(255, 205, 60, 0.98));
                color: #2b2b2b;
                border: 2px solid rgba(255, 240, 160, 0.95);
                border-radius: 12px;
                padding: 6px 16px;
                font-size: 14px;
                font-weight: 800;
                letter-spacing: 0.5px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover { 
                border-color: rgba(255, 250, 180, 1.0);
            }
            QPushButton:disabled {
                background: rgba(120, 120, 120, 0.35);
                color: rgba(255,255,255,0.4);
                border: 2px solid rgba(255,255,255,0.2);
            }
        """)
        self.start_btn.clicked.connect(self._emit_start)
        actions_layout.addWidget(self.start_btn)

        layout.addLayout(actions_layout)

        # Make compact - fixed height
        self.setFixedHeight(130)
        
    def set_selected_decks(self, deck_ids: list, deck_names: list = None):
        """Update the selected decks and show/hide menu accordingly"""
        self.selected_decks = deck_ids
        
        if len(deck_ids) == 0:
            self.hide()
        else:
            self.show()
            
            # Update deck info
            if len(deck_ids) == 1:
                if deck_names and len(deck_names) > 0:
                    info_text = f"Study: {deck_names[0]}"
                else:
                    info_text = "1 deck selected"
            else:
                info_text = f"{len(deck_ids)} decks selected"
            
            self.deck_info_label.setText(info_text)
            
            # Enable/disable buttons based on selection
            self._update_button_states()
            self._update_action_states()
    
    def _update_button_states(self):
        """Enable/disable buttons based on deck selection"""
        has_selection = len(self.selected_decks) > 0
        
        for button in self.mode_buttons.values():
            button.setEnabled(has_selection)

    def _update_action_states(self):
        """Enable Start/Customize when both a mode and at least one deck are selected"""
        has_selection = len(self.selected_decks) > 0
        has_mode = self.selected_mode is not None
        enable = has_selection and has_mode
        self.start_btn.setEnabled(enable)
        self.cancel_btn.setEnabled(has_selection)

    def _on_mode_clicked(self, mode_type: str):
        """Toggle the selected mode with visual feedback and emit selection"""
        if self.selected_mode == mode_type:
            # Deselect if clicking again
            self.selected_mode = None
        else:
            self.selected_mode = mode_type
        # Update visuals
        for m, btn in self.mode_buttons.items():
            btn.set_active(m == self.selected_mode)
        # Keep external listeners informed about mode changes
        if self.selected_mode:
            self.mode_selected.emit(self.selected_mode)
        self._update_action_states()

    def _emit_start(self):
        """Emit start with current mode and selected decks"""
        if self.selected_mode and self.selected_decks:
            self.start_requested.emit(self.selected_mode, self.selected_decks.copy())
    
    def _emit_cancel(self):
        """Emit cancel to allow parent to clear selection and hide"""
        self.cancel_requested.emit()

        
    
    def get_selected_decks(self):
        """Return list of selected deck IDs"""
        return self.selected_decks.copy()
