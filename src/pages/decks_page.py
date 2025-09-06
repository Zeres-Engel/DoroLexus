"""
Modern deck management page with card-like interface and dark theme
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


# Card and dialog classes are now imported from src.ui.layout_components


class DecksPage(QWidget):
    """Modern deck management page with card interface"""
    
    deck_selected = Signal(int)  # For studying a deck
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.init_ui()
        
    def init_ui(self):
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
        self.card_management.back_to_decks.connect(self.show_deck_gallery)
        self.card_management.add_card.connect(self.add_card)
        self.card_management.edit_card.connect(self.edit_card)
        self.card_management.delete_card.connect(self.delete_card)
        self.stacked_widget.addWidget(self.card_management)
        
        layout.addWidget(self.stacked_widget)
        
        # Initially show deck gallery
        self.show_deck_gallery()
        
    def refresh_decks(self):
        """Refresh the deck gallery"""
        decks = self.db_manager.get_all_decks()
        self.deck_gallery.refresh_decks(decks)
        
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
                self.refresh_decks()
                QMessageBox.information(self, "Success", "Deck created successfully!")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
                
    def edit_deck(self, deck_id):
        """Edit deck or manage its cards"""
        deck = self.db_manager.get_deck(deck_id)
        if deck:
            self.card_management.set_deck(deck_id, deck['name'])
            self.card_management.refresh_cards(self.db_manager.get_cards_in_deck(deck_id))
            self.stacked_widget.setCurrentWidget(self.card_management)
            
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
            self.refresh_decks()
            QMessageBox.information(self, "Success", "Deck deleted successfully!")
            
    def show_deck_gallery(self):
        """Show the deck gallery view"""
        self.stacked_widget.setCurrentWidget(self.deck_gallery)
        self.refresh_decks()
