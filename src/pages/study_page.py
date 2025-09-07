"""
Study Page - Deck selection and study mode selection with card preview
Navigation Flow: Home → Deck Gallery → Study Mode Selection → Review Table
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QComboBox, QFrame, QScrollArea,
                               QGridLayout, QSizePolicy, QMessageBox, QStackedWidget)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter, QBrush, QColor, QPen
from src.widgets.button_widget import PrimaryButtonWidget as PrimaryButton, IconTextButtonWidget as IconTextButton
from src.ui import (StudyPageHeaderLayout, StudyDeckSelectionLayout)
from src.widgets.table_widget import ReviewTableWidget
from src.widgets.study_mode_menu_widget import StudyModeMenuWidget
import os
from src.core.paths import asset_path


class StudyPage(QWidget):
    """
    Study page with clear navigation flow:
    1. Deck Gallery (select deck to study)
    2. Study Mode Selection + Review Table (choose mode and preview cards)
    
    Navigation:
    - Back from Deck Gallery → Home
    - Back from Study Mode Selection → Deck Gallery
    """
    
    # View States
    VIEW_DECK_GALLERY = "deck_gallery"
    VIEW_STUDY_MODE = "study_mode"
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_view = self.VIEW_DECK_GALLERY
        self.current_deck_id = None
        self.current_deck_name = ""
        self.current_study_mode = "review"
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the study page UI"""
        self.setStyleSheet("""
            StudyPage {
                background: transparent;
                color: white;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Page header
        self.header = StudyPageHeaderLayout()
        self.header.back_requested.connect(self.handle_back_navigation)
        layout.addWidget(self.header)
        
        # Content area with stacked widgets for different views
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        # 1. Deck selection view
        self.deck_selection_widget = StudyDeckSelectionLayout()
        self.deck_selection_widget.deck_selected.connect(self.on_deck_selected)
        self.content_stack.addWidget(self.deck_selection_widget)
        
        # 2. Combined study view (mode menu + review table in one scrollable page)
        self.study_mode_menu = StudyModeMenuWidget()
        self.study_mode_menu.mode_selected.connect(self.on_study_mode_selected)

        self.study_combined_container = QWidget()
        self.study_combined_layout = QVBoxLayout(self.study_combined_container)
        self.study_combined_layout.setContentsMargins(0, 0, 0, 0)
        self.study_combined_layout.setSpacing(30)
        self.study_combined_layout.addWidget(self.study_mode_menu)

        # Review table section (between mode selection and study widget)
        self.review_table = ReviewTableWidget()
        self.study_combined_layout.addWidget(self.review_table)

        self.study_scroll = QScrollArea()
        self.study_scroll.setWidgetResizable(True)
        self.study_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.study_scroll.setWidget(self.study_combined_container)
        self.study_scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)

        self.content_stack.addWidget(self.study_scroll)
        
        layout.addWidget(self.content_stack)
        
        # Initialize with deck gallery
        self._show_deck_gallery()
        
    # ==================== NAVIGATION METHODS ====================
    
    def handle_back_navigation(self):
        """Context-aware back navigation based on current view"""
        if self.current_view == self.VIEW_STUDY_MODE:
            self._navigate_to_deck_gallery()
        elif self.current_view == self.VIEW_DECK_GALLERY:
            self._navigate_to_home()
    
    def _navigate_to_deck_gallery(self):
        """Go back to deck gallery"""
        self._show_deck_gallery()
    
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
    
    # ==================== VIEW METHODS ====================
    
    def _show_deck_gallery(self):
        """Show deck selection gallery"""
        self.current_view = self.VIEW_DECK_GALLERY
        self.content_stack.setCurrentWidget(self.deck_selection_widget)
        self.header.show_deck_selection()
        self._load_decks()
    
    def _show_study_mode_selection(self):
        """Show study mode selection with review table"""
        self.current_view = self.VIEW_STUDY_MODE
        self.content_stack.setCurrentWidget(self.study_scroll)
        self.header.show_deck_selection()
        # Scroll to top to show mode selection first
        self.study_scroll.verticalScrollBar().setValue(0)
    
    # ==================== DATA METHODS ====================
    
    def _load_decks(self):
        """Load and refresh available decks"""
        decks = self.db_manager.get_all_decks()
        # Add due count information for each deck
        for deck in decks:
            due_cards = self.db_manager.get_cards_due_for_review(deck['id'])
            deck['due_count'] = len(due_cards) if due_cards else 0
        self.deck_selection_widget.refresh_decks(decks)
        
    def _prepare_deck_data(self, deck_id):
        """Load and prepare deck data for study mode"""
        decks = self.db_manager.get_all_decks()
        selected_deck = next((d for d in decks if d['id'] == deck_id), None)
        
        if not selected_deck:
            return False
            
        self.current_deck_name = selected_deck['name']
        due_cards = self.db_manager.get_cards_due_for_review(deck_id)
        due_count = len(due_cards) if due_cards else 0
        
        # Set deck info in study mode selection
        # Update any header info as needed (title elsewhere already shows deck)
        
        # Populate review table with all cards
        cards = self.db_manager.get_cards_in_deck(deck_id)
        self.review_table.set_cards(cards)
        return True
    
    # ==================== EVENT HANDLERS ====================
    
    def on_deck_selected(self, deck_id):
        """Handle deck selection - transition to study mode selection"""
        self.current_deck_id = deck_id
        
        if self._prepare_deck_data(deck_id):
            self._show_study_mode_selection()
        
    def on_study_mode_selected(self, mode_type):
        """Handle study mode selection - scroll to review table"""
        self.current_study_mode = mode_type
        self._scroll_to_review_table()
        
    def _scroll_to_review_table(self):
        """Scroll to review table to show card preview"""
        if not self.current_deck_id:
            QMessageBox.warning(self, "No Deck Selected", "Please select a deck first.")
            return
            
        # Ensure we're showing the study mode view
        self.content_stack.setCurrentWidget(self.study_scroll)
        
        # Smooth scroll to review table
        try:
            self.study_scroll.ensureWidgetVisible(self.review_table, 0, 40)
        except Exception:
            self.study_scroll.verticalScrollBar().setValue(self.review_table.y())
    
    # ==================== PUBLIC API ====================
    
    def load_decks(self):
        """Public API: Load and refresh decks (called by main window)"""
        self._load_decks()
        
    def set_current_deck(self, deck_id):
        """Public API: Set current deck and show study mode selection"""
        self.current_deck_id = deck_id
        
        if self._prepare_deck_data(deck_id):
            self._show_study_mode_selection()

