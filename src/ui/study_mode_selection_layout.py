"""
Study Mode Selection Layout - Choose how to study a deck
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QFrame, QGridLayout, QPushButton)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon
from ..widgets.button_widget import PrimaryButtonWidget


class StudyModeCard(QFrame):
    """Individual study mode card with icon and description"""
    
    mode_selected = Signal(str)  # Emits mode type
    
    def __init__(self, mode_type, title, description, icon_text="📚", color="#64c8ff", parent=None):
        super().__init__(parent)
        self.mode_type = mode_type
        self.title = title
        self.description = description
        self.icon_text = icon_text
        self.color = color
        self.init_ui()
        
    def init_ui(self):
        """Initialize the study mode card UI"""
        self.setFixedSize(280, 160)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            StudyModeCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 60, 60, 0.9),
                    stop:1 rgba(40, 40, 40, 0.9));
                border-radius: 16px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }}
            StudyModeCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(80, 80, 80, 0.9),
                    stop:1 rgba(60, 60, 60, 0.9));
                border: 2px solid {self.color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Icon
        icon_label = QLabel(self.icon_text)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {self.color};
                font-size: 48px;
                background: transparent;
                font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji";
            }}
        """)
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.color};
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }}
        """)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(self.description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(desc_label)
        
    def mousePressEvent(self, event):
        """Handle mouse click to select mode"""
        if event.button() == Qt.LeftButton:
            self.mode_selected.emit(self.mode_type)
        super().mousePressEvent(event)


class StudyModeSelectionLayout(QWidget):
    """Layout for selecting study mode after choosing a deck"""
    
    mode_selected = Signal(str)  # Study mode type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_deck_id = None
        self.current_deck_name = ""
        self.card_count = 0
        self.init_ui()
        
    def init_ui(self):
        """Initialize the study mode selection UI"""
        self.setStyleSheet("""
            StudyModeSelectionLayout {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)
        
        # Header with deck info
        header_layout = QVBoxLayout()
        
        # Deck title
        self.deck_title = QLabel()
        self.deck_title.setAlignment(Qt.AlignCenter)
        self.deck_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                margin: 20px 0px;
            }
        """)
        header_layout.addWidget(self.deck_title)
        
        # Deck info
        self.deck_info = QLabel()
        self.deck_info.setAlignment(Qt.AlignCenter)
        self.deck_info.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 16px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        header_layout.addWidget(self.deck_info)
        
        layout.addLayout(header_layout)
        
        # Study mode selection title
        mode_title = QLabel("Choose Your Study Mode")
        mode_title.setAlignment(Qt.AlignCenter)
        mode_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                margin: 10px 0px;
            }
        """)
        layout.addWidget(mode_title)
        
        # Study mode cards
        modes_layout = QGridLayout()
        modes_layout.setSpacing(20)
        modes_layout.setAlignment(Qt.AlignCenter)
        
        # Define study modes
        study_modes = [
            {
                "type": "review",
                "title": "Review",
                "description": "Study with spaced repetition algorithm",
                "icon": "🧠",
                "color": "#64c8ff"
            },
            {
                "type": "test",
                "title": "Test Mode", 
                "description": "Quiz yourself without revealing answers",
                "icon": "✏️",
                "color": "#ff6b6b"
            },
            {
                "type": "browse",
                "title": "Browse Cards",
                "description": "Go through cards at your own pace",
                "icon": "📖",
                "color": "#66bb6a"
            },
            {
                "type": "cram",
                "title": "Cram Session",
                "description": "Quick review of all cards",
                "icon": "⚡",
                "color": "#ffa726"
            },
            {
                "type": "new_only",
                "title": "New Cards",
                "description": "Study only new, unseen cards",
                "icon": "✨",
                "color": "#ab47bc"
            },
            {
                "type": "difficult",
                "title": "Difficult Cards",
                "description": "Focus on cards you find challenging",
                "icon": "🎯",
                "color": "#f44336"
            }
        ]
        
        # Create mode cards
        for i, mode in enumerate(study_modes):
            mode_card = StudyModeCard(
                mode["type"],
                mode["title"], 
                mode["description"],
                mode["icon"],
                mode["color"]
            )
            mode_card.mode_selected.connect(self.mode_selected.emit)
            
            row = i // 3
            col = i % 3
            modes_layout.addWidget(mode_card, row, col)
        
        layout.addLayout(modes_layout)
        layout.addStretch()
        
    def set_deck_info(self, deck_id, deck_name, card_count, due_count=0):
        """Set the current deck information"""
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.card_count = card_count
        
        self.deck_title.setText(deck_name)
        
        info_text = f"{card_count} cards total"
        if due_count > 0:
            info_text += f" • {due_count} cards due for review"
        self.deck_info.setText(info_text)
