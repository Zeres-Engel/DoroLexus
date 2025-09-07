"""
Refactored main window using pages structure
"""

import os
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon

from src.core import DatabaseManager
from src.core.paths import asset_path
from src.pages import HomePage, StudyPage, DecksPage, TimerPage, StatsPage
from src.animation import AnimatedIconLabel, show_logo_popup, CosmicParticleSystem
from src.widgets.button_widget import PrimaryButtonWidget as PrimaryButton


# Removed simple overlay - using CosmicParticleSystem instead


class DoroLexusApp(QMainWindow):
    """Main application window with pages structure"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_deck = None
        self.init_ui()
        self.setup_connections()
        # Create cosmic particle system on top of all content (after UI is built)
        self._cosmic_particles = CosmicParticleSystem(self.centralWidget())
        self._cosmic_particles.setGeometry(0, 0, self.width(), self.height())
        self._cosmic_particles.show()
        self._cosmic_particles.raise_()

    def init_ui(self):
        """Initialize the main UI"""
        self.setWindowTitle("DoroLexus - Vocabulary Flashcard App")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)

        # Set window icon
        icon_path = asset_path("data", "images", "svg", "doro_lexus logo.svg")
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        # Window properties - removed translucent background to fix overlay issue
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setWindowOpacity(0.96)
        self.apply_theme()

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Overlay canvas will render above all content
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        self.header_widget = self.create_header(main_layout)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        # Make sure content is above background
        self.stacked_widget.raise_()

        # Initialize pages
        self.init_pages()
        
        # Start with home page and hide header for home
        self.stacked_widget.setCurrentWidget(self.home_page)
        if self.header_widget:
            self.header_widget.setVisible(False)
        
        # Start the home page animation after a short delay to ensure proper initialization
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self.home_page.show_with_animation)
        
        # Show logo popup on startup
        if icon_path:
            show_logo_popup(self, icon_path, size=96, lifespan_ms=900)

    def create_header(self, layout):
        """Create the header section"""
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("""
            QWidget {
                background: transparent;
                border: none;
            }
        """)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(15)

        # Logo
        logo_path = asset_path("data", "images", "svg", "doro_lexus logo.svg")
        if logo_path:
            logo_widget = AnimatedIconLabel(logo_path, size=48)
            logo_widget.start()
            logo_widget.clicked.connect(lambda: show_logo_popup(self, logo_path, size=120, lifespan_ms=1000))
            header_layout.addWidget(logo_widget)

        # Title
        title_label = QLabel("DoroLexus")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_font.setFamily("Cascadia Code")
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                background: transparent;
                margin: 10px 0px 10px 10px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Back button
        self.back_button = PrimaryButton("← Back")
        self.back_button.setFixedSize(100, 40)
        self.back_button.clicked.connect(self.on_back_clicked)
        self.back_button.setVisible(False)
        header_layout.addWidget(self.back_button)

        layout.addWidget(header_widget)
        return header_widget

    def init_pages(self):
        """Initialize all pages"""
        # Home page
        self.home_page = HomePage()
        self.stacked_widget.addWidget(self.home_page)

        # Study page
        self.study_page = StudyPage(self.db_manager)
        self.stacked_widget.addWidget(self.study_page)

        # Decks page
        self.decks_page = DecksPage(self.db_manager)
        self.stacked_widget.addWidget(self.decks_page)

        # Timer page
        self.timer_page = TimerPage()
        self.stacked_widget.addWidget(self.timer_page)

        # Stats page
        self.stats_page = StatsPage(self.db_manager)
        self.stacked_widget.addWidget(self.stats_page)

    def setup_connections(self):
        """Setup signal connections between pages"""
        # Home page connections
        self.home_page.study_requested.connect(self.show_study)
        self.home_page.decks_requested.connect(self.show_decks)
        self.home_page.timer_requested.connect(self.show_timer)
        self.home_page.stats_requested.connect(self.show_stats)
        self.home_page.exit_requested.connect(self.close)
        
        # Decks page connections
        self.decks_page.deck_selected.connect(self.on_deck_selected)

    def apply_theme(self):
        """Apply the dark theme with transparent background for animated background"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: transparent;
                color: #E0E0E0;
            }
            QWidget {
                background-color: transparent;
                color: #E0E0E0;
            }
            QLabel {
                color: #E0E0E0;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1F6FEB;
                color: #FFFFFF;
                border: 1px solid #2D333B;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2A7FFF;
            }
            QPushButton:pressed {
                background-color: #1964D0;
            }
            QFrame {
                background-color: #1E1E1E;
                border: 1px solid #2D2D2D;
                border-radius: 10px;
            }
            QComboBox, QLineEdit, QTextEdit {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #2D2D2D;
                border-radius: 6px;
                padding: 6px 10px;
            }
            QListWidget {
                background-color: #151515;
                border: 1px solid #2D2D2D;
            }
            QProgressBar {
                border: 1px solid #2D2D2D;
                border-radius: 6px;
                text-align: center;
                color: #E0E0E0;
                background-color: #1E1E1E;
            }
            QProgressBar::chunk {
                background-color: #2EA043;
            }
        """)

    def show_home(self):
        """Show the home page"""
        self.stacked_widget.setCurrentWidget(self.home_page)
        self.back_button.setVisible(False)
        if self.header_widget:
            self.header_widget.setVisible(False)
        self.home_page.show_with_animation()

    def show_study(self):
        """Show the study page"""
        decks = self.db_manager.get_all_decks()
        if not decks:
            QMessageBox.information(self, "No Decks", "Please create a deck first before studying.")
            return
            
        self.study_page.load_decks()
        self.stacked_widget.setCurrentWidget(self.study_page)
        self.back_button.setVisible(True)
        if self.header_widget:
            self.header_widget.setVisible(True)

    def show_decks(self):
        """Show the decks page"""
        self.decks_page.refresh_decks()
        self.stacked_widget.setCurrentWidget(self.decks_page)
        self.back_button.setVisible(True)
        if self.header_widget:
            self.header_widget.setVisible(True)

    def show_timer(self):
        """Show the timer page"""
        self.stacked_widget.setCurrentWidget(self.timer_page)
        self.back_button.setVisible(True)
        if self.header_widget:
            self.header_widget.setVisible(True)

    def show_stats(self):
        """Show the stats page"""
        self.stats_page.refresh_stats()
        self.stacked_widget.setCurrentWidget(self.stats_page)
        self.back_button.setVisible(True)
        if self.header_widget:
            self.header_widget.setVisible(True)

    def on_deck_selected(self, deck_id):
        """Handle deck selection"""
        self.current_deck = deck_id
        self.study_page.set_current_deck(deck_id)

    def on_back_clicked(self):
        """Context-aware back navigation.
        If current page provides a back handler, delegate to it. Otherwise, go home.
        """
        current = self.stacked_widget.currentWidget()
        try:
            if current and hasattr(current, 'handle_back_navigation') and callable(getattr(current, 'handle_back_navigation')):
                current.handle_back_navigation()
                return
        except Exception:
            pass
        self.show_home()
        
    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        # Keep cosmic particles covering the full area and on top
        if hasattr(self, '_cosmic_particles') and self._cosmic_particles:
            self._cosmic_particles.setGeometry(0, 0, self.width(), self.height())
            self._cosmic_particles.raise_()