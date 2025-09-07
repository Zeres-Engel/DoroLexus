"""
Flashcard Widget for displaying and interacting with flashcards
Includes flip animation and study controls
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTextEdit, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, Signal
from PySide6.QtGui import QFont, QPainter, QPen, QBrush, QColor

class FlashcardWidget(QWidget):
    """Widget for displaying individual flashcards with flip animation"""
    
    # Signals
    card_flipped = Signal(bool)  # True when showing back, False when showing front
    study_rating = Signal(int)   # Rating from 0-5 for spaced repetition
    
    def __init__(self, front_text: str = "", back_text: str = "", parent=None, side_by_side: bool = False):
        super().__init__(parent)
        self.front_text = front_text
        self.back_text = back_text
        self.is_flipped = False
        self.side_by_side = side_by_side
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        """Initialize the flashcard UI"""
        self.setFixedSize(800 if self.side_by_side else 600, 400)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(45, 45, 45, 0.95),
                    stop:1 rgba(30, 30, 30, 0.95));
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Card content area
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 60, 60, 0.8),
                    stop:1 rgba(40, 40, 40, 0.8));
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        self.content_frame.setMinimumHeight(250)
        
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Single label view
        self.card_label = QLabel()
        self.card_label.setAlignment(Qt.AlignCenter)
        self.card_label.setWordWrap(True)
        self.card_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        content_layout.addWidget(self.card_label)
        
        # Side-by-side view container
        self.two_col_container = QWidget()
        two_col_layout = QHBoxLayout(self.two_col_container)
        two_col_layout.setContentsMargins(0, 0, 0, 0)
        two_col_layout.setSpacing(12)
        
        def build_pane(title: str) -> QVBoxLayout:
            pane = QFrame()
            pane.setStyleSheet("""
                QFrame {
                    background: rgba(30, 30, 30, 0.6);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                }
            """)
            pane_layout = QVBoxLayout(pane)
            pane_layout.setContentsMargins(12, 12, 12, 12)
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignLeft)
            title_label.setStyleSheet("""
                QLabel {
                    color: rgba(255,255,255,0.7);
                    font-size: 12px;
                    font-weight: bold;
                    background: transparent;
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                }
            """)
            pane_layout.addWidget(title_label)
            return pane, pane_layout
        
        self.left_pane, self.left_layout = build_pane("Question")
        self.right_pane, self.right_layout = build_pane("Answer")
        
        self.left_label = QLabel()
        self.left_label.setWordWrap(True)
        self.left_label.setStyleSheet(self.card_label.styleSheet())
        self.right_label = QLabel()
        self.right_label.setWordWrap(True)
        self.right_label.setStyleSheet(self.card_label.styleSheet())
        self.left_layout.addWidget(self.left_label)
        self.right_layout.addWidget(self.right_label)
        two_col_layout.addWidget(self.left_pane)
        two_col_layout.addWidget(self.right_pane)
        content_layout.addWidget(self.two_col_container)
        
        layout.addWidget(self.content_frame)
        
        # Flip button
        self.flip_button = QPushButton("Show Answer")
        self.flip_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #64c8ff,
                    stop:1 #4a9eff);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ab8ff,
                    stop:1 #3d8eff);
            }
        """)
        self.flip_button.clicked.connect(self.flip_card)
        layout.addWidget(self.flip_button)
        
        # Study rating buttons (initially hidden)
        # Wrap layout in a QWidget container so we can toggle visibility
        self.rating_container = QWidget()
        self.rating_layout = QHBoxLayout(self.rating_container)
        self.rating_layout.setSpacing(10)
        
        self.rating_buttons = []
        rating_labels = ["Again", "Hard", "Good", "Easy", "Perfect"]
        rating_colors = ["#ff6b6b", "#ffa726", "#ffeb3b", "#66bb6a", "#42a5f5"]
        
        for i, (label, color) in enumerate(zip(rating_labels, rating_colors)):
            btn = QPushButton(label)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {color},
                        stop:1 {self.darken_color(color)});
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {self.lighten_color(color)},
                        stop:1 {color});
                }}
            """)
            btn.clicked.connect(lambda checked, rating=i: self.rate_card(rating))
            self.rating_buttons.append(btn)
            self.rating_layout.addWidget(btn)
            
        layout.addWidget(self.rating_container)
        self.rating_container.setVisible(False)
        
        # Set initial content
        self.update_content()
        
    def setup_animations(self):
        """Setup flip animations"""
        self.flip_animation = QPropertyAnimation(self, b"geometry")
        self.flip_animation.setDuration(300)
        self.flip_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
    def darken_color(self, color: str) -> str:
        """Darken a hex color for hover effects"""
        color_map = {
            "#ff6b6b": "#ff5252",
            "#ffa726": "#ff9800", 
            "#ffeb3b": "#fdd835",
            "#66bb6a": "#4caf50",
            "#42a5f5": "#2196f3"
        }
        return color_map.get(color, color)
        
    def lighten_color(self, color: str) -> str:
        """Lighten a hex color for hover effects"""
        color_map = {
            "#ff6b6b": "#ff8a80",
            "#ffa726": "#ffb74d", 
            "#ffeb3b": "#fff176",
            "#66bb6a": "#81c784",
            "#42a5f5": "#64b5f6"
        }
        return color_map.get(color, color)
        
    def set_card_content(self, front_text: str, back_text: str):
        """Set the card content"""
        self.front_text = front_text
        self.back_text = back_text
        self.is_flipped = False
        self.update_content()
        self.reset_ui_state()

    def set_side_by_side(self, enabled: bool):
        """Toggle side-by-side display mode"""
        self.side_by_side = enabled
        self.setFixedSize(800 if self.side_by_side else 600, 400)
        self.update_content()
        # In side-by-side view, show ratings immediately and hide flip
        self.rating_container.setVisible(self.side_by_side)
        self.flip_button.setVisible(not self.side_by_side)
        
    def update_content(self):
        """Update the displayed content based on flip state"""
        if self.side_by_side:
            # Show both columns
            self.card_label.setVisible(False)
            self.two_col_container.setVisible(True)
            self.left_label.setText(self.front_text)
            self.right_label.setText(self.back_text)
            self.flip_button.setText("Show Answer")
        else:
            # Single label with flip behavior
            self.card_label.setVisible(True)
            self.two_col_container.setVisible(False)
            if self.is_flipped:
                self.card_label.setText(self.back_text)
                self.flip_button.setText("Show Question")
            else:
                self.card_label.setText(self.front_text)
                self.flip_button.setText("Show Answer")
            
    def flip_card(self):
        """Flip the card to show front or back"""
        if self.side_by_side:
            return
        self.is_flipped = not self.is_flipped
        self.update_content()
        self.card_flipped.emit(self.is_flipped)
        
        # Show rating buttons when showing back
        if self.is_flipped:
            self.rating_container.setVisible(True)
            self.flip_button.setVisible(False)
        else:
            self.rating_container.setVisible(False)
            self.flip_button.setVisible(True)
            
    def rate_card(self, rating: int):
        """Rate the card and emit signal"""
        self.study_rating.emit(rating)
        self.reset_ui_state()
        
    def reset_ui_state(self):
        """Reset UI to initial state"""
        self.is_flipped = False
        self.update_content()
        if self.side_by_side:
            self.rating_container.setVisible(True)
            self.flip_button.setVisible(False)
        else:
            self.rating_container.setVisible(False)
            self.flip_button.setVisible(True)
        
    def paintEvent(self, event):
        """Custom paint event for card styling"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw card shadow
        shadow_rect = self.rect().adjusted(8, 8, 0, 0)
        painter.fillRect(shadow_rect, QColor(0, 0, 0, 60))
        
        # Draw card background with gradient
        card_rect = self.rect().adjusted(0, 0, -8, -8)
        gradient = QBrush(QColor(45, 45, 45))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(255, 255, 255, 50), 2))
        painter.drawRoundedRect(card_rect, 15, 15)
        
        painter.end()
        super().paintEvent(event)
