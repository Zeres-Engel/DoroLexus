from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QPixmap

from src.core.paths import asset_path


class HomepageButton(QWidget):
    """Clickable brand widget combining app logo and text.

    Emits:
        clicked: when the widget is clicked with left mouse button.
    """

    clicked = Signal()

    def __init__(self, text: str = "DoroLexus", parent=None):
        super().__init__(parent)
        self._text = text
        self._init_ui()
        
        # Animation setup for gentle hover jump
        self._rest_pos = None
        self._hover_anim = QPropertyAnimation(self, b"pos")
        self._hover_anim.setDuration(140)
        self._hover_anim.setEasingCurve(QEasingCurve.OutQuad)

    def _init_ui(self):
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QWidget { background: transparent; }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.logo_label = QLabel()
        self.logo_label.setFixedSize(36, 36)
        self.logo_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                padding: 0px;
            }
        """)

        # Use official DoroLexus logo
        logo_path = asset_path("data", "images", "svg", "doro_lexus logo.svg")
        if logo_path:
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.text_label = QLabel(self._text)
        self.text_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                border: none;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)

        layout.addWidget(self.logo_label)
        layout.addWidget(self.text_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        # Capture exact rest position to avoid drift
        self._rest_pos = self.pos()
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self.pos())
        self._hover_anim.setEndValue(QPoint(self._rest_pos.x(), self._rest_pos.y() - 6))
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._rest_pos is None:
            self._rest_pos = self.pos()
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self.pos())
        self._hover_anim.setEndValue(self._rest_pos)
        self._hover_anim.start()
        super().leaveEvent(event)


