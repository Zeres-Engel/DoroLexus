"""
Independent Responsive Deck Card Widget
Handles its own positioning and responsive behavior
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QRect
from PySide6.QtGui import QFont, QIcon
from src.core.paths import asset_path


class ResponsiveDeckCardWidget(QFrame):
    """Independent deck card widget with built-in responsive behavior"""
    
    deck_selected = Signal(int)  # Emits deck_id when selected/deselected
    preview_requested = Signal(int)  # Emits deck_id when preview button clicked
    
    def __init__(self, deck_data, parent=None):
        super().__init__(parent)
        self.deck_id = deck_data['id']
        self.deck_name = deck_data['name']
        self.card_count = deck_data['card_count']
        self.due_count = deck_data.get('due_count', 0)
        self.is_selected = False
        self._is_hovered = False
        self._jump_animation = None
        self._original_pos = None
        
        # Fixed size for consistent layout
        self.setFixedSize(200, 120)
        self.setCursor(Qt.PointingHandCursor)
        
        # Animation setup - use visual effects instead of geometry changes
        self._is_hovered = False
        self._hover_effect = None
        
        self.init_ui()
        self._update_style()
        
        # No need to cache position since we're not moving the widget
        
    def init_ui(self):
        """Initialize the deck card UI"""
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
        else:
            self.due_label = None
            
        layout.addWidget(self.text_container)
        
        # Centered sword for selection state (initially hidden)
        self.centered_sword = QLabel()
        self.centered_sword.setAlignment(Qt.AlignCenter)
        self.centered_sword.setFixedSize(200, 120)
        self.centered_sword.setStyleSheet("QLabel { background: transparent; border: none; }")
        # Load SVG sword image for centered display
        sword_center_path = asset_path("data", "images", "svg", "sword-svgrepo-com.svg")
        if sword_center_path:
            from PySide6.QtGui import QPixmap
            _pix = QPixmap(sword_center_path)
            if not _pix.isNull():
                scaled = _pix.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
        
        # Preview button (tomato icon) - centered at bottom
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
        
        # Sword overlay (initially hidden) - transparent background, no border
        self.sword_label = QLabel()
        self.sword_label.setFixedSize(24, 24)
        self.sword_label.hide()

        # Try to use sword SVG icon
        sword_path = asset_path("data", "images", "svg", "sword-svgrepo-com.svg")
        if sword_path:
            from PySide6.QtGui import QPixmap
            pixmap = QPixmap(sword_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.sword_label.setPixmap(scaled_pixmap)
            else:
                self.sword_label.setText("⚔️")
        else:
            self.sword_label.setText("⚔️")

        self.sword_label.setStyleSheet("QLabel { background: transparent; border: none; }")
        try:
            self.sword_label.setAttribute(Qt.WA_TranslucentBackground, True)
        except Exception:
            pass
        self.sword_label.setContentsMargins(0, 0, 0, 0)

        # Position sword in top-right corner
        self.sword_label.move(170, 10)
        self.sword_label.setParent(self)
        
    def _update_style(self):
        """Update styling based on selection state"""
        if self.is_selected:
            style = """
                ResponsiveDeckCardWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(20, 20, 25, 0.95),
                        stop:1 rgba(10, 10, 15, 0.95));
                    border-radius: 12px;
                    border: none;
                }
                ResponsiveDeckCardWidget QLabel { border: none; background: transparent; }
                ResponsiveDeckCardWidget:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(30, 30, 35, 0.95),
                        stop:1 rgba(15, 15, 20, 0.95));
                }
            """
        else:
            style = """
                ResponsiveDeckCardWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(60, 60, 60, 0.9),
                        stop:1 rgba(40, 40, 40, 0.9));
                    border-radius: 12px;
                    border: none;
                }
                ResponsiveDeckCardWidget QLabel { border: none; background: transparent; }
                ResponsiveDeckCardWidget:hover {
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
    
    def _create_hover_effect(self):
        """Create a visual hover effect with jump animation (no shadow)"""
        # Create jump animation only - no shadow effect
        self._start_jump_animation()
    
    def _remove_hover_effect(self):
        """Remove the hover effect and stop animation"""
        # Stop any running jump animation
        if self._jump_animation and self._jump_animation.state() == QPropertyAnimation.Running:
            self._jump_animation.stop()
    
    def _start_jump_animation(self):
        """Start the jump animation"""
        if self._jump_animation and self._jump_animation.state() == QPropertyAnimation.Running:
            return  # Animation already running
        
        # Store original position if not already stored
        if self._original_pos is None:
            self._original_pos = self.pos()
        
        # Create jump animation
        self._jump_animation = QPropertyAnimation(self, b"pos")
        self._jump_animation.setDuration(150)  # Quick jump
        self._jump_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Jump up by 8 pixels
        jump_pos = QPoint(self._original_pos.x(), self._original_pos.y() - 8)
        self._jump_animation.setStartValue(self._original_pos)
        self._jump_animation.setEndValue(jump_pos)
        
        # Connect finished signal to return to original position
        self._jump_animation.finished.connect(self._on_jump_finished)
        self._jump_animation.start()
    
    def _on_jump_finished(self):
        """Handle jump animation finished - return to original position"""
        if self._jump_animation:
            # Create return animation
            return_animation = QPropertyAnimation(self, b"pos")
            return_animation.setDuration(100)  # Quick return
            return_animation.setEasingCurve(QEasingCurve.InCubic)
            
            return_animation.setStartValue(self.pos())
            return_animation.setEndValue(self._original_pos)
            return_animation.start()
    
    def enterEvent(self, event):
        """Show sword and create hover effect with jump"""
        if self.sword_label:
            self.sword_label.show()
        
        # Only create effect if not already in hover state
        if not self._is_hovered:
            self._is_hovered = True
            self._create_hover_effect()
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Hide sword and remove hover effect"""
        if self.sword_label:
            self.sword_label.hide()
        
        # Only remove effect if currently in hover state
        if self._is_hovered:
            self._is_hovered = False
            self._remove_hover_effect()
            # Reset position immediately when leaving
            if self._original_pos is not None:
                self.move(self._original_pos)
        
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Handle mouse click to toggle deck selection"""
        if event.button() == Qt.LeftButton:
            self.toggle_selection()
            self.deck_selected.emit(self.deck_id)
        super().mousePressEvent(event)
    
    def get_deck_id(self):
        """Get the deck ID"""
        return self.deck_id
    
    def is_deck_selected(self):
        """Check if this deck is selected"""
        return self.is_selected
    
    def move(self, pos):
        """Override move to update original position"""
        super().move(pos)
        # Update original position if we're not currently animating
        if not (self._jump_animation and self._jump_animation.state() == QPropertyAnimation.Running):
            self._original_pos = pos
    
    def reset_position(self):
        """Reset the widget to its original position and stop any animations"""
        if self._jump_animation and self._jump_animation.state() == QPropertyAnimation.Running:
            self._jump_animation.stop()
        
        if self._original_pos is not None:
            self.move(self._original_pos)
        else:
            # If no original position stored, use current position
            self._original_pos = self.pos()
