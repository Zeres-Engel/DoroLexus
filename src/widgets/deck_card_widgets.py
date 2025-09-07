"""
Deck Card Widgets - Individual card components for different gallery modes
"""

from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from PySide6.QtGui import QIcon, QPixmap
from src.core.paths import asset_path


class BaseDeckCardWidget(QFrame):
    """Base class for all deck card widgets"""
    
    def __init__(self, deck_data=None, parent=None):
        super().__init__(parent)
        if deck_data:
            self.deck_id = deck_data['id']
            self.deck_name = deck_data['name']
            self.card_count = deck_data.get('card_count', 0)
            self.description = deck_data.get('description', '')
            self.due_count = deck_data.get('due_count', 0)
        
        self.setFixedSize(200, 120)
        self.setCursor(Qt.PointingHandCursor)
        
        # Animation support
        self._original_pos = None
        self._jump_animation = None
        self._is_hovered = False
        
        self.init_ui()
        
    def init_ui(self):
        """Override in subclasses"""
        pass
        
    def _create_jump_animation(self):
        """Create the jump animation for hover effect"""
        self._jump_animation = QPropertyAnimation(self, b"pos")
        self._jump_animation.setDuration(150)
        self._jump_animation.setEasingCurve(QEasingCurve.OutCubic)
        self._jump_animation.finished.connect(self._on_jump_finished)
        
    def _start_jump_animation(self):
        """Start the jump animation"""
        if self._jump_animation and self._jump_animation.state() == QPropertyAnimation.Running:
            return
        if self._original_pos is None:
            self._original_pos = self.pos()
        
        jump_pos = QPoint(self._original_pos.x(), self._original_pos.y() - 8)
        self._jump_animation.setStartValue(self._original_pos)
        self._jump_animation.setEndValue(jump_pos)
        self._jump_animation.start()
        
    def _on_jump_finished(self):
        """Handle jump animation finished - return to original position"""
        if self._jump_animation:
            return_animation = QPropertyAnimation(self, b"pos")
            return_animation.setDuration(100)
            return_animation.setEasingCurve(QEasingCurve.InCubic)
            return_animation.setStartValue(self.pos())
            return_animation.setEndValue(self._original_pos)
            return_animation.start()
            
    def enterEvent(self, event):
        """Handle mouse enter event"""
        if not self._is_hovered:
            self._is_hovered = True
            self._on_hover_enter()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Handle mouse leave event"""
        if self._is_hovered:
            self._is_hovered = False
            self._on_hover_leave()
            if self._original_pos is not None:
                self.move(self._original_pos)
        super().leaveEvent(event)
        
    def _on_hover_enter(self):
        """Override in subclasses for hover enter behavior"""
        pass
        
    def _on_hover_leave(self):
        """Override in subclasses for hover leave behavior"""
        pass
        
    def move(self, pos):
        """Override move to update original position"""
        super().move(pos)
        if not (self._jump_animation and self._jump_animation.state() == QPropertyAnimation.Running):
            self._original_pos = pos
            
    def reset_position(self):
        """Reset the widget to its original position and stop any animations"""
        if self._jump_animation and self._jump_animation.state() == QPropertyAnimation.Running:
            self._jump_animation.stop()
        if self._original_pos is not None:
            self.move(self._original_pos)
        else:
            self._original_pos = self.pos()


class CreateDeckCardWidget(BaseDeckCardWidget):
    """Special card widget for creating new decks"""
    
    create_deck = Signal()
    
    def __init__(self, parent=None):
        super().__init__(None, parent)
        
    def init_ui(self):
        """Initialize the create deck card UI with hover effects"""
        self._create_jump_animation()
        self.setStyleSheet("""
            CreateDeckCardWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 200, 100, 0.3),
                    stop:1 rgba(60, 160, 60, 0.3));
                border: 2px dashed rgba(100, 200, 100, 0.6);
                border-radius: 12px;
            }
            CreateDeckCardWidget:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(120, 220, 120, 0.4),
                    stop:1 rgba(80, 180, 80, 0.4));
                border: 2px dashed rgba(120, 220, 120, 0.8);
            }
        """)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Plus icon
        plus_label = QLabel("+")
        plus_label.setAlignment(Qt.AlignCenter)
        plus_label.setStyleSheet("""
            QLabel {
                color: rgba(100, 200, 100, 0.8);
                font-size: 36px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(plus_label)
        
        # Create text
        create_label = QLabel("New Deck")
        create_label.setAlignment(Qt.AlignCenter)
        create_label.setStyleSheet("""
            QLabel {
                color: rgba(100, 200, 100, 0.9);
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(create_label)
        
    def _on_hover_enter(self):
        """Start jump animation on hover"""
        self._start_jump_animation()
        
    def _on_hover_leave(self):
        """Handle hover leave"""
        pass  # Jump animation handles return automatically
        
    def mousePressEvent(self, event):
        """Handle mouse click to create deck"""
        if event.button() == Qt.LeftButton:
            self.create_deck.emit()
        super().mousePressEvent(event)


class StudyDeckCardWidget(BaseDeckCardWidget):
    """Deck card widget for study mode with multi-selection support"""
    
    deck_selected = Signal(int)
    preview_requested = Signal(int)
    
    def __init__(self, deck_data, parent=None):
        self.is_selected = False
        self.sword_label = None
        self.centered_sword = None
        self.text_container = None
        self.preview_btn = None
        super().__init__(deck_data, parent)
        
    def init_ui(self):
        """Initialize the study deck card UI"""
        self._create_jump_animation()
        self._update_style()
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Text content container
        self.text_container = QWidget()
        text_layout = QVBoxLayout(self.text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(4)
        
        # Deck name
        self.name_label = QLabel(self.deck_name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        self.name_label.setWordWrap(True)
        text_layout.addWidget(self.name_label)
        
        # Card count info
        self.count_label = QLabel(f"{self.card_count} cards")
        self.count_label.setAlignment(Qt.AlignCenter)
        self.count_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        text_layout.addWidget(self.count_label)
        
        # Due count (if any)
        if self.due_count > 0:
            self.due_label = QLabel(f"{self.due_count} due")
            self.due_label.setAlignment(Qt.AlignCenter)
            self.due_label.setStyleSheet("""
                QLabel {
                    color: #ff6b6b;
                    font-size: 11px;
                    font-weight: bold;
                    background: transparent;
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                }
            """)
            text_layout.addWidget(self.due_label)
            
        layout.addWidget(self.text_container)
        
        # Centered sword for selection state (initially hidden)
        self.centered_sword = QLabel()
        self.centered_sword.setAlignment(Qt.AlignCenter)
        self.centered_sword.setFixedSize(200, 120)
        self.centered_sword.setStyleSheet("QLabel { background: transparent; border: none; }")
        
        # Load SVG sword image for centered display
        sword_center_path = asset_path("data", "images", "svg", "sword-svgrepo-com.svg")
        if sword_center_path:
            pix = QPixmap(sword_center_path)
            if not pix.isNull():
                scaled = pix.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.centered_sword.setPixmap(scaled)
            else:
                self.centered_sword.setText("⚔️")
        else:
            self.centered_sword.setText("⚔️")
        self.centered_sword.hide()
        
        # Position centered sword to overlay the entire card
        self.centered_sword.move(0, 0)
        self.centered_sword.setParent(self)
        
        layout.addStretch()
        
        # Preview button (tomato icon)
        self.preview_btn = QPushButton()
        self.preview_btn.setFixedSize(28, 28)
        
        # Try to use tomato SVG icon
        tomato_path = asset_path("data", "images", "svg", "tomato-svgrepo-com.svg")
        if tomato_path:
            icon = QIcon(tomato_path)
            if not icon.isNull():
                self.preview_btn.setIcon(icon)
                self.preview_btn.setText("")
            else:
                self.preview_btn.setText("🍅")
        else:
            self.preview_btn.setText("🍅")
        
        self.preview_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #ff6347;
                border: 2px solid transparent;
                border-radius: 14px;
                font-size: 14px;
                font-weight: bold;
                padding: 2px;
            }
            QPushButton:hover {
                background: rgba(255, 99, 71, 0.2);
                border: 2px solid rgba(255, 99, 71, 0.6);
                color: #ff4500;
            }
            QPushButton:pressed {
                background: rgba(255, 99, 71, 0.4);
                border: 2px solid rgba(255, 99, 71, 0.8);
            }
        """)
        
        self.preview_btn.clicked.connect(lambda: self.preview_requested.emit(self.deck_id))
        
        # Center the preview button at bottom
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.preview_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Sword overlay (initially hidden)
        self.sword_label = QLabel()
        self.sword_label.setFixedSize(24, 24)
        self.sword_label.hide()

        # Try to use sword SVG icon
        sword_path = asset_path("data", "images", "svg", "sword-svgrepo-com.svg")
        if sword_path:
            pixmap = QPixmap(sword_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.sword_label.setPixmap(scaled_pixmap)
            else:
                self.sword_label.setText("⚔️")
        else:
            self.sword_label.setText("⚔️")

        self.sword_label.setStyleSheet("QLabel { background: transparent; border: none; }")
        self.sword_label.setContentsMargins(0, 0, 0, 0)

        # Position sword in top-right corner
        self.sword_label.move(170, 10)
        self.sword_label.setParent(self)
        
    def _update_style(self):
        """Update styling based on selection state"""
        if self.is_selected:
            style = """
                StudyDeckCardWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(20, 20, 25, 0.95),
                        stop:1 rgba(10, 10, 15, 0.95));
                    border-radius: 12px;
                    border: none;
                }
                StudyDeckCardWidget:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(30, 30, 35, 0.95),
                        stop:1 rgba(15, 15, 20, 0.95));
                }
            """
        else:
            style = """
                StudyDeckCardWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(60, 60, 60, 0.9),
                        stop:1 rgba(40, 40, 40, 0.9));
                    border-radius: 12px;
                    border: none;
                }
                StudyDeckCardWidget:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(45, 45, 50, 0.95),
                        stop:1 rgba(25, 25, 30, 0.95));
                }
            """
        self.setStyleSheet(style)
    
    def toggle_selection(self):
        """Toggle the selection state of this deck card"""
        self.is_selected = not self.is_selected
        self._update_style()
        self._update_selection_display()
        return self.is_selected
    
    def set_selected(self, selected: bool):
        """Set the selection state explicitly"""
        self.is_selected = selected
        self._update_style()
        self._update_selection_display()
    
    def _update_selection_display(self):
        """Update the visual display based on selection state"""
        if self.is_selected:
            # Hide text content and show centered sword
            self.text_container.hide()
            self.preview_btn.hide()
            self.centered_sword.show()
        else:
            # Show text content and hide centered sword
            self.text_container.show()
            self.preview_btn.show()
            self.centered_sword.hide()
    
    def _on_hover_enter(self):
        """Show sword and start jump animation on hover"""
        if self.sword_label:
            self.sword_label.show()
        self._start_jump_animation()
        
    def _on_hover_leave(self):
        """Hide sword on hover leave"""
        if self.sword_label:
            self.sword_label.hide()
            
    def mousePressEvent(self, event):
        """Handle mouse click to toggle deck selection"""
        if event.button() == Qt.LeftButton:
            self.toggle_selection()
            self.deck_selected.emit(self.deck_id)
        super().mousePressEvent(event)


class ManagementDeckCardWidget(BaseDeckCardWidget):
    """Deck card widget for management mode with hover effects"""
    
    deck_selected = Signal(int)  # For studying
    edit_deck = Signal(int)      # For editing cards
    delete_deck = Signal(int)
    
    def init_ui(self):
        """Initialize the management deck card UI with hover effects"""
        self._create_jump_animation()
        self.setStyleSheet("""
            ManagementDeckCardWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 60, 60, 0.9),
                    stop:1 rgba(40, 40, 40, 0.9));
                border-radius: 12px;
                border: none;
            }
            ManagementDeckCardWidget:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(80, 80, 80, 0.9),
                    stop:1 rgba(60, 60, 60, 0.9));
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        # Deck name
        name_label = QLabel(self.deck_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Card count
        count_label = QLabel(f"{self.card_count} cards")
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 11px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(count_label)
        
        layout.addStretch()
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(4)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedSize(35, 20)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffa726;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background-color: #ff9800;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_deck.emit(self.deck_id))
        actions_layout.addWidget(edit_btn)
        
        # Study button
        study_btn = QPushButton("Study")
        study_btn.setFixedSize(35, 20)
        study_btn.setStyleSheet("""
            QPushButton {
                background-color: #64c8ff;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background-color: #4a9eff;
            }
        """)
        study_btn.clicked.connect(lambda: self.deck_selected.emit(self.deck_id))
        actions_layout.addWidget(study_btn)
        
        # Delete button
        delete_btn = QPushButton("×")
        delete_btn.setFixedSize(20, 20)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6b6b;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_deck.emit(self.deck_id))
        actions_layout.addWidget(delete_btn)
        
        layout.addLayout(actions_layout)
        
    def _on_hover_enter(self):
        """Start jump animation on hover"""
        self._start_jump_animation()
        
    def _on_hover_leave(self):
        """Handle hover leave"""
        pass  # Jump animation handles return automatically
        
    def mousePressEvent(self, event):
        """Handle mouse click on deck card to edit"""
        if event.button() == Qt.LeftButton:
            self.edit_deck.emit(self.deck_id)
        super().mousePressEvent(event)


class SelectionDeckCardWidget(BaseDeckCardWidget):
    """Simple deck card widget for selection mode"""
    
    deck_selected = Signal(int)
    
    def init_ui(self):
        """Initialize the selection deck card UI"""
        self.setStyleSheet("""
            SelectionDeckCardWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 60, 60, 0.9),
                    stop:1 rgba(40, 40, 40, 0.9));
                border-radius: 12px;
                border: 2px solid transparent;
            }
            SelectionDeckCardWidget:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(80, 80, 80, 0.9),
                    stop:1 rgba(60, 60, 60, 0.9));
                border: 2px solid rgba(100, 150, 255, 0.6);
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Deck name
        name_label = QLabel(self.deck_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Card count
        count_label = QLabel(f"{self.card_count} cards")
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(count_label)
        
    def mousePressEvent(self, event):
        """Handle mouse click to select deck"""
        if event.button() == Qt.LeftButton:
            self.deck_selected.emit(self.deck_id)
        super().mousePressEvent(event)
