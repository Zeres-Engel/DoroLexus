"""
Mini Card Widget for navigation buttons
"""

from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QColor
from src.core.paths import asset_path
from ..ui.menu_config import MiniCardConfig


class MiniCardWidget(QFrame):
    """Compact card widget for secondary menu functions"""
    clicked = Signal()
    
    def __init__(self, title: str, icon_name: str, color: str, 
                 config: MiniCardConfig = None, parent=None):
        super().__init__(parent)
        self.title = title
        self.icon_name = icon_name
        self.color = color
        self.config = config or MiniCardConfig()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the mini card UI with compact styling"""
        self.setFixedHeight(self.config.height)
        self.setFixedWidth(self.config.width)
        self.setCursor(Qt.PointingHandCursor)
        
        # Compact card styling
        self.setStyleSheet(f"""
            MiniCardWidget {{
                background: {self.color};
                border-radius: {self.config.border_radius}px;
                border: {self.config.border_width}px solid {self.config.border_color};
                margin: 4px 0px;
                outline: none;
            }}
            MiniCardWidget:hover {{
                background: {self._lighten_color(self.color, self.config.hover_lighten_factor)};
                border: {self.config.border_width}px solid {self.config.hover_border_color};
            }}
            MiniCardWidget:pressed {{
                background: {self._darken_color(self.color, self.config.press_darken_factor)};
            }}
        """)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(*self.config.margins)
        layout.setSpacing(self.config.spacing)
        layout.setAlignment(Qt.AlignCenter)
        
        # Icon
        self._create_icon_section(layout)
        
        # Title
        self._create_title_section(layout)
        
        # Add subtle shadow effect
        self._add_shadow_effect()
        
    def _create_icon_section(self, parent_layout):
        """Create the icon section"""
        icon_path = asset_path("data", "images", "svg", self.icon_name)
        if icon_path:
            icon_label = QLabel()
            pixmap = QIcon(icon_path).pixmap(self.config.icon_pixmap_size, self.config.icon_pixmap_size)
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet("background: transparent; border: none; outline: none;")
            parent_layout.addWidget(icon_label)
        
    def _create_title_section(self, parent_layout):
        """Create the title section"""
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(self.config.title_font_size)
        title_font.setBold(True)
        title_font.setFamily(self.config.title_font_family)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
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
        parent_layout.addWidget(title_label)
        
    def _add_shadow_effect(self):
        """Add subtle shadow effect for depth"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 60))
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
