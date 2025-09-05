from PySide6.QtCore import QObject, QTimer, Signal

class GameTimer(QObject):
    tick = Signal(int)  # emits elapsed milliseconds

    def __init__(self, interval_ms: int = 16, parent=None):
        super().__init__(parent)
        self._timer = QTimer(self)
        self._timer.setInterval(interval_ms)
        self._timer.timeout.connect(self._on_timeout)
        self._elapsed = 0

    def start(self):
        self._elapsed = 0
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def set_interval(self, interval_ms: int):
        self._timer.setInterval(interval_ms)

    def _on_timeout(self):
        self._elapsed += self._timer.interval()
        self.tick.emit(self._elapsed)
