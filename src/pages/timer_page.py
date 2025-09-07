"""
Timer page wrapper for study timer
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout
from src.modes.timer_impl import StudyTimerWidget
from src.widgets.nav_bar_widget import NavBarWidget


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
        
        # Top navigation bar
        self.navbar = NavBarWidget("Study Timer", show_back_button=False)
        self.navbar.home_requested.connect(self._navigate_to_home)
        layout.addWidget(self.navbar)
        
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
        
        # Use the existing StudyTimerWidget implementation
        self.timer_widget = StudyTimerWidget()
        layout.addWidget(self.timer_widget)
