from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer, QSequentialAnimationGroup, QParallelAnimationGroup
from PySide6.QtGui import QFont, QLinearGradient, QColor, QPalette

from .sword_tomato_anim import SwordTomatoAnim

class GameLikeWelcomeBanner(QWidget):
    """Enhanced game-like welcome banner with multiple animations and styling"""
    
    def __init__(self, title: str = "DoroLexus", subtitle: str = "Master Your Vocabulary Journey", parent=None):
        super().__init__(parent)
        self.title_text = title
        self.subtitle_text = subtitle
        self.init_ui()
        self.setup_animations()

    def init_ui(self):
        """Initialize the banner UI with game-like styling"""
        self.setFixedHeight(180)
        self.setFixedWidth(600)  # Fixed width for consistent centering
        
        # Set size policy to ensure centering
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Apply game-like banner styling
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(31, 111, 235, 0.8),
                    stop:0.5 rgba(46, 125, 50, 0.8),
                    stop:1 rgba(31, 111, 235, 0.6));
                border-radius: 15px;
                border: none;
                outline: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)
        
        # Main title
        self.title_label = QLabel(self.title_text)
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title_font.setFamily("Arial")
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                border: none;
                outline: none;
                padding: 0px;
                margin: 0px;
            }
        """)
        
        # Removed shadow effect to eliminate black borders
        # title_shadow = QGraphicsDropShadowEffect()
        # title_shadow.setBlurRadius(10)
        # title_shadow.setColor(QColor(0, 0, 0, 100))
        # title_shadow.setOffset(2, 2)
        # self.title_label.setGraphicsEffect(title_shadow)
        
        layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel(self.subtitle_text)
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_font.setItalic(True)
        self.subtitle_label.setFont(subtitle_font)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                border: none;
                outline: none;
                padding: 0px;
                margin: 0px;
            }
        """)
        
        layout.addWidget(self.subtitle_label)

        # Sword -> Tomato animation centered under subtitle
        anim_row = QHBoxLayout()
        anim_row.setAlignment(Qt.AlignCenter)
        self.sword_tomato = SwordTomatoAnim(size=28)
        self.sword_tomato.setStyleSheet("background: transparent; border: none; outline: none;")
        anim_row.addWidget(self.sword_tomato)
        layout.addLayout(anim_row)
        
        # Progress indicator dots (game-like)
        dots_layout = QHBoxLayout()
        dots_layout.setAlignment(Qt.AlignCenter)
        dots_layout.setSpacing(8)
        
        self.dots = []
        for i in range(4):
            dot = QLabel("●")
            dot.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.4);
                    font-size: 16px;
                    background: transparent;
                    border: none;
                    outline: none;
                    padding: 0px;
                    margin: 0px;
                }
            """)
            self.dots.append(dot)
            dots_layout.addWidget(dot)
            
        layout.addLayout(dots_layout)

    def setup_animations(self):
        """Setup multiple coordinated animations"""
        # Slide in animation
        self.slide_anim = QPropertyAnimation(self, b"geometry")
        self.slide_anim.setDuration(800)
        self.slide_anim.setEasingCurve(QEasingCurve.OutBack)
        
        # Dot pulse animation timer
        self.dot_timer = QTimer()
        self.dot_timer.timeout.connect(self.animate_dots)
        self.current_dot = 0

    def play(self):
        """Start the welcome banner animations"""
        # Get initial geometry
        w = self.width() or 600
        h = self.height() or 180
        
        # Start from above the screen
        start_rect = QRect(0, -h - 20, w, h)
        end_rect = QRect(0, 0, w, h)
        
        self.setGeometry(start_rect)
        self.slide_anim.setStartValue(start_rect)
        self.slide_anim.setEndValue(end_rect)
        
        # Start slide animation
        self.slide_anim.start()
        
        # Start dot animation and sword->tomato after slide completes
        QTimer.singleShot(900, self.start_dot_animation)
        QTimer.singleShot(900, self.sword_tomato.play)

    def start_dot_animation(self):
        """Start the pulsing dot animation"""
        self.dot_timer.start(600)  # Pulse every 600ms

    def animate_dots(self):
        """Animate the progress dots"""
        # Reset all dots
        for dot in self.dots:
            dot.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.4);
                    font-size: 16px;
                    background: transparent;
                }
            """)
        
        # Highlight current dot
        if self.current_dot < len(self.dots):
            self.dots[self.current_dot].setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    background: transparent;
                }
            """)
        
        self.current_dot = (self.current_dot + 1) % len(self.dots)

    def stop_animations(self):
        """Stop all animations"""
        if self.dot_timer.isActive():
            self.dot_timer.stop()


# Keep the old class for backward compatibility
class AnimatedWelcomeBanner(GameLikeWelcomeBanner):
    def __init__(self, text: str = "Welcome to DoroLexus!", parent=None):
        super().__init__("DoroLexus", "Master Your Vocabulary Journey", parent)
