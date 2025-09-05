from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup, QSequentialAnimationGroup
from PySide6.QtGui import QIcon

from src.core.paths import asset_path


class SwordTomatoAnim(QWidget):
    def __init__(self, size: int = 48, parent=None):
        super().__init__(parent)
        self.size = size
        self.setStyleSheet("background: transparent; border: none; outline: none;")

        # Icons
        tomato_path = asset_path('data','images','svg','tomato-svgrepo-com.svg') or ''
        sword_path = asset_path('data','images','svg','sword-svgrepo-com.svg') or ''

        self.tomato = QLabel()
        self.tomato.setFixedSize(size, size)
        self.tomato.setStyleSheet("background: transparent; border: none; outline: none;")
        if tomato_path:
            self.tomato.setPixmap(QIcon(tomato_path).pixmap(size, size))

        self.sword = QLabel()
        self.sword.setFixedSize(size, size)
        self.sword.setStyleSheet("background: transparent; border: none; outline: none;")
        if sword_path:
            self.sword.setPixmap(QIcon(sword_path).pixmap(size, size))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(12)
        layout.addWidget(self.sword)
        layout.addWidget(self.tomato)

        # Animations
        self.sword_move = QPropertyAnimation(self.sword, b"geometry", self)
        self.sword_move.setDuration(700)
        self.sword_move.setEasingCurve(QEasingCurve.OutCubic)

        # Tomato shake group (left-right jitter)
        self.shake1 = QPropertyAnimation(self.tomato, b"geometry", self)
        self.shake1.setDuration(80)
        self.shake2 = QPropertyAnimation(self.tomato, b"geometry", self)
        self.shake2.setDuration(80)
        self.shake3 = QPropertyAnimation(self.tomato, b"geometry", self)
        self.shake3.setDuration(80)
        self.shake_group = QSequentialAnimationGroup(self)
        self.shake_group.addAnimation(self.shake1)
        self.shake_group.addAnimation(self.shake2)
        self.shake_group.addAnimation(self.shake3)

        self.sequence = QSequentialAnimationGroup(self)
        self.sequence.addAnimation(self.sword_move)
        self.sequence.addAnimation(self.shake_group)

    def play(self):
        # Layout must be done before geometry animations
        self.adjustSize()
        s_geo = self.sword.geometry()
        t_geo = self.tomato.geometry()
        # Start sword left of its current position
        start = QRect(s_geo.x()-80, s_geo.y(), s_geo.width(), s_geo.height())
        self.sword.setGeometry(start)
        self.sword_move.setStartValue(start)
        # End sword slightly overlapping tomato
        end = QRect(s_geo.x()-8, s_geo.y(), s_geo.width(), s_geo.height())
        self.sword_move.setEndValue(end)

        # Tomato shake keyframes
        self.shake1.setStartValue(t_geo)
        self.shake1.setEndValue(QRect(t_geo.x()+6, t_geo.y(), t_geo.width(), t_geo.height()))
        self.shake2.setStartValue(QRect(t_geo.x()+6, t_geo.y(), t_geo.width(), t_geo.height()))
        self.shake2.setEndValue(QRect(t_geo.x()-4, t_geo.y(), t_geo.width(), t_geo.height()))
        self.shake3.setStartValue(QRect(t_geo.x()-4, t_geo.y(), t_geo.width(), t_geo.height()))
        self.shake3.setEndValue(t_geo)

        self.sequence.start()
