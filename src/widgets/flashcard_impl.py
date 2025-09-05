"""
Flashcard widget for displaying and interacting with flashcards
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
    
    def __init__(self, front_text: str = "", back_text: str = "", parent=None):
        super().__init__(parent)
        self.front_text = front_text
        self.back_text = back_text
        self.is_flipped = False
        self.init_ui()
        self.setup_animations()
        
    def init_ui(self):
        """Initialize the flashcard UI"""
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #ddd;
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
                background-color: #f8f9fa;
                border-radius: 10px;
                border: 1px solid #e9ecef;
            }
        """)
        self.content_frame.setMinimumHeight(250)
        
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Card text
        self.card_label = QLabel()
        self.card_label.setAlignment(Qt.AlignCenter)
        self.card_label.setWordWrap(True)
        self.card_label.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        content_layout.addWidget(self.card_label)
        
        layout.addWidget(self.content_frame)
        
        # Flip button
        self.flip_button = QPushButton("Show Answer")
        self.flip_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
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
        rating_colors = ["#dc3545", "#fd7e14", "#ffc107", "#28a745", "#20c997"]
        
        for i, (label, color) in enumerate(zip(rating_labels, rating_colors)):
            btn = QPushButton(label)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
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
            "#dc3545": "#c82333",
            "#fd7e14": "#e55a00", 
            "#ffc107": "#e0a800",
            "#28a745": "#218838",
            "#20c997": "#1ea085"
        }
        return color_map.get(color, color)
        
    def set_card_content(self, front_text: str, back_text: str):
        """Set the card content"""
        self.front_text = front_text
        self.back_text = back_text
        self.is_flipped = False
        self.update_content()
        self.reset_ui_state()
        
    def update_content(self):
        """Update the displayed content based on flip state"""
        if self.is_flipped:
            self.card_label.setText(self.back_text)
            self.flip_button.setText("Show Question")
        else:
            self.card_label.setText(self.front_text)
            self.flip_button.setText("Show Answer")
            
    def flip_card(self):
        """Flip the card to show front or back"""
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
        self.rating_container.setVisible(False)
        self.flip_button.setVisible(True)
        
    def paintEvent(self, event):
        """Custom paint event for card styling"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw card shadow
        shadow_rect = self.rect().adjusted(5, 5, 0, 0)
        painter.fillRect(shadow_rect, QColor(0, 0, 0, 30))
        
        # Draw card background
        card_rect = self.rect().adjusted(0, 0, -5, -5)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(221, 221, 221), 2))
        painter.drawRoundedRect(card_rect, 15, 15)
        
        painter.end()
        super().paintEvent(event)
