"""
Page Content Layout Components
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QScrollArea, QGridLayout, QListWidget, QListWidgetItem,
                               QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt, Signal
from ..widgets.button_widget import PrimaryButtonWidget, DangerButtonWidget


class DeckGalleryLayout(QWidget):
    """Layout for displaying deck cards in a gallery format"""
    
    deck_selected = Signal(int)  # For studying
    edit_deck = Signal(int)      # For editing cards
    delete_deck = Signal(int)
    create_deck = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.deck_cards = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the deck gallery UI"""
        self.setStyleSheet("""
            DeckGalleryLayout {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Instructions
        instructions = QLabel("Create new decks or manage existing ones")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
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
        
    def refresh_decks(self, decks):
        """Refresh the deck gallery with new deck data"""
        # Clear existing cards
        for card in self.deck_cards:
            card.deleteLater()
        self.deck_cards.clear()
        
        # Clear layout
        while self.deck_cards_layout.count():
            child = self.deck_cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create deck cards
        cols = 4  # Number of columns
        for i, deck in enumerate(decks):
            from .deck_card_layout import DeckManagementCardLayout
            deck_card = DeckManagementCardLayout(deck)
            deck_card.deck_selected.connect(self.deck_selected.emit)
            deck_card.edit_deck.connect(self.edit_deck.emit)
            deck_card.delete_deck.connect(self.delete_deck.emit)
            self.deck_cards.append(deck_card)
            
            # Position deck cards
            row = i // cols
            col = i % cols
            self.deck_cards_layout.addWidget(deck_card, row, col)
        
        # Add create deck card at the end
        from .deck_card_layout import CreateDeckCardLayout
        create_card = CreateDeckCardLayout()
        create_card.create_deck.connect(self.create_deck.emit)
        
        # Calculate position for create card (after all deck cards)
        total_decks = len(decks)
        create_row = total_decks // cols
        create_col = total_decks % cols
        self.deck_cards_layout.addWidget(create_card, create_row, create_col)


class StudyDeckSelectionLayout(QWidget):
    """Layout for study page deck selection"""
    
    deck_selected = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.deck_cards = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the study deck selection UI"""
        self.setStyleSheet("""
            StudyDeckSelectionLayout {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Instructions
        instructions = QLabel("Choose a deck to start studying")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
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
        
    def refresh_decks(self, decks):
        """Refresh the deck selection with new deck data"""
        # Clear existing cards
        for card in self.deck_cards:
            card.deleteLater()
        self.deck_cards.clear()
        
        # Clear layout
        while self.deck_cards_layout.count():
            child = self.deck_cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not decks:
            # Show no decks message
            no_decks_label = QLabel("No decks available. Create some decks first!")
            no_decks_label.setAlignment(Qt.AlignCenter)
            no_decks_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.6);
                    font-size: 16px;
                    background: transparent;
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                }
            """)
            self.deck_cards_layout.addWidget(no_decks_label)
            return
        
        # Create deck cards
        cols = 3  # Number of columns
        for i, deck in enumerate(decks):
            from .deck_card_layout import StudyDeckCardLayout
            deck_card = StudyDeckCardLayout(deck)
            deck_card.deck_selected.connect(self.deck_selected.emit)
            self.deck_cards.append(deck_card)
            
            row = i // cols
            col = i % cols
            self.deck_cards_layout.addWidget(deck_card, row, col)


class CardManagementLayout(QWidget):
    """Layout for managing cards within a deck"""
    
    add_card = Signal()
    edit_card = Signal(int)
    delete_card = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_deck_id = None
        self.current_deck_name = ""
        self.init_ui()
        
    def init_ui(self):
        """Initialize card management UI"""
        self.setStyleSheet("""
            CardManagementLayout {
                background: transparent;
                color: white;
            }
            QListWidget {
                background-color: #2d2d2d;
                border: 2px solid #444;
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
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
        
        # Deck title (centered)
        self.deck_title = QLabel()
        self.deck_title.setAlignment(Qt.AlignCenter)
        self.deck_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        header_layout.addWidget(self.deck_title)
        
        header_layout.addStretch()
        
        # Add card button
        add_card_btn = PrimaryButtonWidget("+ Add Card")
        add_card_btn.clicked.connect(self.add_card.emit)
        header_layout.addWidget(add_card_btn)
        
        layout.addLayout(header_layout)
        
        # Card list
        self.card_list = QListWidget()
        self.card_list.itemDoubleClicked.connect(self.edit_card.emit)
        layout.addWidget(self.card_list)
        
        # Card actions
        actions_layout = QHBoxLayout()
        
        edit_btn = PrimaryButtonWidget("Edit Card")
        edit_btn.clicked.connect(self.edit_card.emit)
        actions_layout.addWidget(edit_btn)
        
        delete_btn = DangerButtonWidget("Delete Card")
        delete_btn.clicked.connect(self.delete_card.emit)
        actions_layout.addWidget(delete_btn)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
        
    def set_deck(self, deck_id, deck_name):
        """Set the current deck"""
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.deck_title.setText(f"Managing Cards: {deck_name}")
        
    def refresh_cards(self, cards):
        """Refresh the card list"""
        self.card_list.clear()
        
        for card in cards:
            # Truncate long text for display
            front_text = card['front'][:60] + "..." if len(card['front']) > 60 else card['front']
            back_text = card['back'][:60] + "..." if len(card['back']) > 60 else card['back']
            
            item_text = f"Q: {front_text}\nA: {back_text}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, card['id'])
            self.card_list.addItem(item)
            
    def get_selected_card_id(self):
        """Get the ID of the currently selected card"""
        current_item = self.card_list.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None


class ReviewTableLayout(QWidget):
    """Simple two-column table to preview cards before studying"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("""
            ReviewTableLayout {
                background: transparent;
                color: white;
            }
            QTableWidget {
                background-color: #2d2d2d;
                border: 2px solid #444;
                border-radius: 8px;
                gridline-color: #555;
                color: white;
                font-size: 14px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QHeaderView::section {
                background-color: #383838;
                color: white;
                padding: 6px 10px;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)
        
        title = QLabel("Review Cards")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                margin: 6px 0px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(title)
        
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Question", "Answer"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultSectionSize(400)
        self.table.verticalHeader().setVisible(False)
        self.table.setWordWrap(True)
        self.table.setShowGrid(True)
        layout.addWidget(self.table)
        
    def set_cards(self, cards):
        """Populate table rows with list of {front, back}"""
        self.table.setRowCount(0)
        if not cards:
            return
        self.table.setRowCount(len(cards))
        for row, card in enumerate(cards):
            q_item = QTableWidgetItem(card.get('front', ''))
            a_item = QTableWidgetItem(card.get('back', ''))
            q_item.setFlags(q_item.flags() ^ Qt.ItemIsEditable)
            a_item.setFlags(a_item.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 0, q_item)
            self.table.setItem(row, 1, a_item)
