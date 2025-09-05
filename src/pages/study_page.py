"""
Study page with dark theme, deck selection, and card deck interface
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QComboBox, QFrame, QScrollArea,
                               QGridLayout, QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter, QBrush, QColor, QPen
from src.modes.study_impl import StudyMode
from src.ui.buttons import PrimaryButton, IconTextButton
import os
from src.core.paths import asset_path


class DeckCard(QFrame):
    """Individual deck card widget"""
    
    deck_selected = Signal(int)  # Emits deck_id when selected
    
    def __init__(self, deck_data, parent=None):
        super().__init__(parent)
        self.deck_id = deck_data['id']
        self.deck_name = deck_data['name']
        self.card_count = deck_data['card_count']
        self.due_count = deck_data.get('due_count', 0)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the deck card UI"""
        self.setFixedSize(200, 120)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            DeckCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 60, 60, 0.9),
                    stop:1 rgba(40, 40, 40, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            DeckCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(80, 80, 80, 0.9),
                    stop:1 rgba(60, 60, 60, 0.9));
                border: 2px solid rgba(100, 200, 255, 0.5);
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Deck name
        name_label = QLabel(self.deck_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Card count info
        count_label = QLabel(f"{self.card_count} cards")
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                background: transparent;
            }
        """)
        layout.addWidget(count_label)
        
        # Due count (if any)
        if self.due_count > 0:
            due_label = QLabel(f"{self.due_count} due")
            due_label.setAlignment(Qt.AlignCenter)
            due_label.setStyleSheet("""
                QLabel {
                    color: #ff6b6b;
                    font-size: 11px;
                    font-weight: bold;
                    background: transparent;
                }
            """)
            layout.addWidget(due_label)
        
        layout.addStretch()
        
    def mousePressEvent(self, event):
        """Handle mouse click to select deck"""
        if event.button() == Qt.LeftButton:
            self.deck_selected.emit(self.deck_id)
        super().mousePressEvent(event)


class StudyPage(QWidget):
    """Study page with deck selection and study interface"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_deck_id = None
        self.deck_cards = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the study page UI"""
        self.setStyleSheet("""
            StudyPage {
                background-color: #1a1a1a;
                color: white;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        self.create_header(layout)
        
        # Content area with stacked widgets
        self.content_stack = QFrame()
        self.content_stack.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        content_layout = QVBoxLayout(self.content_stack)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Deck selection view
        self.deck_selection_widget = self.create_deck_selection()
        content_layout.addWidget(self.deck_selection_widget)
        
        # Study interface view
        self.study_widget = self.create_study_interface()
        content_layout.addWidget(self.study_widget)
        
        layout.addWidget(self.content_stack)
        
        # Initially show deck selection
        self.show_deck_selection()
        
    def create_header(self, layout):
        """Create the page header"""
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("Study Mode")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Back button (initially hidden)
        self.back_btn = PrimaryButton("← Back to Decks")
        self.back_btn.clicked.connect(self.show_deck_selection)
        self.back_btn.setVisible(False)
        header_layout.addWidget(self.back_btn)
        
        layout.addLayout(header_layout)
        
    def create_deck_selection(self):
        """Create the deck selection interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Instructions
        instructions = QLabel("Choose a deck to start studying")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 16px;
                background: transparent;
            }
        """)
        layout.addWidget(instructions)
        
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
        
        # Deck cards container
        self.deck_cards_widget = QWidget()
        self.deck_cards_layout = QGridLayout(self.deck_cards_widget)
        self.deck_cards_layout.setSpacing(20)
        self.deck_cards_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        scroll_area.setWidget(self.deck_cards_widget)
        layout.addWidget(scroll_area)
        
        return widget
        
    def create_study_interface(self):
        """Create the study interface"""
        # Use the existing StudyMode but with dark theme
        self.study_mode = StudyMode(self.db_manager)
        
        # Apply dark theme to study mode
        self.apply_dark_theme_to_study()
        
        return self.study_mode
        
    def apply_dark_theme_to_study(self):
        """Apply dark theme to the study mode"""
        # Update study mode styling
        self.study_mode.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: white;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QComboBox:focus {
                border-color: #64c8ff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 8px;
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QProgressBar {
                background-color: #2d2d2d;
                border: 2px solid #444;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #64c8ff;
                border-radius: 6px;
            }
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:disabled {
                background-color: #333;
                color: #666;
            }
        """)
        
    def load_decks(self):
        """Load available decks"""
        self.deck_cards_widget = QWidget()
        self.deck_cards_layout = QGridLayout(self.deck_cards_widget)
        self.deck_cards_layout.setSpacing(20)
        self.deck_cards_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        # Clear existing cards
        for card in self.deck_cards:
            card.deleteLater()
        self.deck_cards.clear()
        
        # Get decks from database
        decks = self.db_manager.get_all_decks()
        
        if not decks:
            # Show no decks message
            no_decks_label = QLabel("No decks available. Create some decks first!")
            no_decks_label.setAlignment(Qt.AlignCenter)
            no_decks_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.6);
                    font-size: 16px;
                    background: transparent;
                }
            """)
            self.deck_cards_layout.addWidget(no_decks_label)
            return
        
        # Create deck cards
        cols = 3  # Number of columns
        for i, deck in enumerate(decks):
            deck_card = DeckCard(deck)
            deck_card.deck_selected.connect(self.start_study)
            self.deck_cards.append(deck_card)
            
            row = i // cols
            col = i % cols
            self.deck_cards_layout.addWidget(deck_card, row, col)
        
        # Update scroll area
        if hasattr(self, 'deck_selection_widget'):
            scroll_area = self.deck_selection_widget.findChild(QScrollArea)
            if scroll_area:
                scroll_area.setWidget(self.deck_cards_widget)
        
    def start_study(self, deck_id):
        """Start studying the selected deck"""
        self.current_deck_id = deck_id
        self.study_mode.set_current_deck(deck_id)
        self.show_study_interface()
        
    def show_deck_selection(self):
        """Show the deck selection interface"""
        self.deck_selection_widget.setVisible(True)
        self.study_widget.setVisible(False)
        self.back_btn.setVisible(False)
        self.load_decks()
        
    def show_study_interface(self):
        """Show the study interface"""
        self.deck_selection_widget.setVisible(False)
        self.study_widget.setVisible(True)
        self.back_btn.setVisible(True)
        
    def set_current_deck(self, deck_id):
        """Set the current deck for study"""
        self.current_deck_id = deck_id
        self.study_mode.set_current_deck(deck_id)
        self.show_study_interface()
