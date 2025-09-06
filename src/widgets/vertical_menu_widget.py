"""
Vertical Menu Widget - Main menu cards (Study, Decks, Timer)
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal
from .menu_card_widget import MenuCardWidget
from ..ui.menu_config import MenuCardConfig


class VerticalMenuWidget(QWidget):
    """Vertical menu widget for main function cards"""
    
    # Signals for navigation
    study_requested = Signal()
    decks_requested = Signal()
    timer_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_card_config = MenuCardConfig()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the vertical menu UI"""
        # Transparent background to show animated background
        self.setStyleSheet("""
            VerticalMenuWidget {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        # Set maximum width to keep organized
        self.setMaximumWidth(750)
        
        # Create container for better responsive control
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Main vertical layout
        layout = QVBoxLayout(self)
        layout.setSpacing(80)  # Default spacing - will be adjusted responsively
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.setContentsMargins(20, 30, 20, 20)
        
        # Create main function cards
        self._create_main_cards(layout)
        
    def _create_main_cards(self, layout):
        """Create the main function cards with responsive spacing"""
        
        # Study card
        self.study_card = MenuCardWidget(
            "Study Flashcards",
            "Review and learn your vocabulary with spaced repetition",
            "sword-svgrepo-com.svg",
            "#2563EB",
            self.menu_card_config
        )
        self.study_card.clicked.connect(self.study_requested.emit)
        self.study_card.setFixedWidth(self.menu_card_config.width)
        layout.addWidget(self.study_card, alignment=Qt.AlignHCenter)
        
        # Decks card
        self.decks_card = MenuCardWidget(
            "Manage Decks",
            "Create and organize your study decks and flashcards",
            "tomato-svgrepo-com.svg",
            "#059669",
            self.menu_card_config
        )
        self.decks_card.clicked.connect(self.decks_requested.emit)
        self.decks_card.setFixedWidth(self.menu_card_config.width)
        layout.addWidget(self.decks_card, alignment=Qt.AlignHCenter)
        
        # Timer card
        self.timer_card = MenuCardWidget(
            "Study Timer",
            "Focus sessions with Pomodoro technique - Easy, Normal, Hard modes",
            "clock-svgrepo-com.svg",
            "#D97706",
            self.menu_card_config
        )
        self.timer_card.clicked.connect(self.timer_requested.emit)
        self.timer_card.setFixedWidth(self.menu_card_config.width)
        layout.addWidget(self.timer_card, alignment=Qt.AlignHCenter)
        
    def resizeEvent(self, event):
        """Handle responsive layout changes with dynamic spacing"""
        super().resizeEvent(event)
        
        # Get current dimensions
        current_width = self.width()
        current_height = self.height()
        
        # Responsive card width
        available_width = max(400, min(current_width - 100, self.menu_card_config.width))
        
        # Resize main cards to available width
        for card in [self.study_card, self.decks_card, self.timer_card]:
            card.setFixedWidth(available_width)
        
        # SMART RESPONSIVE SPACING: Ensure all buttons are visible while maintaining good spacing
        layout = self.layout()
        if layout:
            # Calculate available space for the three main cards
            # Each card is about 80px high, plus we need space for margins
            card_height = 80  # Approximate height of each card
            total_card_height = 3 * card_height  # Three cards
            available_height = current_height - layout.contentsMargins().top() - layout.contentsMargins().bottom()
            remaining_space = available_height - total_card_height
            
            if remaining_space > 200:
                # Plenty of space - use generous spacing
                vertical_spacing = min(120, remaining_space // 3)
                top_margin = 40
            elif remaining_space > 100:
                # Medium space - balanced spacing
                vertical_spacing = min(80, remaining_space // 3)
                top_margin = 30
            else:
                # Tight space - minimal spacing but all buttons visible
                vertical_spacing = max(20, remaining_space // 3)
                top_margin = 20
            
            # Apply calculated spacing
            layout.setSpacing(vertical_spacing)
            mleft, _, mright, mbottom = layout.contentsMargins().left(), 0, layout.contentsMargins().right(), layout.contentsMargins().bottom()
            layout.setContentsMargins(mleft, top_margin, mright, mbottom)
