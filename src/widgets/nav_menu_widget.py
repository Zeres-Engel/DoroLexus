"""
Navigation Menu Widget - Bottom navigation buttons (Statistics, Exit)
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from .mini_card_widget import MiniCardWidget
from ..ui.menu_config import MiniCardConfig


class NavMenuWidget(QWidget):
    """Navigation menu widget for secondary function cards"""
    
    # Signals for navigation
    stats_requested = Signal()
    exit_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mini_card_config = MiniCardConfig()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the navigation menu UI"""
        # Transparent background to show animated background
        self.setStyleSheet("""
            NavMenuWidget {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        # Main horizontal layout
        layout = QHBoxLayout(self)
        layout.setSpacing(400)  # Large spacing between nav buttons
        layout.setAlignment(Qt.AlignHCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create secondary function cards
        self._create_nav_cards(layout)
        
    def _create_nav_cards(self, layout):
        """Create the navigation cards"""
        
        # Statistics card
        self.stats_card = MiniCardWidget(
            "Statistics", 
            "research-svgrepo-com.svg", 
            "#7C3AED",
            self.mini_card_config
        )
        self.stats_card.clicked.connect(self.stats_requested.emit)
        layout.addWidget(self.stats_card)
        
        # Exit card
        self.exit_card = MiniCardWidget(
            "Exit", 
            "school-bell-svgrepo-com.svg", 
            "#DC2626",
            self.mini_card_config
        )
        self.exit_card.clicked.connect(self.exit_requested.emit)
        layout.addWidget(self.exit_card)
        
    def resizeEvent(self, event):
        """Handle responsive layout changes"""
        super().resizeEvent(event)
        
        # Get current width
        current_width = self.width()
        
        # Switch to vertical stack on narrow widths
        layout = self.layout()
        if layout:
            if current_width < 520:
                layout.setDirection(QHBoxLayout.TopToBottom)
                layout.setSpacing(20)
            else:
                layout.setDirection(QHBoxLayout.LeftToRight)
                layout.setSpacing(400)  # Wide spacing for horizontal layout
