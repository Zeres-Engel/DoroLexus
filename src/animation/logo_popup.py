from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer
from PySide6.QtGui import QIcon


class _LogoPopup(QWidget):
    def __init__(self, icon_path: str, size: int = 96, parent=None):
        super().__init__(parent, Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self._label = QLabel(self)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.setPixmap(QIcon(icon_path).pixmap(size, size))
        self.resize(size + 24, size + 24)

        # Center label
        self._label.resize(self.size())

        # Scale-in via geometry animation
        self._anim = QPropertyAnimation(self, b"geometry", self)
        self._anim.setDuration(350)
        self._anim.setEasingCurve(QEasingCurve.OutBack)
        self._fade = QPropertyAnimation(self, b"windowOpacity", self)
        self._fade.setDuration(300)

    def show_centered(self, center_on: QWidget, lifespan_ms: int = 900):
        # Position popup centered over center_on
        parent_rect = center_on.frameGeometry()
        w, h = self.width(), self.height()
        x = parent_rect.center().x() - w // 2
        y = parent_rect.center().y() - h // 2
        end_rect = QRect(x, y, w, h)
        start_rect = QRect(x + w // 2, y + h // 2, 1, 1)

        self.setWindowOpacity(0.0)
        self.setGeometry(start_rect)
        self.show()

        self._anim.stop(); self._fade.stop()
        self._anim.setStartValue(start_rect)
        self._anim.setEndValue(end_rect)
        self._fade.setStartValue(0.0)
        self._fade.setEndValue(1.0)
        self._anim.start(); self._fade.start()

        # Auto fade-out
        def _close():
            fade_out = QPropertyAnimation(self, b"windowOpacity", self)
            fade_out.setDuration(250)
            fade_out.setStartValue(1.0)
            fade_out.setEndValue(0.0)
            fade_out.finished.connect(self.close)
            fade_out.start()

        QTimer.singleShot(lifespan_ms, _close)


def show_logo_popup(parent: QWidget, icon_path: str, size: int = 96, lifespan_ms: int = 900):
    popup = _LogoPopup(icon_path, size=size, parent=parent)
    popup.show_centered(parent, lifespan_ms=lifespan_ms)
    return popup


