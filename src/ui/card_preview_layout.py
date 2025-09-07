"""
Card Preview Layout - Browse and preview flashcards before studying
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QScrollArea, QFrame, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QPainter, QBrush, QColor, QPen
from ..widgets.button_widget import PrimaryButtonWidget, SecondaryButtonWidget


class PreviewCard(QFrame):
    """Individual card preview widget"""
    
    def __init__(self, card_data, parent=None):
        super().__init__(parent)
        self.card_data = card_data
        self.is_flipped = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the preview card UI"""
        self.setFixedSize(400, 250)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            PreviewCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(45, 45, 45, 0.95),
                    stop:1 rgba(30, 30, 30, 0.95));
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            PreviewCard:hover {
                border: 2px solid rgba(100, 200, 255, 0.5);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Card side indicator
        self.side_indicator = QLabel("Front")
        self.side_indicator.setAlignment(Qt.AlignCenter)
        self.side_indicator.setStyleSheet("""
            QLabel {
                color: #64c8ff;
                font-size: 12px;
                font-weight: bold;
                background: rgba(100, 200, 255, 0.2);
                padding: 5px 10px;
                border-radius: 10px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(self.side_indicator)
        
        # Card content
        self.content_label = QLabel()
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_label.setWordWrap(True)
        self.content_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                padding: 20px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(self.content_label)
        
        # Flip instruction
        flip_hint = QLabel("Click to flip")
        flip_hint.setAlignment(Qt.AlignCenter)
        flip_hint.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.5);
                font-size: 10px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(flip_hint)
        
        self.update_content()
        
    def update_content(self):
        """Update card content based on flip state"""
        if self.is_flipped:
            self.content_label.setText(self.card_data.get('back', ''))
            self.side_indicator.setText("Back")
            self.side_indicator.setStyleSheet("""
                QLabel {
                    color: #66bb6a;
                    font-size: 12px;
                    font-weight: bold;
                    background: rgba(102, 187, 106, 0.2);
                    padding: 5px 10px;
                    border-radius: 10px;
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                }
            """)
        else:
            self.content_label.setText(self.card_data.get('front', ''))
            self.side_indicator.setText("Front")
            self.side_indicator.setStyleSheet("""
                QLabel {
                    color: #64c8ff;
                    font-size: 12px;
                    font-weight: bold;
                    background: rgba(100, 200, 255, 0.2);
                    padding: 5px 10px;
                    border-radius: 10px;
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                }
            """)
            
    def mousePressEvent(self, event):
        """Handle click to flip card"""
        if event.button() == Qt.LeftButton:
            self.is_flipped = not self.is_flipped
            self.update_content()
        super().mousePressEvent(event)


class CardPreviewLayout(QWidget):
    """Layout for previewing cards in a deck"""
    
    back_to_modes = Signal()
    start_study = Signal(str)  # Study mode type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_deck_id = None
        self.current_deck_name = ""
        self.cards = []
        self.current_card_index = 0
        self.init_ui()
        
    def init_ui(self):
        """Initialize the card preview UI"""
        self.setStyleSheet("""
            CardPreviewLayout {
                background: transparent;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Back button
        back_btn = PrimaryButtonWidget("← Back to Study Modes")
        back_btn.clicked.connect(self.back_to_modes.emit)
        header_layout.addWidget(back_btn)
        
        header_layout.addStretch()
        
        # Deck title
        self.deck_title = QLabel()
        self.deck_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        header_layout.addWidget(self.deck_title)
        
        header_layout.addStretch()
        
        # Quick study buttons
        quick_study_layout = QHBoxLayout()
        quick_study_layout.setSpacing(10)
        
        review_btn = PrimaryButtonWidget("🧠 Start Review")
        review_btn.clicked.connect(lambda: self.start_study.emit("review"))
        quick_study_layout.addWidget(review_btn)
        
        test_btn = SecondaryButtonWidget("✏️ Start Test")
        test_btn.clicked.connect(lambda: self.start_study.emit("test"))
        quick_study_layout.addWidget(test_btn)
        
        header_layout.addLayout(quick_study_layout)
        
        layout.addLayout(header_layout)
        
        # Card preview section
        preview_layout = QHBoxLayout()
        preview_layout.setSpacing(20)
        
        # Card list (left side)
        card_list_frame = QFrame()
        card_list_frame.setFixedWidth(250)
        card_list_frame.setStyleSheet("""
            QFrame {
                background: rgba(40, 40, 40, 0.8);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        card_list_layout = QVBoxLayout(card_list_frame)
        card_list_layout.setContentsMargins(15, 15, 15, 15)
        card_list_layout.setSpacing(10)
        
        # Card list title
        list_title = QLabel("Cards in Deck")
        list_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        card_list_layout.addWidget(list_title)
        
        # Card list widget
        self.card_list = QListWidget()
        self.card_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 12px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                margin: 2px 0px;
            }
            QListWidget::item:selected {
                background-color: rgba(100, 200, 255, 0.3);
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.card_list.currentRowChanged.connect(self.on_card_selected)
        card_list_layout.addWidget(self.card_list)
        
        preview_layout.addWidget(card_list_frame)
        
        # Card preview (center)
        preview_center = QVBoxLayout()
        
        # Card counter
        self.card_counter = QLabel()
        self.card_counter.setAlignment(Qt.AlignCenter)
        self.card_counter.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        preview_center.addWidget(self.card_counter)
        
        # Current card preview
        self.current_card_widget = None
        self.card_container = QWidget()
        self.card_container.setFixedSize(420, 270)
        preview_center.addWidget(self.card_container)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.prev_btn = PrimaryButtonWidget("← Previous")
        self.prev_btn.clicked.connect(self.previous_card)
        nav_layout.addWidget(self.prev_btn)
        
        nav_layout.addStretch()
        
        self.next_btn = PrimaryButtonWidget("Next →")
        self.next_btn.clicked.connect(self.next_card)
        nav_layout.addWidget(self.next_btn)
        
        preview_center.addLayout(nav_layout)
        
        preview_layout.addLayout(preview_center)
        
        layout.addLayout(preview_layout)
        layout.addStretch()
        
    def set_deck_info(self, deck_id, deck_name, cards):
        """Set deck information and cards"""
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.cards = cards
        self.current_card_index = 0
        
        self.deck_title.setText(f"Preview: {deck_name}")
        self.refresh_card_list()
        self.show_current_card()
        
    def refresh_card_list(self):
        """Refresh the card list"""
        self.card_list.clear()
        
        for i, card in enumerate(self.cards):
            # Truncate text for list display
            front_preview = card['front'][:30] + "..." if len(card['front']) > 30 else card['front']
            item = QListWidgetItem(f"{i+1}. {front_preview}")
            item.setData(Qt.UserRole, i)
            self.card_list.addItem(item)
            
        if self.cards:
            self.card_list.setCurrentRow(0)
            
    def show_current_card(self):
        """Show the current card in preview"""
        if not self.cards or self.current_card_index >= len(self.cards):
            return
            
        # Remove old card widget
        if self.current_card_widget:
            self.current_card_widget.deleteLater()
            
        # Create new card widget
        card_data = self.cards[self.current_card_index]
        self.current_card_widget = PreviewCard(card_data)
        
        # Add to container
        container_layout = QVBoxLayout(self.card_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.current_card_widget)
        
        # Update counter
        self.card_counter.setText(f"Card {self.current_card_index + 1} of {len(self.cards)}")
        
        # Update navigation buttons
        self.prev_btn.setEnabled(self.current_card_index > 0)
        self.next_btn.setEnabled(self.current_card_index < len(self.cards) - 1)
        
        # Update list selection
        self.card_list.setCurrentRow(self.current_card_index)
        
    def on_card_selected(self, row):
        """Handle card selection from list"""
        if 0 <= row < len(self.cards):
            self.current_card_index = row
            self.show_current_card()
            
    def previous_card(self):
        """Show previous card"""
        if self.current_card_index > 0:
            self.current_card_index -= 1
            self.show_current_card()
            
    def next_card(self):
        """Show next card"""
        if self.current_card_index < len(self.cards) - 1:
            self.current_card_index += 1
            self.show_current_card()
