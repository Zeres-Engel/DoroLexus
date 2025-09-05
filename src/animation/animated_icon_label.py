from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QIcon, QPixmap, QTransform
from PySide6.QtCore import QPointF, Qt, Signal

from .game_timer import GameTimer


class AnimatedIconLabel(QLabel):
    clicked = Signal()
    def __init__(self, icon_path: str, size: int = 48, parent=None):
        super().__init__(parent)
        self._icon_path = icon_path
        self._size = size
        self._angle = 0.0
        self._bounce = 0.0
        self._dir = 1.0

        self.setFixedSize(size, size)
        self.setScaledContents(True)

        self._timer = GameTimer(16, self)
        self._timer.tick.connect(self._on_tick)
        self._update_pixmap()

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def _on_tick(self, elapsed_ms: int):
        # Rotate slowly and bounce up/down
        self._angle = (self._angle + 0.5) % 360
        self._bounce += 0.6 * self._dir
        if self._bounce > 6:
            self._bounce = 6
            self._dir = -1.0
        elif self._bounce < -2:
            self._bounce = -2
            self._dir = 1.0
        self._update_pixmap()

    def _update_pixmap(self):
        if not self._icon_path:
            return
        base = QIcon(self._icon_path).pixmap(self._size, self._size)
        if base.isNull():
            self.clear()
            return
        pix = QPixmap(base)
        transform = QTransform()
        transform.translate(self._size / 2, self._size / 2)
        transform.rotate(self._angle)
        transform.translate(-self._size / 2, -self._size / 2)
        rotated = pix.transformed(transform, mode=Qt.SmoothTransformation) if hasattr(pix, 'transformed') else pix
        self.move(self.x(), int(self.y() + self._bounce))
        self.setPixmap(rotated)

    def mousePressEvent(self, event):
        self.clicked.emit()
        return super().mousePressEvent(event)
