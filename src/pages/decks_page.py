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
from src.ui.buttons import PrimaryButton, DangerButton, IconTextButton
import os
from src.core.paths import asset_path


class CreateDeckCard(QFrame):
    """Special card for creating new decks"""
    
    create_deck = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the create deck card UI"""
        self.setFixedSize(200, 120)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            CreateDeckCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 200, 100, 0.3),
                    stop:1 rgba(60, 160, 60, 0.3));
                border: 2px dashed rgba(100, 200, 100, 0.6);
                border-radius: 12px;
            }
            CreateDeckCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(120, 220, 120, 0.4),
                    stop:1 rgba(80, 180, 80, 0.4));
                border: 2px dashed rgba(120, 220, 120, 0.8);
            }
        """)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Plus icon (using text for now)
        plus_label = QLabel("+")
        plus_label.setAlignment(Qt.AlignCenter)
        plus_label.setStyleSheet("""
            QLabel {
                color: rgba(100, 200, 100, 0.8);
                font-size: 36px;
                font-weight: bold;
                background: transparent;
            }
        """)
        layout.addWidget(plus_label)
        
        # Create text
        create_label = QLabel("New Deck")
        create_label.setAlignment(Qt.AlignCenter)
        create_label.setStyleSheet("""
            QLabel {
                color: rgba(100, 200, 100, 0.9);
                font-size: 14px;
                font-weight: bold;
                background: transparent;
            }
        """)
        layout.addWidget(create_label)
        
    def mousePressEvent(self, event):
        """Handle mouse click to create deck"""
        if event.button() == Qt.LeftButton:
            self.create_deck.emit()
        super().mousePressEvent(event)


class DeckManagementCard(QFrame):
    """Individual deck card for management"""
    
    deck_selected = Signal(int)  # For studying
    edit_deck = Signal(int)      # For editing cards
    delete_deck = Signal(int)
    
    def __init__(self, deck_data, parent=None):
        super().__init__(parent)
        self.deck_id = deck_data['id']
        self.deck_name = deck_data['name']
        self.card_count = deck_data['card_count']
        self.description = deck_data.get('description', '')
        self.init_ui()
        
    def init_ui(self):
        """Initialize the deck management card UI"""
        self.setFixedSize(200, 120)
        self.setStyleSheet("""
            DeckManagementCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 60, 60, 0.9),
                    stop:1 rgba(40, 40, 40, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            DeckManagementCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(80, 80, 80, 0.9),
                    stop:1 rgba(60, 60, 60, 0.9));
                border: 2px solid rgba(100, 200, 255, 0.5);
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        # Deck name
        name_label = QLabel(self.deck_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
            }
        """)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Card count
        count_label = QLabel(f"{self.card_count} cards")
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 11px;
                background: transparent;
            }
        """)
        layout.addWidget(count_label)
        
        layout.addStretch()
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(4)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedSize(35, 20)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffa726;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff9800;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_deck.emit(self.deck_id))
        actions_layout.addWidget(edit_btn)
        
        # Study button
        study_btn = QPushButton("Study")
        study_btn.setFixedSize(35, 20)
        study_btn.setStyleSheet("""
            QPushButton {
                background-color: #64c8ff;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a9eff;
            }
        """)
        study_btn.clicked.connect(lambda: self.deck_selected.emit(self.deck_id))
        actions_layout.addWidget(study_btn)
        
        # Delete button
        delete_btn = QPushButton("×")
        delete_btn.setFixedSize(20, 20)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6b6b;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_deck.emit(self.deck_id))
        actions_layout.addWidget(delete_btn)
        
        layout.addLayout(actions_layout)
        
    def mousePressEvent(self, event):
        """Handle mouse click on deck card to edit"""
        if event.button() == Qt.LeftButton:
            self.edit_deck.emit(self.deck_id)
        super().mousePressEvent(event)


class DeckDialog(QDialog):
    """Modern dialog for creating/editing decks"""
    
    def __init__(self, deck_data=None, parent=None):
        super().__init__(parent)
        self.deck_data = deck_data
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        self.setWindowTitle("Edit Deck" if self.deck_data else "Create New Deck")
        self.setModal(True)
        self.resize(450, 300)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: white;
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QLineEdit, QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #64c8ff;
            }
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Edit Deck Details" if self.deck_data else "Create New Deck")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #64c8ff;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Deck name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter deck name...")
        if self.deck_data:
            self.name_edit.setText(self.deck_data.get('name', ''))
        form_layout.addRow("Deck Name:", self.name_edit)
        
        # Deck description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter deck description (optional)...")
        self.description_edit.setMaximumHeight(100)
        if self.deck_data:
            self.description_edit.setText(self.deck_data.get('description', ''))
        form_layout.addRow("Description:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Deck")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #64c8ff;
                color: white;
            }
            QPushButton:hover {
                background-color: #4a9eff;
            }
        """)
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
    def get_deck_data(self):
        """Get the deck data from the form"""
        return {
            'name': self.name_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip()
        }


class CardManagementWidget(QWidget):
    """Widget for managing cards within a deck"""
    
    back_to_decks = Signal()
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_deck_id = None
        self.current_deck_name = ""
        self.init_ui()
        
    def init_ui(self):
        """Initialize card management UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: white;
            }
            QListWidget {
                background-color: #2d2d2d;
                border: 2px solid #444;
                border-radius: 8px;
                color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #444;
            }
            QListWidget::item:selected {
                background-color: #64c8ff;
            }
            QListWidget::item:hover {
                background-color: #444;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Back button
        back_btn = PrimaryButton("← Back to Decks")
        back_btn.clicked.connect(self.back_to_decks.emit)
        header_layout.addWidget(back_btn)
        
        header_layout.addStretch()
        
        # Deck title
        self.deck_title = QLabel()
        self.deck_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
            }
        """)
        header_layout.addWidget(self.deck_title)
        
        header_layout.addStretch()
        
        # Add card button
        add_card_btn = PrimaryButton("+ Add Card")
        add_card_btn.clicked.connect(self.add_card)
        header_layout.addWidget(add_card_btn)
        
        layout.addLayout(header_layout)
        
        # Card list
        self.card_list = QListWidget()
        self.card_list.itemDoubleClicked.connect(self.edit_card)
        layout.addWidget(self.card_list)
        
        # Card actions
        actions_layout = QHBoxLayout()
        
        edit_btn = PrimaryButton("Edit Card")
        edit_btn.clicked.connect(self.edit_card)
        actions_layout.addWidget(edit_btn)
        
        delete_btn = DangerButton("Delete Card")
        delete_btn.clicked.connect(self.delete_card)
        actions_layout.addWidget(delete_btn)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
        
    def set_deck(self, deck_id, deck_name):
        """Set the current deck"""
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.deck_title.setText(f"Managing Cards: {deck_name}")
        self.refresh_cards()
        
    def refresh_cards(self):
        """Refresh the card list"""
        if not self.current_deck_id:
            return
            
        self.card_list.clear()
        cards = self.db_manager.get_cards_in_deck(self.current_deck_id)
        
        for card in cards:
            # Truncate long text for display
            front_text = card['front'][:60] + "..." if len(card['front']) > 60 else card['front']
            back_text = card['back'][:60] + "..." if len(card['back']) > 60 else card['back']
            
            item_text = f"Q: {front_text}\nA: {back_text}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, card['id'])
            self.card_list.addItem(item)
            
    def add_card(self):
        """Add a new card"""
        # Import here to avoid circular imports
        from src.modes.decks_impl import CardDialog
        
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
            
        from src.modes.decks_impl import CardDialog
        
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


class DecksPage(QWidget):
    """Modern deck management page with card interface"""
    
    deck_selected = Signal(int)  # For studying a deck
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.deck_cards = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the decks page UI"""
        self.setStyleSheet("""
            DecksPage {
                background-color: #1a1a1a;
                color: white;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        
        # Deck gallery view
        self.deck_gallery = self.create_deck_gallery()
        self.stacked_widget.addWidget(self.deck_gallery)
        
        # Card management view
        self.card_management = CardManagementWidget(self.db_manager)
        self.card_management.back_to_decks.connect(self.show_deck_gallery)
        self.stacked_widget.addWidget(self.card_management)
        
        layout.addWidget(self.stacked_widget)
        
        # Initially show deck gallery
        self.show_deck_gallery()
        
    def create_deck_gallery(self):
        """Create the deck gallery view"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Deck Management")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Instructions
        instructions = QLabel("Create new decks or manage existing ones")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                background: transparent;
            }
        """)
        layout.addWidget(instructions)
        
        # Scroll area for deck cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: rgba(255, 255, 255, 0.1);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(255, 255, 255, 0.5);
            }
        """)
        
        # Deck cards container
        self.deck_cards_widget = QWidget()
        self.deck_cards_layout = QGridLayout(self.deck_cards_widget)
        self.deck_cards_layout.setSpacing(20)
        self.deck_cards_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        scroll_area.setWidget(self.deck_cards_widget)
        layout.addWidget(scroll_area)
        
        return widget
        
    def refresh_decks(self):
        """Refresh the deck gallery"""
        # Clear existing cards
        for card in self.deck_cards:
            card.deleteLater()
        self.deck_cards.clear()
        
        # Clear layout
        while self.deck_cards_layout.count():
            child = self.deck_cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Get decks from database
        decks = self.db_manager.get_all_decks()
        
        # Create deck cards first
        cols = 4  # Number of columns
        for i, deck in enumerate(decks):
            deck_card = DeckManagementCard(deck)
            deck_card.deck_selected.connect(self.deck_selected.emit)  # Study deck
            deck_card.edit_deck.connect(self.edit_deck)  # Edit deck (card management)
            deck_card.delete_deck.connect(self.delete_deck)
            self.deck_cards.append(deck_card)
            
            # Position deck cards
            row = i // cols
            col = i % cols
            self.deck_cards_layout.addWidget(deck_card, row, col)
        
        # Add create deck card at the end
        create_card = CreateDeckCard()
        create_card.create_deck.connect(self.create_deck)
        
        # Calculate position for create card (after all deck cards)
        total_decks = len(decks)
        create_row = total_decks // cols
        create_col = total_decks % cols
        self.deck_cards_layout.addWidget(create_card, create_row, create_col)
        
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
                
    def edit_deck(self, deck_id):
        """Edit deck or manage its cards"""
        deck = self.db_manager.get_deck(deck_id)
        if deck:
            self.card_management.set_deck(deck_id, deck['name'])
            self.stacked_widget.setCurrentWidget(self.card_management)
            
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
