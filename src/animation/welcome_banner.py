from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont


class AnimatedWelcomeBanner(QWidget):
    def __init__(self, text: str = "Welcome to DoroLexus!", parent=None):
        super().__init__(parent)
        self.label = QLabel(text)
        f = QFont()
        f.setPointSize(18)
        f.setBold(True)
        self.label.setFont(f)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #2E7D32;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        # Opacity via graphics effect would be heavier; emulate with color fade if needed.
        self._pos_anim = QPropertyAnimation(self, b"geometry")
        self._pos_anim.setDuration(700)
        self._pos_anim.setEasingCurve(QEasingCurve.OutCubic)

    def play(self):
        w = self.width() or 400
        h = self.height() or 40
        start = QRect(0, -h, self.width(), self.height())
        end = QRect(0, 0, self.width(), self.height())
        self.setGeometry(start)
        self._pos_anim.setStartValue(start)
        self._pos_anim.setEndValue(end)
        self._pos_anim.start()
