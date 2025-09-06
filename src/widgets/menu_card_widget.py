"""
Menu Card Widget for the main menu
"""

from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QColor
from src.core.paths import asset_path
from ..ui.menu_config import MenuCardConfig


class MenuCardWidget(QFrame):
    """Minimal card widget for main menu functions"""
    clicked = Signal()
    
    def __init__(self, title: str, subtitle: str, icon_name: str, color: str, 
                 config: MenuCardConfig = None, parent=None):
        super().__init__(parent)
        self.title = title
        self.subtitle = subtitle
        self.icon_name = icon_name
        self.color = color
        self.config = config or MenuCardConfig()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the card UI with minimal styling"""
        self.setFixedHeight(self.config.height)
        self.setFixedWidth(self.config.width)
        self.setCursor(Qt.PointingHandCursor)
        
        # Minimal card styling
        self.setStyleSheet(f"""
            MenuCardWidget {{
                background: {self.color};
                border-radius: {self.config.border_radius}px;
                border: {self.config.border_width}px solid {self.config.border_color};
                margin: 8px 0px;
                outline: none;
            }}
            MenuCardWidget:hover {{
                background: {self._lighten_color(self.color, self.config.hover_lighten_factor)};
                border: {self.config.border_width}px solid {self.config.hover_border_color};
            }}
            MenuCardWidget:pressed {{
                background: {self._darken_color(self.color, self.config.press_darken_factor)};
            }}
        """)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(*self.config.margins)
        layout.setSpacing(self.config.spacing)
        
        # Icon section
        self._create_icon_section(layout)
        
        # Text section
        self._create_text_section(layout)
        
        # Add subtle shadow effect
        self._add_shadow_effect()
        
    def _create_icon_section(self, parent_layout):
        """Create the icon section"""
        icon_container = QWidget()
        icon_container.setFixedSize(self.config.icon_size, self.config.icon_size)
        icon_container.setStyleSheet(f"""
            QWidget {{
                background: {self.config.icon_background};
                border-radius: {self.config.icon_border_radius}px;
            }}
        """)
        
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)
        
        icon_path = asset_path("data", "images", "svg", self.icon_name)
        if icon_path:
            icon_label = QLabel()
            pixmap = QIcon(icon_path).pixmap(self.config.icon_pixmap_size, self.config.icon_pixmap_size)
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet("background: transparent; border: none; outline: none;")
            icon_layout.addWidget(icon_label)
        
        parent_layout.addWidget(icon_container)
        
    def _create_text_section(self, parent_layout):
        """Create the text section"""
        text_widget = QWidget()
        text_widget.setStyleSheet("background: transparent; border: none; outline: none;")
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(12, 8, 12, 8)
        text_layout.setSpacing(6)

        # Title
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(self.config.title_font_size)
        title_font.setBold(True)
        title_font.setFamily(self.config.title_font_family)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.config.title_color};
                background: transparent;
                border: none;
                outline: none;
                padding: 0px;
                margin: 0px;
                font-weight: 600;
            }}
        """)
        text_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel(self.subtitle)
        subtitle_font = QFont()
        subtitle_font.setPointSize(self.config.subtitle_font_size)
        subtitle_font.setFamily(self.config.subtitle_font_family)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                color: {self.config.subtitle_color};
                background: transparent;
                border: none;
                outline: none;
                padding: 0px;
                margin: 0px;
                line-height: 1.4;
            }}
        """)
        text_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(text_widget, stretch=1)
        parent_layout.addStretch()
        
    def _add_shadow_effect(self):
        """Add subtle shadow effect for depth"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)
        
    def _lighten_color(self, hex_color: str, factor: float = 0.1) -> str:
        """Lighten a hex color by a factor"""
        if not hex_color.startswith('#'):
            return hex_color
        
        # Remove # and convert to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Lighten each component
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _darken_color(self, hex_color: str, factor: float = 0.1) -> str:
        """Darken a hex color by a factor"""
        if not hex_color.startswith('#'):
            return hex_color
        
        # Remove # and convert to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Darken each component
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def mousePressEvent(self, event):
        """Handle mouse click"""
        self.clicked.emit()
        super().mousePressEvent(event)
