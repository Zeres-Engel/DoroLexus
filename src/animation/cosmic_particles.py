"""
Cosmic particle animation with star twinkling effects
"""

import math
import random
from typing import List, Dict, Any
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QBrush, QColor, QRadialGradient, QPen


class CosmicStar:
    """A single cosmic star with twinkling animation"""
    
    def __init__(self, x: float, y: float, width: int, height: int):
        self.x = x
        self.y = y
        self.base_size = random.uniform(0.001, 0.008)  # Even smaller normalized size (0-1)
        self.current_size = self.base_size
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
        self.twinkle_speed = random.uniform(0.02, 0.08)  # Slower, more subtle twinkling
        self.brightness = random.uniform(0.6, 1.0)
        self.color_hue = random.choice([
            0,      # Red
            30,     # Orange
            60,     # Yellow
            180,    # Cyan
            240,    # Blue
            300,    # Magenta
            0       # White (will be overridden)
        ])
        # Some stars are pure white
        if random.random() < 0.3:
            self.is_white = True
        else:
            self.is_white = False
        
        # Slow drift movement
        self.vx = random.uniform(-0.0005, 0.0005)
        self.vy = random.uniform(-0.0005, 0.0005)
        
        # Pulse animation
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.pulse_speed = random.uniform(0.01, 0.04)  # Slower pulse for subtlety
        
        # Complex star properties - simplified for performance
        self.star_type = random.choice(['simple', 'cross', 'diamond', 'sparkle', 'complex', 'crystal'])
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.01, 0.01)  # Slower rotation
        self.complexity_level = random.randint(1, 3)  # Reduced complexity range
        self.secondary_color = random.choice([0, 60, 120, 180, 240, 300])  # For dual-color stars
        self.pattern_phase = random.uniform(0, 2 * math.pi)  # For animated patterns
        self.detail_count = random.randint(2, 6)  # Reduced detail count
        
        self.width = width
        self.height = height
        
    def update(self):
        """Update star animation"""
        # Twinkle effect - more subtle
        self.twinkle_phase += self.twinkle_speed
        twinkle_factor = 0.7 + 0.3 * math.sin(self.twinkle_phase)  # Less dramatic variation
        
        # Pulse effect - more subtle
        self.pulse_phase += self.pulse_speed
        pulse_factor = 0.9 + 0.1 * math.sin(self.pulse_phase)  # Very subtle pulse
        
        # Combine effects
        self.current_size = self.base_size * twinkle_factor * pulse_factor
        
        # Update rotation for complex patterns
        self.rotation += self.rotation_speed
        
        # Update pattern animation phase
        self.pattern_phase += self.twinkle_speed * 0.5
        
        # Slow drift
        self.x += self.vx
        self.y += self.vy
        
        # Wrap around screen
        if self.x < 0:
            self.x = 1
        elif self.x > 1:
            self.x = 0
        if self.y < 0:
            self.y = 1
        elif self.y > 1:
            self.y = 0
    
    def get_color(self) -> QColor:
        """Get the star's color with twinkling brightness"""
        if self.is_white:
            alpha = int(255 * self.brightness * (0.8 + 0.2 * math.sin(self.twinkle_phase)))  # More stable brightness
            return QColor(255, 255, 255, alpha)
        else:
            # Convert HSV to RGB for colored stars
            saturation = random.uniform(0.7, 1.0)
            value = self.brightness * (0.85 + 0.15 * math.sin(self.twinkle_phase))  # Less brightness variation
            color = QColor.fromHsvF(self.color_hue / 360.0, saturation, value)
            color.setAlphaF(0.8)  # Slightly more transparent
            return color


class ShootingStar:
    """Occasional shooting star effect"""
    
    def __init__(self, width: int, height: int):
        # Start from random edge
        edge = random.randint(0, 3)
        if edge == 0:  # Top
            self.x = random.uniform(0, 1)
            self.y = 0
            self.vx = random.uniform(-0.01, 0.01)
            self.vy = random.uniform(0.01, 0.03)
        elif edge == 1:  # Right
            self.x = 1
            self.y = random.uniform(0, 1)
            self.vx = random.uniform(-0.03, -0.01)
            self.vy = random.uniform(-0.01, 0.01)
        elif edge == 2:  # Bottom
            self.x = random.uniform(0, 1)
            self.y = 1
            self.vx = random.uniform(-0.01, 0.01)
            self.vy = random.uniform(-0.03, -0.01)
        else:  # Left
            self.x = 0
            self.y = random.uniform(0, 1)
            self.vx = random.uniform(0.01, 0.03)
            self.vy = random.uniform(-0.01, 0.01)
        
        self.life = 1.0
        self.trail_points = []
        self.width = width
        self.height = height
        
    def update(self) -> bool:
        """Update shooting star. Returns True if still alive."""
        self.trail_points.append((self.x, self.y))
        if len(self.trail_points) > 8:
            self.trail_points.pop(0)
            
        self.x += self.vx
        self.y += self.vy
        self.life -= 0.02
        
        return self.life > 0 and 0 <= self.x <= 1 and 0 <= self.y <= 1


class CosmicParticleSystem(QWidget):
    """Cosmic particle system with twinkling stars and shooting stars"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setStyleSheet("background: transparent;")
        
        self.stars: List[CosmicStar] = []
        self.shooting_stars: List[ShootingStar] = []
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)  # 20 FPS
        
        # Shooting star timer
        self.shooting_timer = QTimer(self)
        self.shooting_timer.timeout.connect(self.create_shooting_star)
        self.shooting_timer.start(random.randint(3000, 8000))  # Every 3-8 seconds
        
        self.create_stars()
        
    def create_stars(self):
        """Create initial stars"""
        # Create many small twinkling stars
        star_count = 60  # Reduced for performance
        for _ in range(star_count):
            star = CosmicStar(
                random.uniform(0, 1),
                random.uniform(0, 1),
                self.width() or 1000,
                self.height() or 700
            )
            self.stars.append(star)
    
    def create_shooting_star(self):
        """Create a new shooting star"""
        if len(self.shooting_stars) < 2:  # Limit concurrent shooting stars
            shooting_star = ShootingStar(self.width() or 1000, self.height() or 700)
            self.shooting_stars.append(shooting_star)
        
        # Schedule next shooting star
        self.shooting_timer.start(random.randint(3000, 8000))
    
    def update_animation(self):
        """Update all particles"""
        # Update stars
        for star in self.stars:
            star.update()
            
        # Update shooting stars
        self.shooting_stars = [star for star in self.shooting_stars if star.update()]
        
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        """Paint the cosmic particles"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get widget dimensions
        width = self.width()
        height = self.height()
        
        # Draw twinkling stars
        for star in self.stars:
            self.draw_star(painter, star, width, height)
            
        # Draw shooting stars
        for shooting_star in self.shooting_stars:
            self.draw_shooting_star(painter, shooting_star, width, height)
    
    def draw_star(self, painter: QPainter, star: CosmicStar, width: int, height: int):
        """Draw a complex twinkling star with intricate patterns"""
        # Convert normalized coordinates to pixels
        x = int(star.x * width)
        y = int(star.y * height)
        size = max(2, int(star.current_size * min(width, height)))
        
        color = star.get_color()
        
        # Save painter state for transformations
        painter.save()
        painter.translate(x, y)
        painter.rotate(math.degrees(star.rotation))
        
        # Draw complex star based on type - simplified for performance
        if star.star_type == 'simple':
            self._draw_simple_star(painter, star, size, color)
        elif star.star_type == 'cross':
            self._draw_cross_star(painter, star, size, color)
        elif star.star_type == 'diamond':
            self._draw_diamond_star(painter, star, size, color)
        elif star.star_type == 'sparkle':
            self._draw_sparkle_star(painter, star, size, color)
        elif star.star_type == 'complex':
            self._draw_complex_star(painter, star, size, color)
        elif star.star_type == 'crystal':
            self._draw_crystal_star(painter, star, size, color)
        
        painter.restore()
    
    def _draw_simple_star(self, painter: QPainter, star: CosmicStar, size: int, color: QColor):
        """Draw a simple star with subtle glow"""
        # Glow effect
        glow_size = size * 1.5
        gradient = QRadialGradient(0, 0, glow_size)
        center_color = QColor(color)
        center_color.setAlphaF(color.alphaF() * 0.6)
        gradient.setColorAt(0.0, center_color)
        gradient.setColorAt(1.0, QColor(color.red(), color.green(), color.blue(), 0))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-glow_size, -glow_size, glow_size * 2, glow_size * 2)
        
        # Center dot
        painter.setBrush(QBrush(color))
        painter.drawEllipse(-size//2, -size//2, size, size)
    
    def _draw_cross_star(self, painter: QPainter, star: CosmicStar, size: int, color: QColor):
        """Draw a cross-shaped star with intricate details"""
        pen = QPen(color)
        pen.setWidth(max(1, size // 4))
        painter.setPen(pen)
        
        # Main cross
        painter.drawLine(0, -size*2, 0, size*2)
        painter.drawLine(-size*2, 0, size*2, 0)
        
        # Additional detail lines for complexity
        if star.complexity_level > 1:
            smaller_size = size * 0.6
            painter.drawLine(0, -smaller_size, 0, smaller_size)
            painter.drawLine(-smaller_size, 0, smaller_size, 0)
        
        # Center glow
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-size//3, -size//3, size//3*2, size//3*2)
    
    def _draw_diamond_star(self, painter: QPainter, star: CosmicStar, size: int, color: QColor):
        """Draw a diamond-shaped star with geometric precision"""
        # Outer diamond
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        
        from PySide6.QtCore import QPoint
        points = [
            QPoint(0, -size*2),      # Top
            QPoint(size*2, 0),       # Right
            QPoint(0, size*2),       # Bottom
            QPoint(-size*2, 0)       # Left
        ]
        painter.drawPolygon(points)
        
        # Inner diamond for complexity
        if star.complexity_level > 1:
            inner_size = size
            secondary_color = QColor.fromHsvF(star.secondary_color / 360.0, 0.8, 0.9)
            secondary_color.setAlphaF(0.7)
            painter.setBrush(QBrush(secondary_color))
            
            inner_points = [
                QPoint(0, -inner_size),
                QPoint(inner_size, 0),
                QPoint(0, inner_size),
                QPoint(-inner_size, 0)
            ]
            painter.drawPolygon(inner_points)
    
    def _draw_sparkle_star(self, painter: QPainter, star: CosmicStar, size: int, color: QColor):
        """Draw an 8-pointed sparkle star"""
        pen = QPen(color)
        pen.setWidth(max(1, size // 3))
        painter.setPen(pen)
        
        # 8 rays at different angles
        for i in range(8):
            angle = i * math.pi / 4
            end_x = int(size * 2 * math.cos(angle))
            end_y = int(size * 2 * math.sin(angle))
            
            # Vary ray length based on complexity
            length_factor = 0.5 + (star.complexity_level / 8.0)
            end_x = int(end_x * length_factor)
            end_y = int(end_y * length_factor)
            
            painter.drawLine(0, 0, end_x, end_y)
        
        # Center bright dot
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        center_size = max(2, size//2)
        painter.drawEllipse(-center_size//2, -center_size//2, center_size, center_size)
    
    def _draw_complex_star(self, painter: QPainter, star: CosmicStar, size: int, color: QColor):
        """Draw a complex multi-layered star"""
        # Multiple concentric patterns
        layers = min(star.complexity_level, 3)
        
        for layer in range(layers):
            layer_size = size * (1 - layer * 0.3)
            layer_alpha = 1.0 - layer * 0.3
            
            layer_color = QColor(color)
            layer_color.setAlphaF(max(0.0, color.alphaF() * layer_alpha))
            
            pen = QPen(layer_color)
            pen.setWidth(max(1, int(layer_size // 4)))
            painter.setPen(pen)
            
            # Draw star pattern for this layer
            points = 12 if layer == 0 else 8 if layer == 1 else 6
            for i in range(points):
                angle = i * 2 * math.pi / points
                end_x = int(layer_size * 1.5 * math.cos(angle))
                end_y = int(layer_size * 1.5 * math.sin(angle))
                painter.drawLine(0, 0, end_x, end_y)
        
        # Bright center
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-size//3, -size//3, size//3*2, size//3*2)
    
    def _draw_mandala_star(self, painter: QPainter, star: CosmicStar, size: int, color: QColor):
        """Draw a mandala-style star with intricate circular patterns"""
        # Outer ring of petals
        petal_count = 8 + star.complexity_level * 2
        
        for i in range(petal_count):
            angle = i * 2 * math.pi / petal_count
            
            # Create petal shape
            petal_x = int(size * 1.5 * math.cos(angle))
            petal_y = int(size * 1.5 * math.sin(angle))
            
            # Petal color varies
            petal_color = QColor(color)
            hue_shift = (i * 360 / petal_count) % 360
            if not star.is_white:
                petal_color = QColor.fromHsvF(hue_shift / 360.0, 0.7, 0.9)
                petal_color.setAlphaF(0.6)
            
            painter.setBrush(QBrush(petal_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(petal_x - size//4, petal_y - size//4, size//2, size//2)
        
        # Inner mandala circles
        for ring in range(1, star.complexity_level + 1):
            ring_radius = size * 0.8 / ring
            ring_color = QColor(color)
            ring_color.setAlphaF(max(0.0, color.alphaF() * (1.0 - ring * 0.2)))
            
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(ring_color, max(1, size // 6)))
            painter.drawEllipse(-ring_radius, -ring_radius, ring_radius * 2, ring_radius * 2)
        
        # Central bright core
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-size//4, -size//4, size//2, size//2)
    
    def _draw_crystal_star(self, painter: QPainter, star: CosmicStar, size: int, color: QColor):
        """Draw a crystalline star with faceted appearance"""
        from PySide6.QtCore import QPoint
        
        # Create crystal facets
        facet_count = 6 + star.complexity_level
        
        for i in range(facet_count):
            angle1 = i * 2 * math.pi / facet_count
            angle2 = (i + 1) * 2 * math.pi / facet_count
            
            # Outer points
            x1 = int(size * 2 * math.cos(angle1))
            y1 = int(size * 2 * math.sin(angle1))
            x2 = int(size * 2 * math.cos(angle2))
            y2 = int(size * 2 * math.sin(angle2))
            
            # Inner points (creating facet effect)
            inner_x1 = int(size * 0.5 * math.cos(angle1))
            inner_y1 = int(size * 0.5 * math.sin(angle1))
            inner_x2 = int(size * 0.5 * math.cos(angle2))
            inner_y2 = int(size * 0.5 * math.sin(angle2))
            
            # Facet color varies for crystal effect
            facet_brightness = 0.5 + 0.5 * math.sin(angle1 + star.rotation)
            facet_color = QColor(color)
            facet_color.setAlphaF(color.alphaF() * facet_brightness)
            
            # Draw facet
            points = [
                QPoint(0, 0),          # Center
                QPoint(x1, y1),        # Outer point 1
                QPoint(x2, y2),        # Outer point 2
            ]
            
            painter.setBrush(QBrush(facet_color))
            painter.setPen(Qt.NoPen)
            painter.drawPolygon(points)
            
            # Draw facet edges for definition
            edge_color = QColor(color)
            edge_color.setAlphaF(color.alphaF() * 0.8)
            painter.setPen(QPen(edge_color, 1))
            painter.drawLine(x1, y1, x2, y2)
        
        # Central crystal core
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-size//3, -size//3, size//3*2, size//3*2)
    
    
    def draw_shooting_star(self, painter: QPainter, shooting_star: ShootingStar, width: int, height: int):
        """Draw a shooting star with trail"""
        if not shooting_star.trail_points:
            return
            
        # Draw trail
        for i, (trail_x, trail_y) in enumerate(shooting_star.trail_points):
            alpha = (i + 1) / len(shooting_star.trail_points) * shooting_star.life
            color = QColor(255, 255, 255, int(255 * alpha * 0.6))
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            
            x = int(trail_x * width)
            y = int(trail_y * height)
            size = int(alpha * 8)
            
            painter.drawEllipse(x - size // 2, y - size // 2, size, size)
        
        # Draw bright head
        head_color = QColor(255, 255, 255, int(255 * shooting_star.life))
        painter.setBrush(QBrush(head_color))
        painter.setPen(Qt.NoPen)
        
        x = int(shooting_star.x * width)
        y = int(shooting_star.y * height)
        size = 12
        
        painter.drawEllipse(x - size // 2, y - size // 2, size, size)
    
    def resizeEvent(self, event):
        """Handle resize to update star coordinates"""
        super().resizeEvent(event)
        # Update star dimensions
        for star in self.stars:
            star.width = self.width()
            star.height = self.height()
        for shooting_star in self.shooting_stars:
            shooting_star.width = self.width()
            shooting_star.height = self.height()
