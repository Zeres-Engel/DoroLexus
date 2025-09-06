"""
Home page for DoroLexus - Refactored with modular widget components
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import QBoxLayout
from src.widgets import WelcomeBannerWidget, VerticalMenuWidget, NavMenuWidget




class HomePage(QWidget):
    """Main home page with refactored UI components"""
    
    # Signals for navigation
    study_requested = Signal()
    decks_requested = Signal()
    timer_requested = Signal()
    stats_requested = Signal()
    exit_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the home page UI with refactored components"""
        # Transparent background to show animated background
        self.setStyleSheet("""
            HomePage {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        # Main vertical layout with responsive behavior
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add margins for responsiveness
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)  # Center everything
        
        # Add top stretch to push content toward center
        main_layout.addStretch(1)
        
        # Welcome banner widget with container for better centering
        self.banner_widget = WelcomeBannerWidget()
        
        # Create a container to ensure proper centering
        banner_container = QWidget()
        banner_container.setStyleSheet("QWidget { background: transparent; }")
        banner_container.setMaximumWidth(800)  # Maximum width for large screens
        
        # Banner horizontal layout - always centered
        banner_layout = QHBoxLayout(banner_container)
        banner_layout.setContentsMargins(0, 0, 0, 0)
        banner_layout.addStretch(1)  # Left stretch
        banner_layout.addWidget(self.banner_widget, 0, Qt.AlignCenter)
        banner_layout.addStretch(1)  # Right stretch
        
        main_layout.addWidget(banner_container, 0, Qt.AlignHCenter)
        
        # Add minimal spacing between banner and vertical menu
        main_layout.addSpacing(5)
        
        # Vertical menu widget for main functions
        self.vertical_menu = VerticalMenuWidget()
        
        # Connect vertical menu signals to page signals
        self.vertical_menu.study_requested.connect(self.study_requested.emit)
        self.vertical_menu.decks_requested.connect(self.decks_requested.emit)
        self.vertical_menu.timer_requested.connect(self.timer_requested.emit)
        
        # Add vertical menu to main layout with center alignment
        main_layout.addWidget(self.vertical_menu, 0, Qt.AlignHCenter)
        
        # Add spacing between vertical menu and navigation menu
        main_layout.addSpacing(20)
        
        # Navigation menu widget for secondary functions
        self.nav_menu = NavMenuWidget()
        
        # Connect navigation menu signals to page signals
        self.nav_menu.stats_requested.connect(self.stats_requested.emit)
        self.nav_menu.exit_requested.connect(self.exit_requested.emit)
        
        # Add navigation menu to main layout with center alignment
        main_layout.addWidget(self.nav_menu, 0, Qt.AlignHCenter)
        
        # Add bottom stretch to push content toward center
        main_layout.addStretch(1)
        
    def show_with_animation(self):
        """Show the page with welcome animation"""
        # Force layout calculation before starting animation
        self.layout().activate()
        self.layout().update()
        
        # Ensure proper widget geometry
        self.banner_widget.updateGeometry()
        
        # Use timer to ensure layout is fully calculated before animation
        QTimer.singleShot(10, self._start_banner_animation)
        
    def _start_banner_animation(self):
        """Start banner animation after layout is ready"""
        self.banner_widget.play()

    def resizeEvent(self, event):
        """Responsive layout changes when window is resized/minimized"""
        super().resizeEvent(event)
        
        # Pass resize events to child widgets for responsive behavior
        if hasattr(self, 'vertical_menu'):
            self.vertical_menu.resizeEvent(event)
        
        if hasattr(self, 'nav_menu'):
            self.nav_menu.resizeEvent(event)
        
        # Force a repaint to ensure cosmic animation adapts to new size
        self.update()
