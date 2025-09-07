"""
Decks Management Page - Deck gallery and card management
Navigation Flow: Home → Deck Gallery → Card Management
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QScrollArea, QGridLayout, 
                               QDialog, QLineEdit, QTextEdit, QDialogButtonBox,
                               QFormLayout, QListWidget, QListWidgetItem, QMessageBox,
                               QSplitter, QStackedWidget)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter, QBrush, QColor, QPen
from src.widgets.button_widget import PrimaryButtonWidget as PrimaryButton, DangerButtonWidget as DangerButton, IconTextButtonWidget as IconTextButton
from src.ui import (DeckGalleryLayout, CardManagementLayout, DeckDialogLayout, CardDialogLayout, 
                   DecksPageHeaderLayout)
import os
from src.core.paths import asset_path


class DecksPage(QWidget):
    """
    Deck management page with clear navigation flow:
    1. Deck Gallery (create, edit, delete decks)
    2. Card Management (manage cards within a specific deck)
    
    Navigation:
    - Back from Deck Gallery → Home
    - Back from Card Management → Deck Gallery
    """
    
    # View States
    VIEW_DECK_GALLERY = "deck_gallery"
    VIEW_CARD_MANAGEMENT = "card_management"
    
    deck_selected = Signal(int)  # For studying a deck
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_view = self.VIEW_DECK_GALLERY
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the decks page UI"""
        self.setStyleSheet("""
            DecksPage {
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
        self.header = DecksPageHeaderLayout()
        self.header.back_requested.connect(self.handle_back_navigation)
        layout.addWidget(self.header)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        
        # Deck gallery view
        self.deck_gallery = DeckGalleryLayout()
        self.deck_gallery.deck_selected.connect(self.deck_selected.emit)
        self.deck_gallery.edit_deck.connect(self.edit_deck)
        self.deck_gallery.delete_deck.connect(self.delete_deck)
        self.deck_gallery.create_deck.connect(self.create_deck)
        self.stacked_widget.addWidget(self.deck_gallery)
        
        # Card management view
        self.card_management = CardManagementLayout()
        self.card_management.add_card.connect(self.add_card)
        self.card_management.edit_card.connect(self.edit_card)
        self.card_management.delete_card.connect(self.delete_card)
        self.stacked_widget.addWidget(self.card_management)
        
        layout.addWidget(self.stacked_widget)
        
        # Initialize with deck gallery
        self._show_deck_gallery()
        
    # ==================== NAVIGATION METHODS ====================
    
    def handle_back_navigation(self):
        """Context-aware back navigation based on current view"""
        if self.current_view == self.VIEW_CARD_MANAGEMENT:
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
        """Show deck gallery view"""
        self.current_view = self.VIEW_DECK_GALLERY
        self.stacked_widget.setCurrentWidget(self.deck_gallery)
        self._refresh_decks()
    
    def _show_card_management(self, deck_id, deck_name):
        """Show card management view for specific deck"""
        self.current_view = self.VIEW_CARD_MANAGEMENT
        self.card_management.set_deck(deck_id, deck_name)
        self.card_management.refresh_cards(self.db_manager.get_cards_in_deck(deck_id))
        self.stacked_widget.setCurrentWidget(self.card_management)
    
    # ==================== DATA METHODS ====================
    
    def _refresh_decks(self):
        """Load and refresh deck gallery"""
        decks = self.db_manager.get_all_decks()
        self.deck_gallery.refresh_decks(decks)
        
    # ==================== EVENT HANDLERS ====================
    
    def create_deck(self):
        """Create a new deck"""
        dialog = DeckDialogLayout(parent=self)
        if dialog.exec() == QDialog.Accepted:
            deck_data = dialog.get_deck_data()
            if not deck_data['name']:
                QMessageBox.warning(self, "Invalid Input", "Deck name cannot be empty.")
                return
                
            try:
                self.db_manager.create_deck(deck_data['name'], deck_data['description'])
                self._refresh_decks()
                QMessageBox.information(self, "Success", "Deck created successfully!")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
                
    def edit_deck(self, deck_id):
        """Edit deck - navigate to card management"""
        deck = self.db_manager.get_deck(deck_id)
        if deck:
            self._show_card_management(deck_id, deck['name'])
            
    def add_card(self):
        """Add a new card"""
        dialog = CardDialogLayout(parent=self)
        if dialog.exec() == QDialog.Accepted:
            card_data = dialog.get_card_data()
            if not card_data['front'] or not card_data['back']:
                QMessageBox.warning(self, "Invalid Input", "Both front and back text are required.")
                return
                
            self.db_manager.create_card(self.card_management.current_deck_id, card_data['front'], card_data['back'])
            self.card_management.refresh_cards(self.db_manager.get_cards_in_deck(self.card_management.current_deck_id))
            QMessageBox.information(self, "Success", "Card added successfully!")
            
    def edit_card(self, card_id=None):
        """Edit the selected card"""
        if card_id is None:
            card_id = self.card_management.get_selected_card_id()
        if not card_id:
            return
            
        cards = self.db_manager.get_cards_in_deck(self.card_management.current_deck_id)
        card_data = next((card for card in cards if card['id'] == card_id), None)
        
        if not card_data:
            return
            
        dialog = CardDialogLayout(card_data, parent=self)
        if dialog.exec() == QDialog.Accepted:
            new_data = dialog.get_card_data()
            if not new_data['front'] or not new_data['back']:
                QMessageBox.warning(self, "Invalid Input", "Both front and back text are required.")
                return
                
            self.db_manager.update_card(card_id, new_data['front'], new_data['back'])
            self.card_management.refresh_cards(self.db_manager.get_cards_in_deck(self.card_management.current_deck_id))
            QMessageBox.information(self, "Success", "Card updated successfully!")
            
    def delete_card(self, card_id=None):
        """Delete the selected card"""
        if card_id is None:
            card_id = self.card_management.get_selected_card_id()
        if not card_id:
            return
            
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this card?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.db_manager.delete_card(card_id)
            self.card_management.refresh_cards(self.db_manager.get_cards_in_deck(self.card_management.current_deck_id))
            QMessageBox.information(self, "Success", "Card deleted successfully!")
            
    def delete_deck(self, deck_id):
        """Delete a deck"""
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this deck? All cards will be lost!",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.db_manager.delete_deck(deck_id)
            self._refresh_decks()
            QMessageBox.information(self, "Success", "Deck deleted successfully!")
    
    # ==================== PUBLIC API ====================
    
    def refresh_decks(self):
        """Public API: Refresh deck gallery (called by main window)"""
        self._refresh_decks()
