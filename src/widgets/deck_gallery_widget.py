"""
Modular Deck Gallery Widget - Reusable component for deck display and management
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QScrollArea, QGraphicsDropShadowEffect, QPushButton)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from PySide6.QtGui import QColor
from src.ui.responsive_grid_layout import ResponsiveGridLayout
from enum import Enum


class DeckGalleryMode(Enum):
    """Different modes for the deck gallery"""
    STUDY = "study"           # For study page - multi-select, preview, sword theme
    MANAGEMENT = "management" # For deck management - edit, delete, create
    SELECTION = "selection"   # Simple selection mode


class DeckGalleryWidget(QWidget):
    """
    Modular deck gallery widget that can be configured for different use cases:
    - Study Mode: Multi-selection, preview cards, sword theme
    - Management Mode: Create, edit, delete decks
    - Selection Mode: Simple single selection
    """
    
    # Unified signals for all modes
    deck_selected = Signal(int)        # Deck selected/deselected (study) or single selection
    deck_preview = Signal(int)         # Request to preview deck cards
    deck_edit = Signal(int)           # Request to edit deck (management)
    deck_delete = Signal(int)         # Request to delete deck (management)
    deck_create = Signal()            # Request to create new deck (management)
    selection_changed = Signal(list)  # Emitted when selection changes (list of deck IDs)
    
    def __init__(self, mode=DeckGalleryMode.STUDY, title="", show_title=True, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.title_text = title
        self.show_title = show_title
        self.deck_cards = []
        self.deck_id_to_name = {}
        self._decks_cache = []
        self.selected_deck_ids = set()
        
        # Animation attributes
        self._animation_timer = None
        self._glow_phase = 0
        self._shadow_effect = None
        self._typing_timer = None
        self._typing_index = 0
        self._is_visible = False
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the deck gallery UI based on mode"""
        self.setStyleSheet("""
            DeckGalleryWidget {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Title section (optional)
        if self.show_title:
            self._create_title_section(layout)
        
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
        
    def _create_title_section(self, parent_layout):
        """Create the title section based on mode"""
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)
        
        if self.mode == DeckGalleryMode.STUDY:
            # Animated typing title for study mode
            self.title_label = QLabel("")
            self.title_label.setAlignment(Qt.AlignCenter)
            self._typing_text = self.title_text or "⚔️ Choose Your Weapon ⚔️"
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
        else:
            # Static title for other modes
            display_title = self.title_text or "Deck Gallery"
            self.title_label = QLabel(display_title)
            self.title_label.setAlignment(Qt.AlignCenter)
            self.title_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.9);
                    font-size: 20px;
                    font-weight: bold;
                    background: transparent;
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                    margin: 15px 0px;
                    padding: 0px;
                }
            """)
        
        title_layout.addWidget(self.title_label)
        parent_layout.addLayout(title_layout)
        
    def refresh_decks(self, decks):
        """Refresh the deck gallery with new deck data"""
        self._decks_cache = decks or []
        
        # Clear existing cards
        for card in self.deck_cards:
            card.deleteLater()
        self.deck_cards.clear()
        self.deck_cards_layout.clear_cards()
        self.selected_deck_ids.clear()
        
        if not decks:
            # Show no decks message
            self._show_no_decks_message()
            return
        
        # Store deck names for reference
        self.deck_id_to_name = {deck['id']: deck['name'] for deck in self._decks_cache}
        
        # Add create deck card for management mode
        if self.mode == DeckGalleryMode.MANAGEMENT:
            self._add_create_deck_card()
        
        # Create and add deck cards based on mode
        for deck in self._decks_cache:
            deck_card = self._create_deck_card(deck)
            if deck_card:
                self.deck_cards.append(deck_card)
                self.deck_cards_layout.add_card(deck_card)
        
        # Force layout update
        self.deck_cards_layout._recalculate_layout()
        
    def _show_no_decks_message(self):
        """Show a message when no decks are available"""
        if self.mode == DeckGalleryMode.MANAGEMENT:
            message = "No decks yet. Create your first deck!"
        else:
            message = "No decks available. Create some decks first!"
            
        no_decks_label = QLabel(message)
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
        no_decks_label.move(50, 50)
        
    def _add_create_deck_card(self):
        """Add create deck card for management mode"""
        from src.widgets.deck_card_widgets import CreateDeckCardWidget
        create_card = CreateDeckCardWidget()
        create_card.create_deck.connect(self.deck_create.emit)
        self.deck_cards.append(create_card)
        self.deck_cards_layout.add_card(create_card)
        
    def _create_deck_card(self, deck):
        """Create a deck card widget based on the current mode"""
        if self.mode == DeckGalleryMode.STUDY:
            from src.widgets.deck_card_widgets import StudyDeckCardWidget
            card = StudyDeckCardWidget(deck)
            card.deck_selected.connect(self._handle_deck_selection)
            card.preview_requested.connect(self.deck_preview.emit)
            return card
            
        elif self.mode == DeckGalleryMode.MANAGEMENT:
            from src.widgets.deck_card_widgets import ManagementDeckCardWidget
            card = ManagementDeckCardWidget(deck)
            card.deck_selected.connect(self.deck_selected.emit)
            card.edit_deck.connect(self.deck_edit.emit)
            card.delete_deck.connect(self.deck_delete.emit)
            return card
            
        elif self.mode == DeckGalleryMode.SELECTION:
            from src.widgets.deck_card_widgets import SelectionDeckCardWidget
            card = SelectionDeckCardWidget(deck)
            card.deck_selected.connect(self.deck_selected.emit)
            return card
            
        return None
        
    def _handle_deck_selection(self, deck_id):
        """Handle deck selection for multi-select modes"""
        if self.mode == DeckGalleryMode.STUDY:
            # Toggle selection
            if deck_id in self.selected_deck_ids:
                self.selected_deck_ids.remove(deck_id)
            else:
                self.selected_deck_ids.add(deck_id)
                
            # Emit signals
            self.deck_selected.emit(deck_id)
            self.selection_changed.emit(list(self.selected_deck_ids))
            
    def clear_selection(self):
        """Clear all deck selections"""
        self.selected_deck_ids.clear()
        for card in self.deck_cards:
            if hasattr(card, 'set_selected'):
                card.set_selected(False)
        self.selection_changed.emit([])
        
    def get_selected_deck_ids(self):
        """Get list of currently selected deck IDs"""
        return list(self.selected_deck_ids)
        
    def set_mode(self, mode: DeckGalleryMode):
        """Change the gallery mode and refresh"""
        if self.mode != mode:
            self.mode = mode
            if hasattr(self, '_decks_cache'):
                self.refresh_decks(self._decks_cache)
                
    def set_title(self, title: str):
        """Update the title text"""
        self.title_text = title
        if hasattr(self, 'title_label'):
            if self.mode == DeckGalleryMode.STUDY:
                self._typing_text = title
                # Restart typing animation if visible
                if self._is_visible:
                    self.start_title_animation()
            else:
                self.title_label.setText(title)
                
    # ==================== ANIMATION METHODS ====================
    
    def start_title_animation(self):
        """Start the typing animation (study mode only)"""
        if self.mode != DeckGalleryMode.STUDY:
            return
            
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
        
        # Apply animated styling
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
        
        if self._shadow_effect:
            self.title_label.setGraphicsEffect(None)
            self._shadow_effect = None
            
    # ==================== EVENT HANDLERS ====================
    
    def resizeEvent(self, event):
        """Handle resize events to update grid layout"""
        super().resizeEvent(event)
        # Trigger grid layout recalculation when the gallery is resized
        if hasattr(self, 'deck_cards_layout') and self.deck_cards_layout:
            self.deck_cards_layout._recalculate_layout()
    
    def showEvent(self, event):
        """Handle widget show event - start animation when visible"""
        super().showEvent(event)
        if not self._is_visible:
            self._is_visible = True
            # Start animation after a short delay to ensure proper rendering
            if self.mode == DeckGalleryMode.STUDY and self.show_title:
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
