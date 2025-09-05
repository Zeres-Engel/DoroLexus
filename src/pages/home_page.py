"""
Home page for DoroLexus - Game-like main menu
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import QBoxLayout
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from src.core.paths import asset_path
from src.animation import AnimatedWelcomeBanner, SwordTomatoAnim


class MenuCard(QFrame):
    """Enhanced card widget for main menu functions"""
    clicked = Signal()
    
    def __init__(self, title, subtitle, icon_name, color, parent=None):
        super().__init__(parent)
        self.title = title
        self.subtitle = subtitle
        self.icon_name = icon_name
        self.color = color
        self.init_ui()
        
    def init_ui(self):
        """Initialize the card UI"""
        self.setFixedHeight(90)
        self.setCursor(Qt.PointingHandCursor)
        
        # Apply card styling without borders to prevent sticking
        self.setStyleSheet(f"""
            MenuCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color},
                    stop:1 rgba(45, 45, 45, 0.9));
                border-radius: 15px;
                border: none;
                margin: 4px 0px;
                outline: none;
            }}
            MenuCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color},
                    stop:1 rgba(55, 55, 55, 0.95));
                border: none;
                outline: none;
            }}
        """)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(14)
        
        # Icon section
        icon_container = QWidget()
        icon_container.setFixedSize(40, 40)
        icon_container.setStyleSheet("background: transparent; border: none; outline: none;")
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)
        
        icon_path = asset_path("data", "images", "svg", self.icon_name)
        if icon_path:
            icon_label = QLabel()
            pixmap = QIcon(icon_path).pixmap(28, 28)
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet("background: transparent; border: none; outline: none;")
            icon_layout.addWidget(icon_label)
        
        layout.addWidget(icon_container)
        
        # Text section - simplified without overlapping panel
        text_widget = QWidget()
        text_widget.setStyleSheet("background: transparent; border: none; outline: none;")
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(8, 6, 8, 6)
        text_layout.setSpacing(4)

        # Title
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_font.setFamily("Arial")
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; background: transparent; border: none; outline: none; padding: 0px; margin: 0px;")
        text_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel(self.subtitle)
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle_font.setFamily("Arial")
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet("color: rgba(255,255,255,0.9); background: transparent; border: none; outline: none; padding: 0px; margin: 0px;")
        text_layout.addWidget(subtitle_label)
        
        layout.addWidget(text_widget, stretch=1)
        layout.addStretch()

        # Removed shadow effect to eliminate black borders
        # shadow = QGraphicsDropShadowEffect(self)
        # shadow.setBlurRadius(16)
        # shadow.setOffset(0, 4)
        # shadow.setColor(QColor(0, 0, 0, 120))
        # self.setGraphicsEffect(shadow)
        
    def mousePressEvent(self, event):
        """Handle mouse click"""
        self.clicked.emit()
        super().mousePressEvent(event)


class MiniCard(QFrame):
    """Mini card for secondary functions"""
    clicked = Signal()
    
    def __init__(self, title, icon_name, color, parent=None):
        super().__init__(parent)
        self.title = title
        self.icon_name = icon_name
        self.color = color
        self.init_ui()
        
    def init_ui(self):
        """Initialize the mini card UI"""
        self.setFixedSize(140, 58)
        self.setCursor(Qt.PointingHandCursor)
        
        # Apply styling without borders
        self.setStyleSheet(f"""
            MiniCard {{
                background-color: {self.color};
                border-radius: 12px;
                border: none;
                margin: 2px;
                outline: none;
            }}
            MiniCard:hover {{
                background-color: {self.lighten_color(self.color)};
                border: none;
                outline: none;
            }}
        """)
        
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        
        # Icon
        icon_path = asset_path("data", "images", "svg", self.icon_name)
        if icon_path:
            icon_label = QLabel()
            pixmap = QIcon(icon_path).pixmap(22, 22)
            icon_label.setPixmap(pixmap)
            icon_label.setFixedSize(22, 22)
            icon_label.setStyleSheet("background: transparent; border: none; outline: none;")
            layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_font.setFamily("Arial")
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                border: none;
                outline: none;
                padding: 0px;
                margin: 0px;
            }
        """)
        layout.addWidget(title_label)
        
    def lighten_color(self, hex_color):
        """Lighten color for hover effect"""
        color_map = {
            "#6F42C1": "#8A5FD3",
            "#DC3545": "#E85A67"
        }
        return color_map.get(hex_color, hex_color)
        
    def mousePressEvent(self, event):
        """Handle mouse click"""
        self.clicked.emit()
        super().mousePressEvent(event)


class HomePage(QWidget):
    """Main home page with game-like interface"""
    
    # Signals for navigation
    study_requested = Signal()
    decks_requested = Signal()
    timer_requested = Signal()
    stats_requested = Signal()
    exit_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the home page UI"""
        # Apply background gradient
        self.setStyleSheet("""
            HomePage {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(18, 18, 18, 0.95),
                    stop:0.5 rgba(30, 30, 30, 0.95),
                    stop:1 rgba(18, 18, 18, 0.95));
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)  # Changed back to top alignment for better control
        
        # Welcome banner - always centered using a container with stretches
        self.banner = AnimatedWelcomeBanner()
        
        # Create a centering container with explicit stretch factors
        self._banner_container = QWidget()
        self._banner_container.setFixedHeight(200)  # Ensure consistent height
        self._banner_container.setStyleSheet("background-color: transparent;")  # Ensure no background overlay
        _banner_hbox = QHBoxLayout(self._banner_container)
        _banner_hbox.setContentsMargins(0, 10, 0, 10)
        _banner_hbox.addStretch(1)  # Left stretch
        _banner_hbox.addWidget(self.banner, 0, Qt.AlignCenter)  # Center with explicit alignment
        _banner_hbox.addStretch(1)  # Right stretch
        
        layout.addWidget(self._banner_container, 0, Qt.AlignHCenter)
        
        # Main function cards centered and constrained width
        cards_layout = QVBoxLayout()
        cards_layout.setSpacing(28)
        cards_layout.setAlignment(Qt.AlignHCenter)
        
        # Study card
        self.study_card = MenuCard(
            "Study Flashcards",
            "Review and learn your vocabulary with spaced repetition",
            "sword-svgrepo-com.svg",
            "#1F6FEB"
        )
        self.study_card.clicked.connect(self.study_requested.emit)
        self.study_card.setFixedWidth(620)
        cards_layout.addWidget(self.study_card, alignment=Qt.AlignHCenter)
        
        # Decks card
        self.decks_card = MenuCard(
            "Manage Decks",
            "Create and organize your study decks and flashcards",
            "tomato-svgrepo-com.svg",
            "#2EA043"
        )
        self.decks_card.clicked.connect(self.decks_requested.emit)
        self.decks_card.setFixedWidth(620)
        cards_layout.addWidget(self.decks_card, alignment=Qt.AlignHCenter)
        
        # Timer card
        self.timer_card = MenuCard(
            "Study Timer",
            "Focus sessions with Pomodoro technique - Easy, Normal, Hard modes",
            "clock-svgrepo-com.svg",
            "#E3B341"
        )
        self.timer_card.clicked.connect(self.timer_requested.emit)
        self.timer_card.setFixedWidth(620)
        cards_layout.addWidget(self.timer_card, alignment=Qt.AlignHCenter)
        
        layout.addLayout(cards_layout)
        
        # Secondary functions centered and smaller
        self.secondary_layout = QHBoxLayout()
        self.secondary_layout.setSpacing(12)
        self.secondary_layout.setAlignment(Qt.AlignHCenter)
        
        # Statistics card
        self.stats_card = MiniCard("Statistics", "research-svgrepo-com.svg", "#6F42C1")
        self.stats_card.clicked.connect(self.stats_requested.emit)
        self.secondary_layout.addWidget(self.stats_card)
        
        # Exit card
        self.exit_card = MiniCard("Exit", "school-bell-svgrepo-com.svg", "#DC3545")
        self.exit_card.clicked.connect(self.exit_requested.emit)
        self.secondary_layout.addWidget(self.exit_card)
        
        # Add the secondary layout with center alignment
        layout.addLayout(self.secondary_layout)
        
        # Animated decoration
        decoration_layout = QHBoxLayout()
        decoration_layout.setAlignment(Qt.AlignCenter)
        
        sword_tomato = SwordTomatoAnim(size=36)
        sword_tomato.setStyleSheet("background: transparent; border: none; outline: none;")
        decoration_layout.addWidget(sword_tomato)
        sword_tomato.play()
        
        layout.addLayout(decoration_layout)
        
    def show_with_animation(self):
        """Show the page with welcome animation"""
        # Force proper layout reset
        self.reset_layout()
        
        # Multiple timer calls to ensure layout is properly refreshed
        QTimer.singleShot(10, self.reset_layout)
        QTimer.singleShot(50, self.reset_layout)
        
        self.banner.play()
        
    def reset_layout(self):
        """Reset and center the layout properly"""
        if hasattr(self, '_banner_container') and hasattr(self, 'banner'):
            # Force container and banner to proper sizes
            self._banner_container.setFixedHeight(200)
            self.banner.setFixedWidth(600)
            
            # Activate and update all layouts
            if hasattr(self._banner_container, 'layout'):
                banner_layout = self._banner_container.layout()
                if banner_layout:
                    banner_layout.activate()
                    banner_layout.update()
            
            # Force main layout update
            main_layout = self.layout()
            if main_layout:
                main_layout.activate()
                main_layout.update()
                
            # Force secondary layout centering
            if hasattr(self, 'secondary_layout'):
                self.secondary_layout.setAlignment(Qt.AlignHCenter)
                self.secondary_layout.activate()
                self.secondary_layout.update()
                
            # Force geometry and visual updates
            self._banner_container.updateGeometry()
            self.banner.updateGeometry()
            self.updateGeometry()
            self.update()
        
    def ensure_banner_centered(self):
        """Ensure the banner is properly centered"""
        if hasattr(self, 'banner') and hasattr(self, '_banner_container'):
            # Force the banner to fixed size
            self.banner.setFixedWidth(600)
            
            # Force layout updates at multiple levels
            if hasattr(self._banner_container, 'layout'):
                self._banner_container.layout().activate()
                self._banner_container.layout().update()
            
            self.layout().activate()
            self.layout().update()
            self.updateGeometry()
            self.update()
            
            # Force repaint
            self.repaint()

    def resizeEvent(self, event):
        """Responsive layout changes when window is resized/minimized"""
        super().resizeEvent(event)
        
        # Ensure banner stays centered
        self.reset_layout()
        
        available_width = max(360, min(self.width() - 80, 780))

        # Resize main cards to available width
        for card in [self.study_card, self.decks_card, self.timer_card]:
            card.setFixedWidth(available_width)
            # Add top margin to ensure separation at very small heights
            card.setContentsMargins(0, 6, 0, 6)

        # Switch secondary buttons to vertical stack on narrow widths
        if self.width() < 520:
            self.secondary_layout.setDirection(QBoxLayout.TopToBottom)
            self.secondary_layout.setSpacing(8)
        else:
            self.secondary_layout.setDirection(QBoxLayout.LeftToRight)
            self.secondary_layout.setSpacing(12)
