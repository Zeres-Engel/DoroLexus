"""
Deck management widget for creating, editing, and organizing flashcard decks
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QLineEdit, QTextEdit, QListWidget, 
                               QListWidgetItem, QMessageBox, QDialog, QDialogButtonBox,
                               QFormLayout, QGroupBox, QSplitter)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon
import os
from src.core.paths import asset_path

class DeckDialog(QDialog):
    """Dialog for creating/editing decks"""
    
    def __init__(self, deck_data=None, parent=None):
        super().__init__(parent)
        self.deck_data = deck_data
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        self.setWindowTitle("Edit Deck" if self.deck_data else "Create New Deck")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Deck name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter deck name...")
        if self.deck_data:
            self.name_edit.setText(self.deck_data.get('name', ''))
        form_layout.addRow("Name:", self.name_edit)
        
        # Deck description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter deck description (optional)...")
        self.description_edit.setMaximumHeight(100)
        if self.deck_data:
            self.description_edit.setText(self.deck_data.get('description', ''))
        form_layout.addRow("Description:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def get_deck_data(self):
        """Get the deck data from the form"""
        return {
            'name': self.name_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip()
        }

class CardDialog(QDialog):
    """Dialog for creating/editing cards"""
    
    def __init__(self, card_data=None, parent=None):
        super().__init__(parent)
        self.card_data = card_data
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        self.setWindowTitle("Edit Card" if self.card_data else "Create New Card")
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Front text
        self.front_edit = QTextEdit()
        self.front_edit.setPlaceholderText("Enter the question or front of the card...")
        self.front_edit.setMaximumHeight(120)
        if self.card_data:
            self.front_edit.setText(self.card_data.get('front', ''))
        form_layout.addRow("Front:", self.front_edit)
        
        # Back text
        self.back_edit = QTextEdit()
        self.back_edit.setPlaceholderText("Enter the answer or back of the card...")
        self.back_edit.setMaximumHeight(120)
        if self.card_data:
            self.back_edit.setText(self.card_data.get('back', ''))
        form_layout.addRow("Back:", self.back_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def get_card_data(self):
        """Get the card data from the form"""
        return {
            'front': self.front_edit.toPlainText().strip(),
            'back': self.back_edit.toPlainText().strip()
        }

class DeckManager(QWidget):
    """Widget for managing flashcard decks and cards"""
    
    # Signals
    deck_selected = Signal(int)  # Emitted when a deck is selected for study
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_deck_id = None
        self.init_ui()
        self.refresh_decks()
        
    def init_ui(self):
        """Initialize the deck manager UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        # Deck header with tomato icon
        title_label = QLabel("Deck Manager")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2E7D32;")

        tomato_icon_path = asset_path('data', 'images', 'svg', 'tomato-svgrepo-com.svg')
        if tomato_icon_path:
            self.setWindowIcon(QIcon(tomato_icon_path))
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Create deck button
        self.create_deck_btn = QPushButton("+ New Deck")
        self.create_deck_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.create_deck_btn.clicked.connect(self.create_deck)
        header_layout.addWidget(self.create_deck_btn)
        
        layout.addLayout(header_layout)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Deck list
        self.deck_list = QListWidget()
        self.deck_list.setMaximumWidth(300)
        self.deck_list.itemClicked.connect(self.on_deck_selected)
        splitter.addWidget(self.deck_list)
        
        # Right side - Card management
        self.card_widget = self.create_card_management_widget()
        splitter.addWidget(self.card_widget)
        
        # Set splitter proportions
        splitter.setSizes([300, 700])
        layout.addWidget(splitter)
        
    def create_card_management_widget(self):
        """Create the card management widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Card management header
        card_header_layout = QHBoxLayout()
        self.card_title_label = QLabel("Select a deck to manage cards")
        card_font = QFont()
        card_font.setPointSize(16)
        card_font.setBold(True)
        self.card_title_label.setFont(card_font)
        self.card_title_label.setStyleSheet("color: #495057;")
        
        card_header_layout.addWidget(self.card_title_label)
        card_header_layout.addStretch()
        
        # Add card button
        self.add_card_btn = QPushButton("+ Add Card")
        self.add_card_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.add_card_btn.clicked.connect(self.add_card)
        self.add_card_btn.setVisible(False)
        card_header_layout.addWidget(self.add_card_btn)
        
        layout.addLayout(card_header_layout)
        
        # Card list
        self.card_list = QListWidget()
        self.card_list.itemDoubleClicked.connect(self.edit_card)
        layout.addWidget(self.card_list)
        
        # Card actions
        card_actions_layout = QHBoxLayout()
        
        self.edit_card_btn = QPushButton("Edit Card")
        self.edit_card_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #212529;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        self.edit_card_btn.clicked.connect(self.edit_card)
        self.edit_card_btn.setVisible(False)
        card_actions_layout.addWidget(self.edit_card_btn)
        
        self.delete_card_btn = QPushButton("Delete Card")
        self.delete_card_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.delete_card_btn.clicked.connect(self.delete_card)
        self.delete_card_btn.setVisible(False)
        card_actions_layout.addWidget(self.delete_card_btn)
        
        # Study deck button
        self.study_deck_btn = QPushButton("Study This Deck")
        self.study_deck_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
        """)
        self.study_deck_btn.clicked.connect(self.study_deck)
        self.study_deck_btn.setVisible(False)
        card_actions_layout.addWidget(self.study_deck_btn)
        
        card_actions_layout.addStretch()
        layout.addLayout(card_actions_layout)
        
        return widget
        
    def refresh_decks(self):
        """Refresh the deck list"""
        self.deck_list.clear()
        decks = self.db_manager.get_all_decks()
        
        for deck in decks:
            item_text = f"{deck['name']}\n({deck['card_count']} cards)"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, deck['id'])
            self.deck_list.addItem(item)
            
    def create_deck(self):
        """Create a new deck"""
        dialog = DeckDialog(parent=self)
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
                
    def on_deck_selected(self, item):
        """Handle deck selection"""
        self.current_deck_id = item.data(Qt.UserRole)
        deck = self.db_manager.get_deck(self.current_deck_id)
        
        if deck:
            self.card_title_label.setText(f"Cards in '{deck['name']}'")
            self.add_card_btn.setVisible(True)
            self.study_deck_btn.setVisible(True)
            self.refresh_cards()
            
    def refresh_cards(self):
        """Refresh the card list for the current deck"""
        if not self.current_deck_id:
            return
            
        self.card_list.clear()
        cards = self.db_manager.get_cards_in_deck(self.current_deck_id)
        
        for card in cards:
            # Truncate long text for display
            front_text = card['front'][:50] + "..." if len(card['front']) > 50 else card['front']
            back_text = card['back'][:50] + "..." if len(card['back']) > 50 else card['back']
            
            item_text = f"Q: {front_text}\nA: {back_text}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, card['id'])
            self.card_list.addItem(item)
            
        # Show/hide card action buttons
        has_cards = len(cards) > 0
        self.edit_card_btn.setVisible(has_cards)
        self.delete_card_btn.setVisible(has_cards)
        
    def add_card(self):
        """Add a new card to the current deck"""
        if not self.current_deck_id:
            return
            
        dialog = CardDialog(parent=self)
        if dialog.exec() == QDialog.Accepted:
            card_data = dialog.get_card_data()
            if not card_data['front'] or not card_data['back']:
                QMessageBox.warning(self, "Invalid Input", "Both front and back text are required.")
                return
                
            self.db_manager.create_card(self.current_deck_id, card_data['front'], card_data['back'])
            self.refresh_cards()
            QMessageBox.information(self, "Success", "Card added successfully!")
            
    def edit_card(self):
        """Edit the selected card"""
        current_item = self.card_list.currentItem()
        if not current_item:
            return
            
        card_id = current_item.data(Qt.UserRole)
        cards = self.db_manager.get_cards_in_deck(self.current_deck_id)
        card_data = next((card for card in cards if card['id'] == card_id), None)
        
        if not card_data:
            return
            
        dialog = CardDialog(card_data, parent=self)
        if dialog.exec() == QDialog.Accepted:
            new_data = dialog.get_card_data()
            if not new_data['front'] or not new_data['back']:
                QMessageBox.warning(self, "Invalid Input", "Both front and back text are required.")
                return
                
            self.db_manager.update_card(card_id, new_data['front'], new_data['back'])
            self.refresh_cards()
            QMessageBox.information(self, "Success", "Card updated successfully!")
            
    def delete_card(self):
        """Delete the selected card"""
        current_item = self.card_list.currentItem()
        if not current_item:
            return
            
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure you want to delete this card?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            card_id = current_item.data(Qt.UserRole)
            self.db_manager.delete_card(card_id)
            self.refresh_cards()
            QMessageBox.information(self, "Success", "Card deleted successfully!")
            
    def study_deck(self):
        """Start studying the current deck"""
        if self.current_deck_id:
            self.deck_selected.emit(self.current_deck_id)
