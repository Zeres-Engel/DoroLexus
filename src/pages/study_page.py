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
from src.widgets.deck_gallery_widget import DeckGalleryWidget, DeckGalleryMode
from src.widgets.table_widget import ReviewTableWidget
from src.widgets.nav_bar_widget import NavBarWidget
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
        
        # Top navigation bar
        self.navbar = NavBarWidget("Study Mode", show_back_button=False)
        self.navbar.back_requested.connect(self.handle_back_navigation)
        self.navbar.home_requested.connect(self._navigate_to_home)
        layout.addWidget(self.navbar)
        
        # Content area with stacked widgets for different views
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        # 1. Deck selection view
        self.deck_gallery = DeckGalleryWidget(
            mode=DeckGalleryMode.STUDY,
            title="⚔️ Choose Your Weapon ⚔️",
            show_title=True
        )
        self.deck_gallery.deck_selected.connect(self.on_deck_selection_changed)
        self.deck_gallery.deck_preview.connect(self.on_deck_selected)
        self.deck_gallery.selection_changed.connect(self.on_selection_changed)
        self.content_stack.addWidget(self.deck_gallery)
        
        # 2. Card preview view (just review table)
        self.review_table = ReviewTableWidget()
        self.content_stack.addWidget(self.review_table)
        
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
        self.content_stack.setCurrentWidget(self.deck_gallery)
        self.navbar.set_title("Study Decks")
        # Show back button so user can return to Home from deck gallery
        self.navbar.show_back_button()
        # Load decks and ensure proper state
        self._load_decks()
    
    def _show_card_preview(self):
        """Show card preview table"""
        self.current_view = self.VIEW_STUDY_MODE
        self.content_stack.setCurrentWidget(self.review_table)
        self.navbar.set_title(f"Preview: {self.current_deck_name}")
        self.navbar.show_back_button()
    
    # ==================== DATA METHODS ====================
    
    def _load_decks(self):
        """Load and refresh available decks"""
        decks = self.db_manager.get_all_decks()
        # Add due count information for each deck
        for deck in decks:
            due_cards = self.db_manager.get_cards_due_for_review(deck['id'])
            deck['due_count'] = len(due_cards) if due_cards else 0
        self.deck_gallery.refresh_decks(decks)
        
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
        """Handle deck preview request - show card preview"""
        self.current_deck_id = deck_id
        
        if self._prepare_deck_data(deck_id):
            self._show_card_preview()
    
    def on_deck_selection_changed(self, deck_id):
        """Handle deck selection/deselection for multi-select mode"""
        # This is for toggling selections, not preview
        pass
    
    def on_selection_changed(self, selected_deck_ids):
        """Handle when the selection list changes"""
        # Update any UI that depends on selection count
        # Could show/hide study mode menu based on selection count
        pass
    
    def on_study_mode_selected(self, mode_type, selected_deck_ids):
        """Handle study mode selection with multiple decks"""
        # TODO: Implement actual study mode launching with selected decks
        from PySide6.QtWidgets import QMessageBox
        deck_names = []
        for deck_id in selected_deck_ids:
            decks = self.db_manager.get_all_decks()
            deck = next((d for d in decks if d['id'] == deck_id), None)
            if deck:
                deck_names.append(deck['name'])
        
        deck_list = ", ".join(deck_names)
        QMessageBox.information(
            self,
            "Study Mode Selected",
            f"Starting {mode_type} study mode with decks:\n{deck_list}\n\n"
            f"(Study implementation coming soon...)"
        )
    
    # ==================== PUBLIC API ====================
    
    def load_decks(self):
        """Public API: Load and refresh decks (called by main window)"""
        # Reset to deck gallery view when loading
        self._show_deck_gallery()
        self._load_decks()
    
    def reset_to_initial_state(self):
        """Reset the study page to its initial state"""
        self.current_view = self.VIEW_DECK_GALLERY
        self.current_deck_id = None
        self.current_deck_name = ""
        self.current_study_mode = "review"
        # Clear any selections in the deck gallery
        self.deck_gallery.clear_selection()
        self._show_deck_gallery()
        
    def set_current_deck(self, deck_id):
        """Public API: Set current deck and show card preview"""
        self.current_deck_id = deck_id
        
        if self._prepare_deck_data(deck_id):
            self._show_card_preview()

