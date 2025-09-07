"""
StudyModeMenuWidget - reusable study mode menu with cards
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Qt, Signal


class StudyModeCard(QFrame):
    mode_selected = Signal(str)

    def __init__(self, mode_type, title, description, icon_text="📚", color="#64c8ff", parent=None):
        super().__init__(parent)
        self.mode_type = mode_type
        self.title = title
        self.description = description
        self.icon_text = icon_text
        self.color = color
        self._init_ui()

    def _init_ui(self):
        self.setFixedSize(280, 160)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            StudyModeCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 60, 60, 0.9),
                    stop:1 rgba(40, 40, 40, 0.9));
                border-radius: 16px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }}
            StudyModeCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(80, 80, 80, 0.9),
                    stop:1 rgba(60, 60, 60, 0.9));
                border: 2px solid {self.color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        icon_label = QLabel(self.icon_text)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {self.color};
                font-size: 48px;
                background: transparent;
                font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji";
            }}
        """)
        layout.addWidget(icon_label)

        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.color};
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }}
        """)
        layout.addWidget(title_label)

        desc_label = QLabel(self.description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(desc_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mode_selected.emit(self.mode_type)
        super().mousePressEvent(event)


class StudyModeMenuWidget(QWidget):
    mode_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet("""
            StudyModeMenuWidget { background: transparent; }
            QWidget { background: transparent; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        title = QLabel("Choose Your Study Mode")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                margin: 10px 0px;
            }
        """)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        study_modes = [
            ("review", "Review", "Study with spaced repetition algorithm", "🧠", "#64c8ff"),
            ("test", "Test Mode", "Quiz yourself without revealing answers", "✏️", "#ff6b6b"),
            ("browse", "Browse Cards", "Go through cards at your own pace", "📖", "#66bb6a"),
            ("cram", "Cram Session", "Quick review of all cards", "⚡", "#ffa726"),
            ("new_only", "New Cards", "Study only new, unseen cards", "✨", "#ab47bc"),
            ("difficult", "Difficult Cards", "Focus on cards you find challenging", "🎯", "#f44336"),
        ]

        for i, (mode, title_text, desc, icon, color) in enumerate(study_modes):
            card = StudyModeCard(mode, title_text, desc, icon, color)
            card.mode_selected.connect(self.mode_selected.emit)
            row, col = divmod(i, 3)
            grid.addWidget(card, row, col)

        layout.addLayout(grid)
        layout.addStretch()


