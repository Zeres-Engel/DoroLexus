"""
Responsive Grid Layout - Proper responsive positioning for deck cards
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt, Signal, QTimer, QRect, QPoint
from PySide6.QtGui import QPainter, QBrush, QColor


class ResponsiveGridLayout(QWidget):
    """Responsive grid layout that properly positions deck cards"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards = []
        self.card_width = 200
        self.card_height = 120
        self.spacing = 20
        self.margin = 20
        
        # Resize timer for debouncing
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self._recalculate_layout)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the responsive grid UI"""
        self.setStyleSheet("""
            ResponsiveGridLayout {
                background: transparent;
            }
        """)
        
    def add_card(self, card_widget):
        """Add a deck card to the grid"""
        self.cards.append(card_widget)
        card_widget.setParent(self)
        self._recalculate_layout()
        
    def remove_card(self, card_widget):
        """Remove a deck card from the grid"""
        if card_widget in self.cards:
            self.cards.remove(card_widget)
            card_widget.setParent(None)
            self._recalculate_layout()
            
    def clear_cards(self):
        """Clear all cards from the grid"""
        for card in self.cards:
            # Reset position before removing to prevent disturbance
            if hasattr(card, 'reset_position'):
                card.reset_position()
            card.setParent(None)
        self.cards.clear()
        self._recalculate_layout()
        
    def resizeEvent(self, event):
        """Handle resize events with debouncing"""
        super().resizeEvent(event)
        # Only recalculate if the size actually changed significantly
        if not hasattr(self, '_last_width') or abs(self.width() - self._last_width) > 10:
            self._last_width = self.width()
            self.resize_timer.start(50)  # 50ms debounce
        
    def _recalculate_layout(self):
        """Recalculate the grid layout based on available width"""
        if not self.cards:
            return
            
        # Get available width - use parent width if we don't have a width yet
        widget_width = self.width()
        if widget_width <= 0 and self.parent():
            widget_width = self.parent().width()
        if widget_width <= 0:
            widget_width = 800  # Fallback width
            
        available_width = widget_width - (2 * self.margin)
        
        # Calculate how many cards fit per row
        # Formula: (available_width + spacing) / (card_width + spacing)
        cards_per_row = max(1, int((available_width + self.spacing) / (self.card_width + self.spacing)))
        
        # Check if layout actually needs to change
        if hasattr(self, '_last_cards_per_row') and self._last_cards_per_row == cards_per_row and hasattr(self, '_last_card_count') and self._last_card_count == len(self.cards):
            return  # No need to recalculate if the layout hasn't changed
        
        self._last_cards_per_row = cards_per_row
        self._last_card_count = len(self.cards)
        
        # Calculate starting x position to center the row
        total_row_width = (cards_per_row * self.card_width) + ((cards_per_row - 1) * self.spacing)
        start_x = self.margin + max(0, (available_width - total_row_width) // 2)
        
        # Position cards
        current_x = start_x
        current_y = self.margin
        row_count = 0
        
        for i, card in enumerate(self.cards):
            # Check if we need to wrap to next row
            if i > 0 and i % cards_per_row == 0:
                current_y += self.card_height + self.spacing
                current_x = start_x
                row_count += 1
                
            # Position the card
            card.move(QPoint(current_x, current_y))
            current_x += self.card_width + self.spacing
            
        # Update the widget's minimum size
        total_rows = (len(self.cards) + cards_per_row - 1) // cards_per_row
        total_height = self.margin + (total_rows * self.card_height) + ((total_rows - 1) * self.spacing) + self.margin
        self.setMinimumHeight(total_height)
        
        # Set the widget size to match the content
        self.resize(widget_width, total_height)
        
    def get_selected_cards(self):
        """Get list of selected card widgets"""
        return [card for card in self.cards if card.is_deck_selected()]
        
    def clear_selection(self):
        """Clear selection on all cards"""
        for card in self.cards:
            card.set_selected(False)
