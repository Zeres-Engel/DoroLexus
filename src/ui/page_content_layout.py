"""
Page Content Layout Components
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QScrollArea, QGridLayout, QListWidget, QListWidgetItem,
                               QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt, Signal
from ..widgets.button_widget import PrimaryButtonWidget, DangerButtonWidget




class StudyDeckSelectionLayout(QWidget):
    """Layout for study page deck selection with multi-selection and study mode menu"""
    
    deck_selected = Signal(int)  # For single deck preview
    study_mode_selected = Signal(str, list)  # mode_type, selected_deck_ids
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_deck_ids = []
        self.deck_id_to_name = {}
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
        
        # Compact study mode menu (initially hidden)
        from src.widgets.compact_study_menu_widget import CompactStudyMenuWidget
        self.study_menu = CompactStudyMenuWidget()
        # Start should trigger upward emission with current selected decks
        self.study_menu.start_requested.connect(lambda mode, decks: self.study_mode_selected.emit(mode, decks))
        # Cancel clears selection and hides the menu via our helper
        self.study_menu.cancel_requested.connect(self.clear_selection)
        # Retain mode_selected for potential future UI reactions
        self.study_menu.mode_selected.connect(self._on_study_mode_selected)
        layout.addWidget(self.study_menu)
        
        # Responsive deck gallery (with title)
        from .responsive_deck_gallery_layout import ResponsiveDeckGalleryLayout
        self.deck_gallery = ResponsiveDeckGalleryLayout()
        self.deck_gallery.deck_selected.connect(self._on_deck_toggled)
        self.deck_gallery.preview_requested.connect(self.deck_selected.emit)
        layout.addWidget(self.deck_gallery)
        
    def refresh_decks(self, decks):
        """Refresh the deck selection with new deck data"""
        # Store deck names for reference
        self.deck_id_to_name = {deck['id']: deck['name'] for deck in decks}
        
        # Delegate to responsive deck gallery
        self.deck_gallery.refresh_decks(decks)
    
    def _on_deck_toggled(self, deck_id):
        """Handle deck selection/deselection (no preview)"""
        if deck_id in self.selected_deck_ids:
            self.selected_deck_ids.remove(deck_id)
        else:
            self.selected_deck_ids.append(deck_id)
        
        # Update study menu visibility and content
        selected_names = [self.deck_id_to_name.get(deck_id, f"Deck {deck_id}") 
                         for deck_id in self.selected_deck_ids]
        self.study_menu.set_selected_decks(self.selected_deck_ids, selected_names)
    
    def _on_study_mode_selected(self, mode_type):
        """Handle study mode selection"""
        if self.selected_deck_ids:
            self.study_mode_selected.emit(mode_type, self.selected_deck_ids.copy())
    
    def clear_selection(self):
        """Clear all deck selections"""
        self.selected_deck_ids.clear()
        self.deck_gallery.clear_selection()
        self.study_menu.set_selected_decks([])
    
    def get_selected_deck_ids(self):
        """Get list of currently selected deck IDs"""
        return self.selected_deck_ids.copy()


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
