"""
Page Header Layout Components
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QIcon
from ..widgets.button_widget import PrimaryButtonWidget
from src.core.paths import asset_path


class PageHeaderLayout(QWidget):
    """Standard page header layout with logo, title and optional back button"""
    
    back_requested = Signal()
    home_requested = Signal()
    
    def __init__(self, title: str, show_back_button: bool = False, parent=None):
        super().__init__(parent)
        self.title = title
        self.show_back_button = show_back_button
        self.init_ui()
        
    def init_ui(self):
        """Initialize the page header UI with logo and enhanced styling"""
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
        layout.setSpacing(15)
        
        # DoroLexus logo (clickable)
        self.logo_label = QLabel()
        self.logo_label.setCursor(Qt.PointingHandCursor)
        logo_path = asset_path("data", "images", "svg", "doro_lexus logo.svg")
        if logo_path:
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                # Scale logo to fit header height
                scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.mousePressEvent = self._on_logo_clicked
        layout.addWidget(self.logo_label)
        
        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                margin-left: 10px;
            }
        """)
        layout.addWidget(self.title_label)
        
        # Spacer
        layout.addStretch()
        
        # Enhanced back button with sword styling
        self.back_btn = QPushButton()
        self._setup_sword_back_button()
        self.back_btn.clicked.connect(self.back_requested.emit)
        self.back_btn.setVisible(self.show_back_button)
        layout.addWidget(self.back_btn)
        
    def _setup_sword_back_button(self):
        """Setup the sword-styled back button"""
        sword_path = asset_path("data", "images", "svg", "sword-svgrepo-com.svg")
        
        self.back_btn.setText("⚔️ Back")
        self.back_btn.setFixedSize(120, 40)
        
        button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 100, 100, 0.9),
                    stop:1 rgba(60, 60, 60, 0.9));
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(120, 120, 120, 0.9),
                    stop:1 rgba(80, 80, 80, 0.9));
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(80, 80, 80, 0.9),
                    stop:1 rgba(40, 40, 40, 0.9));
            }
        """
        
        # Try to add sword icon if available
        if sword_path:
            icon = QIcon(sword_path)
            if not icon.isNull():
                self.back_btn.setIcon(icon)
                self.back_btn.setText(" Back")  # Less text since we have icon
                
        self.back_btn.setStyleSheet(button_style)
        
    def _on_logo_clicked(self, event):
        """Handle logo click to navigate home"""
        if event.button() == Qt.LeftButton:
            self.home_requested.emit()
        
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
