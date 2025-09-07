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


# Removed simple overlay - using CosmicParticleSystem instead


class DoroLexusApp(QMainWindow):
    """Main application window with pages structure"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_deck = None
        self.init_ui()
        self.setup_connections()
        # Create cosmic particle system as an overlay on the main window
        self._cosmic_particles = CosmicParticleSystem(self)
        self._cosmic_particles.setGeometry(0, 0, self.width(), self.height())
        self._cosmic_particles.setVisible(True)
        self._cosmic_particles.show()
        # Render above content but ignore mouse events (set in widget)
        self._cosmic_particles.raise_()
        # Force initial paint
        self._cosmic_particles.update()

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

        # No global header; pages render their own nav bars
        self.header_widget = None

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        # Make sure content is above background
        self.stacked_widget.raise_()

        # Initialize pages
        self.init_pages()
        
        # Start with home page
        self.stacked_widget.setCurrentWidget(self.home_page)
        
        # Start the home page animation after a short delay to ensure proper initialization
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self.home_page.show_with_animation)
        
        # Show logo popup on startup
        if icon_path:
            show_logo_popup(self, icon_path, size=96, lifespan_ms=900)

    # Removed global header creation

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
        # Refresh cosmic particles when showing home
        if hasattr(self, '_cosmic_particles') and self._cosmic_particles:
            self._cosmic_particles.show()
            self._cosmic_particles.raise_()
            self._cosmic_particles.update()
        self.home_page.show_with_animation()

    def show_study(self):
        """Show the study page"""
        decks = self.db_manager.get_all_decks()
        if not decks:
            QMessageBox.information(self, "No Decks", "Please create a deck first before studying.")
            return
        
        # Pause cosmic particles during navigation for smoother transition
        if hasattr(self, '_cosmic_particles') and self._cosmic_particles:
            self._cosmic_particles.pause_animation()
        
        # Reset study page to initial state for clean navigation
        self.study_page.reset_to_initial_state()
        self.stacked_widget.setCurrentWidget(self.study_page)
        
        # Resume cosmic particles after a short delay
        from PySide6.QtCore import QTimer
        QTimer.singleShot(200, self._resume_cosmic_particles)

    def show_decks(self):
        """Show the decks page"""
        self.decks_page.refresh_decks()
        self.stacked_widget.setCurrentWidget(self.decks_page)

    def show_timer(self):
        """Show the timer page"""
        self.stacked_widget.setCurrentWidget(self.timer_page)

    def show_stats(self):
        """Show the stats page"""
        self.stats_page.refresh_stats()
        self.stacked_widget.setCurrentWidget(self.stats_page)
    
    def _resume_cosmic_particles(self):
        """Resume cosmic particle animation"""
        if hasattr(self, '_cosmic_particles') and self._cosmic_particles:
            self._cosmic_particles.resume_animation()
            self._cosmic_particles.raise_()
            self._cosmic_particles.update()

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
        
    def showEvent(self, event):
        """Handle window show event"""
        super().showEvent(event)
        # Ensure cosmic particles are visible when window is shown
        if hasattr(self, '_cosmic_particles') and self._cosmic_particles:
            self._cosmic_particles.show()
            self._cosmic_particles.raise_()
            self._cosmic_particles.update()
    
    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        # Keep cosmic particles covering the full area but behind content
        if hasattr(self, '_cosmic_particles') and self._cosmic_particles:
            self._cosmic_particles.setGeometry(0, 0, self.width(), self.height())
            # Do not recreate stars on resize; just ensure overlay stays on top
            self._cosmic_particles.raise_()
            self._cosmic_particles.update()  # Force repaint