"""
Responsive Deck Gallery Layout - Independent deck gallery with title
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QScrollArea, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QTimer, QRect, QPoint
from PySide6.QtGui import QColor
from src.widgets.responsive_deck_card_widget import ResponsiveDeckCardWidget
from src.ui.responsive_grid_layout import ResponsiveGridLayout


class ResponsiveDeckGalleryLayout(QWidget):
    """Responsive deck gallery with title and independent responsive grid"""
    
    deck_selected = Signal(int)  # For deck selection/deselection
    preview_requested = Signal(int)  # For deck preview
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.deck_cards = []
        self.deck_id_to_name = {}
        self._decks_cache = []
        self._animation_timer = None
        self._glow_phase = 0
        self._slide_animation = None
        self._shadow_effect = None
        self._typing_timer = None
        self._typing_index = 0
        self._is_visible = False
        self.init_ui()
        # Don't start animation immediately - wait for show event
        
    def init_ui(self):
        """Initialize the responsive deck gallery UI"""
        self.setStyleSheet("""
            ResponsiveDeckGalleryLayout {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Title section
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)
        
        # Main title - Typing animation with sword theme
        self.title_label = QLabel("")
        self.title_label.setAlignment(Qt.AlignCenter)
        self._typing_text = "⚔️ Choose Your Weapon ⚔️"
        self._typing_index = 0
        self._typing_timer = None
        self.title_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 215, 0, 0.9);
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                border: none;
                outline: none;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                margin: 15px 0px;
                padding: 0px;
                letter-spacing: 2px;
            }
        """)
        title_layout.addWidget(self.title_label)
        
        layout.addLayout(title_layout)
        
        # Scroll area for deck cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: rgba(255, 255, 255, 0.1);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(255, 255, 255, 0.5);
            }
        """)
        
        # Deck cards container with responsive grid
        self.deck_cards_widget = QWidget()
        self.deck_cards_layout = ResponsiveGridLayout()
        
        # Add the grid layout to the widget
        widget_layout = QVBoxLayout(self.deck_cards_widget)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.addWidget(self.deck_cards_layout)
        
        # Set up the scroll area
        scroll_area.setWidget(self.deck_cards_widget)
        layout.addWidget(scroll_area)
        
        # Store reference to scroll area for resize handling
        self.scroll_area = scroll_area
        
    def resizeEvent(self, event):
        """Handle resize events to update grid layout"""
        super().resizeEvent(event)
        # Trigger grid layout recalculation when the gallery is resized
        if hasattr(self, 'deck_cards_layout') and self.deck_cards_layout:
            self.deck_cards_layout._recalculate_layout()
        
    def refresh_decks(self, decks):
        """Refresh the deck gallery with new deck data"""
        self._decks_cache = decks or []
        
        # Clear existing cards
        for card in self.deck_cards:
            card.deleteLater()
        self.deck_cards.clear()
        self.deck_cards_layout.clear_cards()
        
        if not decks:
            # Show no decks message
            no_decks_label = QLabel("No decks available. Create some decks first!")
            no_decks_label.setAlignment(Qt.AlignCenter)
            no_decks_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.6);
                    font-size: 16px;
                    background: transparent;
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                }
            """)
            no_decks_label.setParent(self.deck_cards_widget)
            no_decks_label.move(50, 50)  # Simple positioning for no decks message
            return
        
        # Store deck names for reference
        self.deck_id_to_name = {deck['id']: deck['name'] for deck in self._decks_cache}
        
        # Create and add deck cards to responsive grid
        for deck in self._decks_cache:
            deck_card = ResponsiveDeckCardWidget(deck)
            deck_card.deck_selected.connect(self.deck_selected.emit)
            deck_card.preview_requested.connect(self.preview_requested.emit)
            self.deck_cards.append(deck_card)
            self.deck_cards_layout.add_card(deck_card)
        
        # Force layout update
        self.deck_cards_layout._recalculate_layout()
        
    def clear_selection(self):
        """Clear all deck selections"""
        self.deck_cards_layout.clear_selection()
    
    def start_title_animation(self):
        """Start the typing animation"""
        # Reset typing state
        self._typing_index = 0
        self.title_label.setText("")
        
        # Start typing animation
        self._typing_timer = QTimer()
        self._typing_timer.timeout.connect(self._update_typing_animation)
        self._typing_timer.start(100)  # Type every 100ms
    
    def _update_typing_animation(self):
        """Update the typing animation"""
        if self._typing_index < len(self._typing_text):
            # Add next character
            current_text = self._typing_text[:self._typing_index + 1]
            self.title_label.setText(current_text)
            self._typing_index += 1
        else:
            # Typing complete, start pulsing glow
            self._typing_timer.stop()
            self._start_glow_animation()
    
    def _start_glow_animation(self):
        """Start the pulsing glow animation after typing is complete"""
        # Create shadow effect for glow
        self._shadow_effect = QGraphicsDropShadowEffect()
        self._shadow_effect.setBlurRadius(15)
        self._shadow_effect.setOffset(0, 0)
        self.title_label.setGraphicsEffect(self._shadow_effect)
        
        # Start the glow timer
        self._animation_timer = QTimer()
        self._animation_timer.timeout.connect(self._update_title_animation)
        self._animation_timer.start(50)  # 20 FPS
    
    def _update_title_animation(self):
        """Update the title animation with pulsing glow"""
        import math
        
        # Increment glow phase
        self._glow_phase += 0.1
        if self._glow_phase > 2 * math.pi:
            self._glow_phase = 0
        
        # Calculate pulsing values
        pulse_intensity = 0.3 + 0.2 * math.sin(self._glow_phase)
        glow_intensity = 0.7 + 0.3 * math.sin(self._glow_phase * 0.7)
        
        # Create animated colors - Gold theme
        base_color = QColor(255, 215, 0)  # Gold
        glow_color = QColor(255, 69, 0)   # Red-orange glow
        
        # Mix colors based on pulse
        final_color = QColor(
            int(base_color.red() * (1 - pulse_intensity) + glow_color.red() * pulse_intensity),
            int(base_color.green() * (1 - pulse_intensity) + glow_color.green() * pulse_intensity),
            int(base_color.blue() * (1 - pulse_intensity) + glow_color.blue() * pulse_intensity)
        )
        
        # Update shadow effect for glow
        if self._shadow_effect:
            glow_color_with_alpha = QColor(glow_color.red(), glow_color.green(), glow_color.blue(), int(100 * pulse_intensity))
            self._shadow_effect.setColor(glow_color_with_alpha)
            self._shadow_effect.setBlurRadius(int(15 * pulse_intensity))
        
        # Apply animated styling (no box-shadow or text-shadow)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: rgba({final_color.red()}, {final_color.green()}, {final_color.blue()}, {glow_intensity});
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                border: none;
                outline: none;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                margin: 15px 0px;
                padding: 0px;
                letter-spacing: 2px;
            }}
        """)
    
    def stop_title_animation(self):
        """Stop the title animation"""
        if self._animation_timer:
            self._animation_timer.stop()
            self._animation_timer = None
        
        if self._typing_timer:
            self._typing_timer.stop()
            self._typing_timer = None
        
        if self._slide_animation:
            self._slide_animation.stop()
            self._slide_animation = None
        
        if self._shadow_effect:
            self.title_label.setGraphicsEffect(None)
            self._shadow_effect = None
    
    def showEvent(self, event):
        """Handle widget show event - start animation when visible"""
        super().showEvent(event)
        if not self._is_visible:
            self._is_visible = True
            # Start animation after a short delay to ensure proper rendering
            QTimer.singleShot(150, self.start_title_animation)
    
    def hideEvent(self, event):
        """Handle widget hide event - stop animation when hidden"""
        super().hideEvent(event)
        if self._is_visible:
            self._is_visible = False
            self.stop_title_animation()
    
    def closeEvent(self, event):
        """Clean up animation when widget is closed"""
        self.stop_title_animation()
        super().closeEvent(event)
        
    def get_selected_deck_ids(self):
        """Get list of currently selected deck IDs"""
        selected_cards = self.deck_cards_layout.get_selected_cards()
        return [card.get_deck_id() for card in selected_cards]
