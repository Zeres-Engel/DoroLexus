"""
Page Header Layout Components
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from ..widgets.button_widget import PrimaryButtonWidget


class PageHeaderLayout(QWidget):
    """Standard page header layout with title and optional back button"""
    
    back_requested = Signal()
    
    def __init__(self, title: str, show_back_button: bool = False, parent=None):
        super().__init__(parent)
        self.title = title
        self.show_back_button = show_back_button
        self.init_ui()
        
    def init_ui(self):
        """Initialize the page header UI"""
        self.setStyleSheet("""
            PageHeaderLayout {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(self.title_label)
        
        # Spacer
        layout.addStretch()
        
        # Back button (optional)
        self.back_btn = PrimaryButtonWidget("← Back")
        self.back_btn.clicked.connect(self.back_requested.emit)
        self.back_btn.setVisible(self.show_back_button)
        layout.addWidget(self.back_btn)
        
    def set_back_button_visible(self, visible: bool):
        """Show or hide the back button"""
        self.back_btn.setVisible(visible)
        
    def set_title(self, title: str):
        """Update the page title"""
        self.title = title
        self.title_label.setText(title)


class StudyPageHeaderLayout(PageHeaderLayout):
    """Specialized header for study page with deck selection and study modes"""
    
    def __init__(self, parent=None):
        super().__init__("Study Mode", show_back_button=False, parent=parent)
        self.init_study_ui()
        
    def init_study_ui(self):
        """Initialize study-specific UI elements"""
        # The back button will be shown/hidden based on study state
        self.back_btn.setText("← Back to Decks")
        
    def show_study_mode(self):
        """Show back button when in study mode"""
        self.set_back_button_visible(True)
        
    def show_deck_selection(self):
        """Hide back button when in deck selection"""
        self.set_back_button_visible(False)


class DecksPageHeaderLayout(PageHeaderLayout):
    """Specialized header for decks page"""
    
    def __init__(self, parent=None):
        super().__init__("Deck Management", show_back_button=False, parent=parent)
        self.init_decks_ui()
        
    def init_decks_ui(self):
        """Initialize decks-specific UI elements"""
        # Add any decks-specific header elements here if needed
        pass


class StatsPageHeaderLayout(PageHeaderLayout):
    """Specialized header for stats page"""
    
    def __init__(self, parent=None):
        super().__init__("Statistics", show_back_button=False, parent=parent)
        self.init_stats_ui()
        
    def init_stats_ui(self):
        """Initialize stats-specific UI elements"""
        # Add any stats-specific header elements here if needed
        pass


class TimerPageHeaderLayout(PageHeaderLayout):
    """Specialized header for timer page"""
    
    def __init__(self, parent=None):
        super().__init__("Study Timer", show_back_button=False, parent=parent)
        self.init_timer_ui()
        
    def init_timer_ui(self):
        """Initialize timer-specific UI elements"""
        # Add any timer-specific header elements here if needed
        pass
