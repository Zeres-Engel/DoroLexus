"""
Stats page wrapper for statistics
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from src.modes.stats_impl import StatsWidget
from src.widgets.nav_bar_widget import NavBarWidget


class StatsPage(QWidget):
    """Stats page wrapper"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.init_ui()
        
    def init_ui(self):
        """Initialize the stats page"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Top navigation bar
        self.navbar = NavBarWidget("Statistics", show_back_button=False)
        self.navbar.home_requested.connect(self._navigate_to_home)
        layout.addWidget(self.navbar)
        
        # Use the existing StatsWidget implementation
        self.stats_widget = StatsWidget(self.db_manager)
        layout.addWidget(self.stats_widget)
        
    def refresh_stats(self):
        """Refresh the statistics"""
        self.stats_widget.refresh_stats()
        
    def _navigate_to_home(self):
        """Navigate to home page through parent window"""
        try:
            ancestor = self.parent()
            max_hops = 5
            while ancestor and max_hops > 0:
                if hasattr(ancestor, 'show_home') and callable(getattr(ancestor, 'show_home')):
                    ancestor.show_home()
                    return
                ancestor = ancestor.parent()
                max_hops -= 1
        except Exception:
            pass
