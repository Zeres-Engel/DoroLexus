"""
PreviewDeckLayout - deck header info and a review table of all cards
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from .page_header_layout import StudyPageHeaderLayout
from ..widgets.table_widget import ReviewTableWidget


class PreviewDeckLayout(QWidget):
    """Layout for previewing a deck with deck info and a Q/A table."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_deck_id = None
        self.current_deck_name = ""
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet("""
            PreviewDeckLayout { background: transparent; }
            QWidget { background: transparent; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Title
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white; font-size: 24px; font-weight: bold; background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(self.title_label)

        # Table
        self.review_table = ReviewTableWidget()
        layout.addWidget(self.review_table)

    def set_deck(self, deck_id: int, deck_name: str, cards):
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.title_label.setText(f"Preview: {deck_name}")
        self.review_table.set_cards(cards)


