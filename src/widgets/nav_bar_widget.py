"""
NavBarWidget - simple top navigation bar with logo, title and sword-styled back button
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect, QPoint
from PySide6.QtGui import QPixmap, QIcon
from src.core.paths import asset_path


class NavBarWidget(QWidget):
    """Top navigation bar used across pages as a lightweight header replacement."""

    back_requested = Signal()
    home_requested = Signal()

    def __init__(self, title: str = "", show_back_button: bool = False, parent=None):
        super().__init__(parent)
        self._title = title
        self._show_back = show_back_button
        self._init_ui()

    def _init_ui(self):
        self.setStyleSheet("""
            NavBarWidget { 
                background: rgba(30, 30, 30, 0.3); 
                border: none;
            }
            QWidget { background: transparent; }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # Brand area - use reusable HomepageButton
        from .homepage_button import HomepageButton
        self.homepage_button = HomepageButton("DoroLexus")
        self.homepage_button.clicked.connect(self.home_requested)
        layout.addWidget(self.homepage_button)

        # Title
        self.title_label = QLabel("")
        self.title_label.setVisible(False)  # Hide page title in navbar per request
        layout.addWidget(self.title_label)

        layout.addStretch()

        # Back button with sword stab animation
        self.back_btn = QPushButton()
        self.back_btn.setFixedSize(110, 36)
        
        # Animation for sword stab effect
        self.sword_animation = QPropertyAnimation(self.back_btn, b"geometry")
        self.sword_animation.setDuration(200)
        self.sword_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        self._setup_sword_back_button()
        self.back_btn.clicked.connect(self.back_requested.emit)
        self.back_btn.setVisible(self._show_back)
        layout.addWidget(self.back_btn)

    def _setup_sword_back_button(self):
        sword_path = asset_path("data", "images", "svg", "sword-svgrepo-com.svg")
        if sword_path:
            icon = QIcon(sword_path)
            if not icon.isNull():
                self.back_btn.setIcon(icon)
                self.back_btn.setText(" Back")
        else:
            self.back_btn.setText("← Back")

        self.back_btn.setStyleSheet("""
            QPushButton {
                background: rgba(128, 128, 128, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background: rgba(128, 128, 128, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: rgba(96, 96, 96, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
        """)
        
        # Add hover events for sword stab animation
        self.back_btn.enterEvent = self._on_sword_hover_enter
        self.back_btn.leaveEvent = self._on_sword_hover_leave

    # Brand click is handled in HomepageButton

    # Hover effects removed for harmonious static brand appearance

    def _on_sword_hover_enter(self, event):
        """Sword stab animation on hover - thrust forward"""
        current_rect = self.back_btn.geometry()
        # Move forward (left) by 5 pixels for stab effect
        stab_rect = QRect(current_rect.x() - 5, current_rect.y(), current_rect.width(), current_rect.height())
        
        self.sword_animation.setStartValue(current_rect)
        self.sword_animation.setEndValue(stab_rect)
        self.sword_animation.start()

    def _on_sword_hover_leave(self, event):
        """Sword return to normal position"""
        current_rect = self.back_btn.geometry()
        # Return to original position
        normal_rect = QRect(current_rect.x() + 5, current_rect.y(), current_rect.width(), current_rect.height())
        
        self.sword_animation.setStartValue(current_rect)
        self.sword_animation.setEndValue(normal_rect)
        self.sword_animation.start()

    # Public helpers
    def set_title(self, title: str):
        self._title = title
        self.title_label.setText(title)

    def show_back_button(self):
        self._show_back = True
        self.back_btn.setVisible(True)

    def hide_back_button(self):
        self._show_back = False
        self.back_btn.setVisible(False)


