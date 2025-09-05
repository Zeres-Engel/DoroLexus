from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from .theme import PRIMARY_COLOR, DANGER_COLOR


class PrimaryButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: #FFFFFF;
                border: 1px solid #2D333B;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #2A7FFF; }}
            QPushButton:pressed {{ background-color: #1964D0; }}
        """)


class DangerButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {DANGER_COLOR};
                color: #FFFFFF;
                border: 1px solid #7A1C23;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #b02a37; }}
            QPushButton:pressed {{ background-color: #9a2430; }}
        """)


class IconTextButton(QPushButton):
    def __init__(self, text: str, icon_path: str = None, parent=None):
        super().__init__(f"  {text}", parent)
        self.setMinimumHeight(50)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
        self.setStyleSheet("""
            QPushButton {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #2D2D2D;
                padding: 10px 16px;
                border-radius: 8px;
                font-size: 14px;
                text-align: left;
            }
            QPushButton:hover { background-color: #2A2A2A; }
            QPushButton:pressed { background-color: #252525; }
        """)
