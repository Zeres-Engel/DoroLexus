"""
Reusable table widgets
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt


class ReviewTableWidget(QWidget):
    """Two-column read-only table to preview flashcards (Question/Answer)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet("""
            ReviewTableWidget {
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
            QTableWidget::item { padding: 8px; }
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
        """Populate table with list of dicts containing 'front' and 'back'."""
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


