"""
Stats page wrapper for statistics
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from src.modes.stats_impl import StatsWidget
from src.ui import StatsPageHeaderLayout


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
        
        # Page header
        self.header = StatsPageHeaderLayout()
        layout.addWidget(self.header)
        
        # Use the existing StatsWidget implementation
        self.stats_widget = StatsWidget(self.db_manager)
        layout.addWidget(self.stats_widget)
        
    def refresh_stats(self):
        """Refresh the statistics"""
        self.stats_widget.refresh_stats()
