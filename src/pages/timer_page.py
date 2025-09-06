"""
Timer page wrapper for study timer
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from src.modes.timer_impl import StudyTimerWidget
from src.ui import TimerPageHeaderLayout


class TimerPage(QWidget):
    """Timer page wrapper"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the timer page"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Page header
        self.header = TimerPageHeaderLayout()
        layout.addWidget(self.header)
        
        # Use the existing StudyTimerWidget implementation
        self.timer_widget = StudyTimerWidget()
        layout.addWidget(self.timer_widget)
