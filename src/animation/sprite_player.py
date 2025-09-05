from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QRect, Qt

from .game_timer import GameTimer


class SpritePlayer(QLabel):
    """Simple sprite-sheet animation player.

    Expects a horizontal sprite sheet with equal-width frames.
    """

    def __init__(self, sprite_path: str, frame_width: int, frame_height: int, fps: int = 12, parent=None):
        super().__init__(parent)
        self._sheet = QPixmap(sprite_path)
        self._frame_w = frame_width
        self._frame_h = frame_height
        self._cols = 0 if self._sheet.isNull() else self._sheet.width() // frame_width
        self._index = 0
        self.setFixedSize(frame_width, frame_height)
        self.setScaledContents(True)

        interval = max(16, int(1000 / max(1, fps)))
        self._timer = GameTimer(interval, self)
        self._timer.tick.connect(self._on_tick)
        self._render()

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def _on_tick(self, _):
        if self._cols <= 0:
            return
        self._index = (self._index + 1) % self._cols
        self._render()

    def _render(self):
        if self._sheet.isNull() or self._cols <= 0:
            self.clear()
            return
        x = self._index * self._frame_w
        rect = self._sheet.copy(x, 0, self._frame_w, self._frame_h)
        self.setPixmap(rect)


