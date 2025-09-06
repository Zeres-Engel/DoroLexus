"""
Welcome Banner Widget - Main banner component for the application
"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer, QSequentialAnimationGroup, QParallelAnimationGroup, QPointF, QEasingCurve
from PySide6.QtGui import QFont, QLinearGradient, QColor, QPalette, QPainter, QPen, QBrush, QRadialGradient, QConicalGradient
import math
import random

from src.animation.sword_tomato_anim import SwordTomatoAnim


class WelcomeBannerWidget(QWidget):
    """Enhanced game-like welcome banner with multiple animations and styling"""
    
    def __init__(self, title: str = "DoroLexus", subtitle: str = "Master Your Vocabulary Journey", parent=None):
        super().__init__(parent)
        self.title_text = title
        self.subtitle_text = subtitle
        self.init_ui()
        self.setup_animations()

    def init_ui(self):
        """Initialize the banner UI with game-like styling"""
        self.setFixedHeight(180)  # Compact height
        self.setFixedWidth(720)
        
        # Set size policy to ensure centering
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Enhanced game-like banner styling with animated gradient
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(37, 99, 235, 0.95),
                    stop:0.2 rgba(59, 130, 246, 0.9),
                    stop:0.4 rgba(5, 150, 105, 0.88),
                    stop:0.6 rgba(16, 185, 129, 0.85),
                    stop:0.8 rgba(217, 119, 6, 0.82),
                    stop:1 rgba(37, 99, 235, 0.75));
                border-radius: 25px;
                border: 3px solid rgba(255, 255, 255, 0.3);
                outline: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 15, 40, 10)  # Compact margins
        layout.setSpacing(8)  # Reduced spacing
        layout.setAlignment(Qt.AlignCenter)
        
        # Enhanced main title with animated effects
        self.title_label = QLabel("")  # Start empty for typewriter effect
        title_font = QFont()
        title_font.setPointSize(46)  # Large title
        title_font.setBold(True)
        title_font.setFamily("Cascadia Code")
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
                font-weight: 700;
                font-size: 46px;  /* Explicit size to override global QLabel */
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        
        # Add animated glow effect to title
        title_glow = QGraphicsDropShadowEffect()
        title_glow.setBlurRadius(20)
        title_glow.setColor(QColor(255, 255, 255, 150))
        title_glow.setOffset(0, 0)
        self.title_label.setGraphicsEffect(title_glow)
        
        layout.addWidget(self.title_label)
        
        # Enhanced subtitle with animated effects
        self.subtitle_label = QLabel("")  # Start empty for typewriter effect
        subtitle_font = QFont()
        subtitle_font.setPointSize(22)  # Large subtitle
        subtitle_font.setItalic(True)
        subtitle_font.setFamily("Cascadia Code")
        self.subtitle_label.setFont(subtitle_font)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.95);
                background: transparent;
                border: none;
                outline: none;
                padding: 0px;
                margin: 0px;
                font-weight: 500;
                font-size: 22px;  /* Explicit size to override global QLabel */
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        
        # Add subtle glow to subtitle
        subtitle_glow = QGraphicsDropShadowEffect()
        subtitle_glow.setBlurRadius(10)
        subtitle_glow.setColor(QColor(255, 255, 255, 80))
        subtitle_glow.setOffset(0, 0)
        self.subtitle_label.setGraphicsEffect(subtitle_glow)
        
        layout.addWidget(self.subtitle_label)

        # Sword -> Tomato animation centered under subtitle
        anim_row = QHBoxLayout()
        anim_row.setAlignment(Qt.AlignCenter)
        self.sword_tomato = SwordTomatoAnim(size=36)  # Larger animation
        self.sword_tomato.setStyleSheet("background: transparent; border: none; outline: none;")
        anim_row.addWidget(self.sword_tomato)
        layout.addLayout(anim_row)
        
        # Enhanced progress indicator dots with animations
        dots_layout = QHBoxLayout()
        dots_layout.setAlignment(Qt.AlignCenter)
        dots_layout.setSpacing(12)
        
        self.dots = []
        for i in range(5):  # Progress dots
            dot = QLabel("●")
            dot.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.3);
                    font-size: 18px;
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
        
        # Add animated border elements
        self.border_timer = QTimer()
        self.border_timer.timeout.connect(self.animate_border)
        self.border_phase = 0
        
        # Enhanced shadow effect with animation
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setBlurRadius(30)
        self.shadow_effect.setOffset(0, 10)
        self.shadow_effect.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(self.shadow_effect)
        
        # Add rainbow border effect
        self.rainbow_timer = QTimer()
        self.rainbow_timer.timeout.connect(self.animate_rainbow_border)
        self.rainbow_phase = 0

    def setup_animations(self):
        """Setup multiple coordinated animations"""
        # Slide in animation with bounce
        self.slide_anim = QPropertyAnimation(self, b"geometry")
        self.slide_anim.setDuration(1000)
        self.slide_anim.setEasingCurve(QEasingCurve.OutBounce)
        
        # Scale animation for dramatic entrance
        self.scale_anim = QPropertyAnimation(self, b"geometry")
        self.scale_anim.setDuration(1200)
        self.scale_anim.setEasingCurve(QEasingCurve.OutElastic)
        
        # Title typewriter effect
        self.title_timer = QTimer()
        self.title_timer.timeout.connect(self.typewriter_title)
        self.title_index = 0
        
        # Subtitle typewriter effect
        self.subtitle_timer = QTimer()
        self.subtitle_timer.timeout.connect(self.typewriter_subtitle)
        self.subtitle_index = 0
        
        # Dot pulse animation timer
        self.dot_timer = QTimer()
        self.dot_timer.timeout.connect(self.animate_dots)
        self.current_dot = 0
        
        # Glow pulse animation
        self.glow_timer = QTimer()
        self.glow_timer.timeout.connect(self.animate_glow)
        self.glow_phase = 0
        
        # Shadow pulse animation
        self.shadow_timer = QTimer()
        self.shadow_timer.timeout.connect(self.animate_shadow)
        self.shadow_phase = 0

    def play(self):
        """Start the welcome banner animations"""
        # Ensure proper geometry setup before animation
        self.setFixedSize(720, 180)
        self.updateGeometry()
        
        # Get parent widget dimensions for proper centering
        if self.parent():
            parent_width = self.parent().width()
            x_center = max(0, (parent_width - 720) // 2)
        else:
            x_center = 0
        
        # Get initial geometry with proper centering
        w = 720
        h = 180
        
        # Start from above the screen with proper horizontal centering
        start_rect = QRect(x_center, -h - 20, w, h)
        end_rect = QRect(x_center, 0, w, h)
        
        self.setGeometry(start_rect)
        self.slide_anim.setStartValue(start_rect)
        self.slide_anim.setEndValue(end_rect)
        
        # Start slide animation
        self.slide_anim.start()
        
        # Start typewriter effects with delays
        QTimer.singleShot(500, self.start_title_typewriter)
        QTimer.singleShot(1200, self.start_subtitle_typewriter)
        
        # Start other animations after slide completes
        QTimer.singleShot(1100, self.start_dot_animation)
        QTimer.singleShot(1100, self.sword_tomato.play)
        QTimer.singleShot(1100, self.start_glow_animation)
        QTimer.singleShot(1100, self.start_shadow_animation)
        QTimer.singleShot(1100, self.start_rainbow_animation)
        QTimer.singleShot(1100, self.start_border_animation)

    def start_title_typewriter(self):
        """Start typewriter effect for title"""
        self.title_index = 0
        self.title_timer.start(100)  # 100ms per character
        
    def typewriter_title(self):
        """Typewriter effect for title"""
        if self.title_index < len(self.title_text):
            self.title_label.setText(self.title_text[:self.title_index + 1])
            self.title_index += 1
        else:
            self.title_timer.stop()
            
    def start_subtitle_typewriter(self):
        """Start typewriter effect for subtitle"""
        self.subtitle_index = 0
        self.subtitle_timer.start(80)  # 80ms per character
        
    def typewriter_subtitle(self):
        """Typewriter effect for subtitle"""
        if self.subtitle_index < len(self.subtitle_text):
            self.subtitle_label.setText(self.subtitle_text[:self.subtitle_index + 1])
            self.subtitle_index += 1
        else:
            self.subtitle_timer.stop()
            
    def start_dot_animation(self):
        """Start the pulsing dot animation"""
        self.dot_timer.start(500)  # Pulse every 500ms

    def animate_dots(self):
        """Animate the progress dots with enhanced effects"""
        # Reset all dots
        for i, dot in enumerate(self.dots):
            if i == self.current_dot:
                # Current dot - bright and larger
                dot.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 22px;
                        background: transparent;
                    }
                """)
            elif i == (self.current_dot - 1) % len(self.dots):
                # Previous dot - medium brightness
                dot.setStyleSheet("""
                    QLabel {
                        color: rgba(255, 255, 255, 0.7);
                        font-size: 20px;
                        background: transparent;
                    }
                """)
            else:
                # Other dots - dim
                dot.setStyleSheet("""
                    QLabel {
                        color: rgba(255, 255, 255, 0.3);
                        font-size: 18px;
                        background: transparent;
                    }
                """)
        
        self.current_dot = (self.current_dot + 1) % len(self.dots)
        
    def start_glow_animation(self):
        """Start glow pulse animation"""
        self.glow_timer.start(100)  # 100ms updates
        
    def animate_glow(self):
        """Animate glow effects"""
        self.glow_phase += 0.1
        intensity = int(100 + 50 * math.sin(self.glow_phase))
        
        # Update title glow
        title_glow = self.title_label.graphicsEffect()
        if title_glow:
            title_glow.setBlurRadius(15 + 10 * math.sin(self.glow_phase))
            title_glow.setColor(QColor(255, 255, 255, intensity))
            
        # Update subtitle glow
        subtitle_glow = self.subtitle_label.graphicsEffect()
        if subtitle_glow:
            subtitle_glow.setBlurRadius(8 + 5 * math.sin(self.glow_phase))
            subtitle_glow.setColor(QColor(255, 255, 255, intensity // 2))
            
    def start_shadow_animation(self):
        """Start shadow pulse animation"""
        self.shadow_timer.start(150)  # 150ms updates
        
    def animate_shadow(self):
        """Animate shadow effects"""
        self.shadow_phase += 0.08
        blur = int(25 + 10 * math.sin(self.shadow_phase))
        offset = int(8 + 3 * math.cos(self.shadow_phase))
        opacity = int(100 + 20 * math.sin(self.shadow_phase * 1.5))
        
        self.shadow_effect.setBlurRadius(blur)
        self.shadow_effect.setOffset(0, offset)
        self.shadow_effect.setColor(QColor(0, 0, 0, opacity))
        
    def start_rainbow_animation(self):
        """Start rainbow border animation"""
        self.rainbow_timer.start(50)  # 50ms updates for smooth rainbow
        
    def animate_rainbow_border(self):
        """Animate rainbow border effect"""
        self.rainbow_phase += 0.05
        hue = int((self.rainbow_phase * 360) % 360)
        
        # Create rainbow gradient
        gradient = QConicalGradient(375, 120, 0)  # Center of banner
        for i in range(6):
            angle = (i * 60 + self.rainbow_phase * 360) % 360
            color = QColor.fromHsv(int(angle) % 360, 255, 255, 150)
            gradient.setColorAt(i / 5.0, color)
            
        # Update border color
        border_color = QColor.fromHsv(hue, 255, 255, 200)
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(37, 99, 235, 0.95),
                    stop:0.2 rgba(59, 130, 246, 0.9),
                    stop:0.4 rgba(5, 150, 105, 0.88),
                    stop:0.6 rgba(16, 185, 129, 0.85),
                    stop:0.8 rgba(217, 119, 6, 0.82),
                    stop:1 rgba(37, 99, 235, 0.75));
                border-radius: 25px;
                border: 3px solid {border_color.name()};
                outline: none;
            }}
        """)
        
    def start_border_animation(self):
        """Start border animation"""
        self.border_timer.start(200)  # 200ms updates
        
    def animate_border(self):
        """Animate border effects"""
        self.border_phase += 0.1
        # Add subtle pulsing effect to border radius
        radius = int(22 + 3 * math.sin(self.border_phase))
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(37, 99, 235, 0.95),
                    stop:0.2 rgba(59, 130, 246, 0.9),
                    stop:0.4 rgba(5, 150, 105, 0.88),
                    stop:0.6 rgba(16, 185, 129, 0.85),
                    stop:0.8 rgba(217, 119, 6, 0.82),
                    stop:1 rgba(37, 99, 235, 0.75));
                border-radius: {radius}px;
                border: 3px solid rgba(255, 255, 255, 0.3);
                outline: none;
            }}
        """)

    def stop_animations(self):
        """Stop all animations"""
        if self.dot_timer.isActive():
            self.dot_timer.stop()
        if self.title_timer.isActive():
            self.title_timer.stop()
        if self.subtitle_timer.isActive():
            self.subtitle_timer.stop()
        if self.glow_timer.isActive():
            self.glow_timer.stop()
        if self.shadow_timer.isActive():
            self.shadow_timer.stop()
        if self.rainbow_timer.isActive():
            self.rainbow_timer.stop()
        if self.border_timer.isActive():
            self.border_timer.stop()
            
    def showEvent(self, event):
        """Handle show event to ensure proper positioning"""
        super().showEvent(event)
        # Ensure the widget is properly sized when shown
        self.setFixedSize(720, 180)
        self.updateGeometry()
        
    def resizeEvent(self, event):
        """Handle resize event to maintain fixed size"""
        super().resizeEvent(event)
        # Ensure banner maintains its fixed size
        if self.size() != self.sizeHint():
            self.setFixedSize(720, 180)
