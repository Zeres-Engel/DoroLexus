"""
Deck Card Layout Components
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class CreateDeckCardLayout(QFrame):
    """Special card layout for creating new decks"""
    
    create_deck = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the create deck card UI"""
        self.setFixedSize(200, 120)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            CreateDeckCardLayout {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 200, 100, 0.3),
                    stop:1 rgba(60, 160, 60, 0.3));
                border: 2px dashed rgba(100, 200, 100, 0.6);
                border-radius: 12px;
            }
            CreateDeckCardLayout:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(120, 220, 120, 0.4),
                    stop:1 rgba(80, 180, 80, 0.4));
                border: 2px dashed rgba(120, 220, 120, 0.8);
            }
        """)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Plus icon (using text for now)
        plus_label = QLabel("+")
        plus_label.setAlignment(Qt.AlignCenter)
        plus_label.setStyleSheet("""
            QLabel {
                color: rgba(100, 200, 100, 0.8);
                font-size: 36px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(plus_label)
        
        # Create text
        create_label = QLabel("New Deck")
        create_label.setAlignment(Qt.AlignCenter)
        create_label.setStyleSheet("""
            QLabel {
                color: rgba(100, 200, 100, 0.9);
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(create_label)
        
    def mousePressEvent(self, event):
        """Handle mouse click to create deck"""
        if event.button() == Qt.LeftButton:
            self.create_deck.emit()
        super().mousePressEvent(event)


class DeckManagementCardLayout(QFrame):
    """Individual deck card layout for management"""
    
    deck_selected = Signal(int)  # For studying
    edit_deck = Signal(int)      # For editing cards
    delete_deck = Signal(int)
    
    def __init__(self, deck_data, parent=None):
        super().__init__(parent)
        self.deck_id = deck_data['id']
        self.deck_name = deck_data['name']
        self.card_count = deck_data['card_count']
        self.description = deck_data.get('description', '')
        self.init_ui()
        
    def init_ui(self):
        """Initialize the deck management card UI"""
        self.setFixedSize(200, 120)
        self.setStyleSheet("""
            DeckManagementCardLayout {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 60, 60, 0.9),
                    stop:1 rgba(40, 40, 40, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            DeckManagementCardLayout:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(80, 80, 80, 0.9),
                    stop:1 rgba(60, 60, 60, 0.9));
                border: 2px solid rgba(100, 200, 255, 0.5);
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        # Deck name
        name_label = QLabel(self.deck_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Card count
        count_label = QLabel(f"{self.card_count} cards")
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 11px;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
        """)
        layout.addWidget(count_label)
        
        layout.addStretch()
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(4)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedSize(35, 20)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffa726;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background-color: #ff9800;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_deck.emit(self.deck_id))
        actions_layout.addWidget(edit_btn)
        
        # Study button
        study_btn = QPushButton("Study")
        study_btn.setFixedSize(35, 20)
        study_btn.setStyleSheet("""
            QPushButton {
                background-color: #64c8ff;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 9px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background-color: #4a9eff;
            }
        """)
        study_btn.clicked.connect(lambda: self.deck_selected.emit(self.deck_id))
        actions_layout.addWidget(study_btn)
        
        # Delete button
        delete_btn = QPushButton("×")
        delete_btn.setFixedSize(20, 20)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6b6b;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background-color: #ff5252;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_deck.emit(self.deck_id))
        actions_layout.addWidget(delete_btn)
        
        layout.addLayout(actions_layout)
        
    def mousePressEvent(self, event):
        """Handle mouse click on deck card to edit"""
        if event.button() == Qt.LeftButton:
            self.edit_deck.emit(self.deck_id)
        super().mousePressEvent(event)


class StudyDeckCardLayout(QFrame):
    """Deck card layout for study page"""
    
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
            StudyDeckCardLayout {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 60, 60, 0.9),
                    stop:1 rgba(40, 40, 40, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            StudyDeckCardLayout:hover {
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
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
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
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
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
                    font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
                }
            """)
            layout.addWidget(due_label)
        
        layout.addStretch()
        
    def mousePressEvent(self, event):
        """Handle mouse click to select deck"""
        if event.button() == Qt.LeftButton:
            self.deck_selected.emit(self.deck_id)
        super().mousePressEvent(event)
