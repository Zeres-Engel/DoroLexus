"""
Dialog Layout Components
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QTextEdit, QPushButton, QFormLayout)
from PySide6.QtCore import Qt, Signal
from ..widgets.button_widget import PrimaryButtonWidget, DangerButtonWidget


class DeckDialogLayout(QDialog):
    """Modern dialog layout for creating/editing decks"""
    
    def __init__(self, deck_data=None, parent=None):
        super().__init__(parent)
        self.deck_data = deck_data
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        self.setWindowTitle("Edit Deck" if self.deck_data else "Create New Deck")
        self.setModal(True)
        self.resize(450, 300)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background: transparent;
                color: white;
            }
            QLabel {
                color: white;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QLineEdit, QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #64c8ff;
            }
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Edit Deck Details" if self.deck_data else "Create New Deck")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #64c8ff;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Deck name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter deck name...")
        if self.deck_data:
            self.name_edit.setText(self.deck_data.get('name', ''))
        form_layout.addRow("Deck Name:", self.name_edit)
        
        # Deck description
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Enter deck description (optional)...")
        self.description_edit.setMaximumHeight(100)
        if self.deck_data:
            self.description_edit.setText(self.deck_data.get('description', ''))
        form_layout.addRow("Description:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Deck")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #64c8ff;
                color: white;
            }
            QPushButton:hover {
                background-color: #4a9eff;
            }
        """)
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
    def get_deck_data(self):
        """Get the deck data from the form"""
        return {
            'name': self.name_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip()
        }


class CardDialogLayout(QDialog):
    """Dialog layout for creating/editing cards"""
    
    def __init__(self, card_data=None, parent=None):
        super().__init__(parent)
        self.card_data = card_data
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        self.setWindowTitle("Edit Card" if self.card_data else "Create New Card")
        self.setModal(True)
        self.resize(500, 400)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background: transparent;
                color: white;
            }
            QLabel {
                color: white;
                background: transparent;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QLineEdit, QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #64c8ff;
            }
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Edit Card Details" if self.card_data else "Create New Card")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #64c8ff;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Front text
        self.front_edit = QTextEdit()
        self.front_edit.setPlaceholderText("Enter the question or front text...")
        self.front_edit.setMaximumHeight(120)
        if self.card_data:
            self.front_edit.setText(self.card_data.get('front', ''))
        form_layout.addRow("Front (Question):", self.front_edit)
        
        # Back text
        self.back_edit = QTextEdit()
        self.back_edit.setPlaceholderText("Enter the answer or back text...")
        self.back_edit.setMaximumHeight(120)
        if self.card_data:
            self.back_edit.setText(self.card_data.get('back', ''))
        form_layout.addRow("Back (Answer):", self.back_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Card")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #64c8ff;
                color: white;
            }
            QPushButton:hover {
                background-color: #4a9eff;
            }
        """)
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
    def get_card_data(self):
        """Get the card data from the form"""
        return {
            'front': self.front_edit.toPlainText().strip(),
            'back': self.back_edit.toPlainText().strip()
        }
