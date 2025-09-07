"""
PreviewDeckPage - a page that shows a deck preview with Q/A table
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt
from src.ui import StudyPageHeaderLayout, PreviewDeckLayout


class PreviewDeckPage(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_deck_id = None
        self.current_deck_name = ""
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        self.header = StudyPageHeaderLayout()
        self.header.back_requested.connect(self._handle_back)
        layout.addWidget(self.header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.scroll)

        self.preview_layout = PreviewDeckLayout()
        self.scroll.setWidget(self.preview_layout)

    def set_deck(self, deck_id: int):
        self.current_deck_id = deck_id
        deck = next((d for d in self.db_manager.get_all_decks() if d['id'] == deck_id), None)
        if not deck:
            return
        self.current_deck_name = deck['name']
        cards = self.db_manager.get_cards_in_deck(deck_id)
        self.preview_layout.set_deck(deck_id, deck['name'], cards)

    def _handle_back(self):
        try:
            ancestor = self.parent()
            while ancestor is not None:
                if hasattr(ancestor, 'show_decks') and callable(getattr(ancestor, 'show_decks')):
                    ancestor.show_decks()
                    return
                ancestor = ancestor.parent()
        except Exception:
            pass


