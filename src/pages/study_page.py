"""
Study page with dark theme, deck selection, and card deck interface
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QComboBox, QFrame, QScrollArea,
                               QGridLayout, QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter, QBrush, QColor, QPen
from src.modes.study_impl import StudyMode
from src.widgets.button_widget import PrimaryButtonWidget as PrimaryButton, IconTextButtonWidget as IconTextButton
from src.ui import StudyPageHeaderLayout, StudyDeckSelectionLayout
import os
from src.core.paths import asset_path


# DeckCard class is now imported from src.ui.deck_card_layout


class StudyPage(QWidget):
    """Study page with deck selection and study interface"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_deck_id = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the study page UI"""
        self.setStyleSheet("""
            StudyPage {
                background: transparent;
                color: white;
            }
            QWidget {
                background: transparent;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Page header
        self.header = StudyPageHeaderLayout()
        self.header.back_requested.connect(self.show_deck_selection)
        layout.addWidget(self.header)
        
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
        self.deck_selection_widget = StudyDeckSelectionLayout()
        self.deck_selection_widget.deck_selected.connect(self.start_study)
        content_layout.addWidget(self.deck_selection_widget)
        
        # Study interface view
        self.study_widget = self.create_study_interface()
        content_layout.addWidget(self.study_widget)
        
        layout.addWidget(self.content_stack)
        
        # Initially show deck selection
        self.show_deck_selection()
        
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
                background: transparent;
                color: white;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
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
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
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
                font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
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
        decks = self.db_manager.get_all_decks()
        self.deck_selection_widget.refresh_decks(decks)
        
    def start_study(self, deck_id):
        """Start studying the selected deck"""
        self.current_deck_id = deck_id
        self.study_mode.set_current_deck(deck_id)
        self.show_study_interface()
        
    def show_deck_selection(self):
        """Show the deck selection interface"""
        self.deck_selection_widget.setVisible(True)
        self.study_widget.setVisible(False)
        self.header.show_deck_selection()
        self.load_decks()
        
    def show_study_interface(self):
        """Show the study interface"""
        self.deck_selection_widget.setVisible(False)
        self.study_widget.setVisible(True)
        self.header.show_study_mode()
        
    def set_current_deck(self, deck_id):
        """Set the current deck for study"""
        self.current_deck_id = deck_id
        self.study_mode.set_current_deck(deck_id)
        self.show_study_interface()
