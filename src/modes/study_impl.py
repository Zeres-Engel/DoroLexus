"""
Study mode widget for reviewing flashcards with spaced repetition
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QProgressBar, QMessageBox, QComboBox)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QIcon
import os
from src.core.paths import asset_path

from ..widgets import FlashcardWidget

class StudyMode(QWidget):
    """Widget for studying flashcards with spaced repetition"""
    
    def __init__(self, db_manager, parent=None, show_deck_selector: bool = True):
        super().__init__(parent)
        self.db_manager = db_manager
        self.show_deck_selector = show_deck_selector
        self.current_deck_id = None
        self.cards_due = []
        self.current_card_index = 0
        self.study_session_stats = {
            'cards_studied': 0,
            'correct_answers': 0,
            'start_time': None
        }
        self.init_ui()
        
    def init_ui(self):
        """Initialize the study mode UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Add sword icon to header via window icon
        sword_icon_path = asset_path('data', 'images', 'svg', 'sword-svgrepo-com.svg')
        if sword_icon_path:
            self.setWindowIcon(QIcon(sword_icon_path))

        # Deck selector
        self.deck_label = QLabel("Study Deck:")
        self.deck_selector = QComboBox()
        self.deck_selector.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #007bff;
            }
        """)
        self.deck_selector.currentTextChanged.connect(self.on_deck_changed)
        header_layout.addWidget(self.deck_label)
        header_layout.addWidget(self.deck_selector)
        
        header_layout.addStretch()
        
        # Progress info
        self.progress_label = QLabel("No cards to study")
        self.progress_label.setStyleSheet("color: #6c757d; font-size: 14px;")
        header_layout.addWidget(self.progress_label)
        
        layout.addLayout(header_layout)

        # Hide deck selector when embedded-controlled
        if not self.show_deck_selector:
            self.deck_label.setVisible(False)
            self.deck_selector.setVisible(False)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #28a745;
                border-radius: 3px;
            }
        """)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Flashcard widget (use side-by-side layout)
        self.flashcard_widget = FlashcardWidget(side_by_side=True)
        self.flashcard_widget.study_rating.connect(self.on_card_rated)
        layout.addWidget(self.flashcard_widget)
        
        # Study controls
        controls_layout = QHBoxLayout()
        
        self.previous_btn = QPushButton("← Previous")
        self.previous_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """)
        self.previous_btn.clicked.connect(self.previous_card)
        self.previous_btn.setEnabled(False)
        controls_layout.addWidget(self.previous_btn)
        
        controls_layout.addStretch()
        
        self.next_btn = QPushButton("Next →")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }
        """)
        self.next_btn.clicked.connect(self.next_card)
        self.next_btn.setEnabled(False)
        controls_layout.addWidget(self.next_btn)
        
        layout.addLayout(controls_layout)
        
        # Study session info
        self.session_info = QLabel("")
        self.session_info.setAlignment(Qt.AlignCenter)
        self.session_info.setStyleSheet("""
            QLabel {
                color: #495057;
                font-size: 12px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }
        """)
        self.session_info.setVisible(False)
        layout.addWidget(self.session_info)
        
    def load_decks(self):
        """Load available decks into the selector"""
        self.deck_selector.clear()
        decks = self.db_manager.get_all_decks()
        
        for deck in decks:
            self.deck_selector.addItem(f"{deck['name']} ({deck['card_count']} cards)", deck['id'])
            
        if decks:
            self.deck_selector.setCurrentIndex(0)
            self.on_deck_changed()
            
    def set_current_deck(self, deck_id):
        """Set the current deck for study"""
        for i in range(self.deck_selector.count()):
            if self.deck_selector.itemData(i) == deck_id:
                self.deck_selector.setCurrentIndex(i)
                break
                
    def on_deck_changed(self):
        """Handle deck selection change"""
        if self.deck_selector.currentData():
            self.current_deck_id = self.deck_selector.currentData()
            self.load_cards_due()
            self.start_study_session()
            
    def load_cards_due(self):
        """Load cards due for review"""
        if not self.current_deck_id:
            return
            
        self.cards_due = self.db_manager.get_cards_due_for_review(self.current_deck_id)
        self.current_card_index = 0
        
        if self.cards_due:
            self.progress_label.setText(f"Cards due: {len(self.cards_due)}")
            self.progress_bar.setVisible(True)
            self.progress_bar.setMaximum(len(self.cards_due))
            self.progress_bar.setValue(0)
            self.show_current_card()
        else:
            self.progress_label.setText("No cards due for review")
            self.progress_bar.setVisible(False)
            self.flashcard_widget.set_card_content("", "")
            self.next_btn.setEnabled(False)
            self.previous_btn.setEnabled(False)
            
    def start_study_session(self):
        """Start a new study session"""
        from datetime import datetime
        self.study_session_stats = {
            'cards_studied': 0,
            'correct_answers': 0,
            'start_time': datetime.now()
        }
        self.update_session_info()
        
    def show_current_card(self):
        """Display the current card"""
        if not self.cards_due or self.current_card_index >= len(self.cards_due):
            return
            
        card = self.cards_due[self.current_card_index]
        self.flashcard_widget.set_card_content(card['front'], card['back'])
        
        # Update progress
        self.progress_bar.setValue(self.current_card_index + 1)
        
        # Update navigation buttons
        self.previous_btn.setEnabled(self.current_card_index > 0)
        self.next_btn.setEnabled(self.current_card_index < len(self.cards_due) - 1)
        
    def next_card(self):
        """Move to the next card"""
        if self.current_card_index < len(self.cards_due) - 1:
            self.current_card_index += 1
            self.show_current_card()
            
    def previous_card(self):
        """Move to the previous card"""
        if self.current_card_index > 0:
            self.current_card_index -= 1
            self.show_current_card()
            
    def on_card_rated(self, rating):
        """Handle card rating from spaced repetition"""
        if not self.cards_due or self.current_card_index >= len(self.cards_due):
            return
            
        card = self.cards_due[self.current_card_index]
        
        # Record the study session
        self.db_manager.record_study_session(card['id'], self.current_deck_id, rating)
        
        # Update session stats
        self.study_session_stats['cards_studied'] += 1
        if rating >= 3:  # Correct answer (rating 3-5)
            self.study_session_stats['correct_answers'] += 1
            
        self.update_session_info()
        
        # Move to next card or finish session
        if self.current_card_index < len(self.cards_due) - 1:
            self.next_card()
        else:
            self.finish_study_session()
            
    def update_session_info(self):
        """Update the session information display"""
        stats = self.study_session_stats
        if stats['cards_studied'] > 0:
            accuracy = (stats['correct_answers'] / stats['cards_studied']) * 100
            self.session_info.setText(
                f"Session: {stats['cards_studied']} cards studied | "
                f"Accuracy: {accuracy:.1f}% | "
                f"Correct: {stats['correct_answers']}"
            )
            self.session_info.setVisible(True)
        else:
            self.session_info.setVisible(False)
            
    def finish_study_session(self):
        """Finish the current study session"""
        stats = self.study_session_stats
        if stats['cards_studied'] > 0:
            # Record daily statistics
            from datetime import datetime
            study_time = (datetime.now() - stats['start_time']).total_seconds()
            
            self.db_manager.record_daily_stats(
                self.current_deck_id,
                stats['cards_studied'],
                stats['correct_answers'],
                int(study_time)
            )
            
            # Show completion message
            accuracy = (stats['correct_answers'] / stats['cards_studied']) * 100
            QMessageBox.information(
                self, 
                "Study Session Complete",
                f"Great job! You studied {stats['cards_studied']} cards with {accuracy:.1f}% accuracy.\n\n"
                f"Study time: {int(study_time // 60)} minutes {int(study_time % 60)} seconds"
            )
            
            # Reload cards for next session
            self.load_cards_due()
