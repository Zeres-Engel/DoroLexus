"""
Statistics widget for displaying study progress and analytics
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QGroupBox, QGridLayout, QProgressBar,
                               QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class StatsWidget(QWidget):
    """Widget for displaying study statistics and progress"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.init_ui()
        
    def init_ui(self):
        """Initialize the statistics UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Study Statistics")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2E7D32;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Deck selector
        self.deck_selector = QComboBox()
        self.deck_selector.addItem("All Decks", None)
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
        self.deck_selector.currentTextChanged.connect(self.refresh_stats)
        header_layout.addWidget(QLabel("Filter by deck:"))
        header_layout.addWidget(self.deck_selector)
        
        layout.addLayout(header_layout)
        
        # Main statistics grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(20)
        
        # Overall stats group
        overall_group = self.create_stats_group("Overall Statistics", [
            ("Total Study Sessions", "0"),
            ("Cards Studied", "0"),
            ("Correct Answers", "0"),
            ("Accuracy Rate", "0%"),
            ("Total Study Time", "0 minutes")
        ])
        stats_grid.addWidget(overall_group, 0, 0)
        
        # Recent activity group
        recent_group = self.create_stats_group("Recent Activity (Last 7 Days)", [
            ("Study Sessions", "0"),
            ("Cards Studied", "0"),
            ("Average Accuracy", "0%"),
            ("Study Streak", "0 days")
        ])
        stats_grid.addWidget(recent_group, 0, 1)
        
        layout.addLayout(stats_grid)
        
        # Daily progress chart
        chart_group = QGroupBox("Daily Progress (Last 30 Days)")
        chart_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #495057;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        chart_layout = QVBoxLayout(chart_group)
        
        # Progress table
        self.progress_table = QTableWidget()
        self.progress_table.setColumnCount(4)
        self.progress_table.setHorizontalHeaderLabels(["Date", "Cards Studied", "Accuracy", "Study Time"])
        self.progress_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.progress_table.setAlternatingRowColors(True)
        self.progress_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 5px;
                background-color: white;
                gridline-color: #dee2e6;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
            }
        """)
        chart_layout.addWidget(self.progress_table)
        
        layout.addWidget(chart_group)
        
        # Load initial data
        self.load_decks()
        self.refresh_stats()
        
    def create_stats_group(self, title, stats_items):
        """Create a statistics group box with the given items"""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #495057;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(10)
        
        for label_text, value_text in stats_items:
            stat_layout = QHBoxLayout()
            
            label = QLabel(f"{label_text}:")
            label.setStyleSheet("color: #6c757d; font-size: 12px;")
            stat_layout.addWidget(label)
            
            value = QLabel(value_text)
            value.setStyleSheet("color: #495057; font-size: 14px; font-weight: bold;")
            stat_layout.addWidget(value)
            
            stat_layout.addStretch()
            layout.addLayout(stat_layout)
            
        return group
        
    def load_decks(self):
        """Load available decks into the selector"""
        self.deck_selector.clear()
        self.deck_selector.addItem("All Decks", None)
        
        decks = self.db_manager.get_all_decks()
        for deck in decks:
            self.deck_selector.addItem(deck['name'], deck['id'])
            
    def refresh_stats(self):
        """Refresh all statistics"""
        deck_id = self.deck_selector.currentData()
        self.update_overall_stats(deck_id)
        self.update_recent_stats(deck_id)
        self.update_progress_table(deck_id)
        
    def update_overall_stats(self, deck_id=None):
        """Update overall statistics"""
        stats = self.db_manager.get_study_statistics(deck_id, 30)
        
        # Find the overall stats group and update values
        overall_group = None
        for group in self.findChildren(QGroupBox):
            if group.title() == "Overall Statistics":
                overall_group = group
                break
                
        if overall_group:
            labels = overall_group.findChildren(QLabel)
            if len(labels) >= 10:  # 5 pairs of label/value
                labels[1].setText(str(stats['total_sessions']))  # Total Study Sessions
                labels[3].setText(str(stats['total_cards_studied']))  # Cards Studied
                labels[5].setText(str(stats['total_correct']))  # Correct Answers
                labels[7].setText(f"{stats['accuracy_rate']:.1f}%")  # Accuracy Rate
                labels[9].setText(f"{stats['total_study_time'] // 60} minutes")  # Total Study Time
                
    def update_recent_stats(self, deck_id=None):
        """Update recent activity statistics"""
        stats = self.db_manager.get_study_statistics(deck_id, 7)
        
        # Calculate study streak (simplified)
        daily_stats = stats['daily_stats']
        streak = 0
        if daily_stats:
            # Count consecutive days with study activity
            for day_stat in daily_stats:
                if day_stat['cards_studied'] > 0:
                    streak += 1
                else:
                    break
                    
        # Find the recent activity group and update values
        recent_group = None
        for group in self.findChildren(QGroupBox):
            if group.title() == "Recent Activity (Last 7 Days)":
                recent_group = group
                break
                
        if recent_group:
            labels = recent_group.findChildren(QLabel)
            if len(labels) >= 8:  # 4 pairs of label/value
                labels[1].setText(str(stats['total_sessions']))  # Study Sessions
                labels[3].setText(str(stats['total_cards_studied']))  # Cards Studied
                labels[5].setText(f"{stats['accuracy_rate']:.1f}%")  # Average Accuracy
                labels[7].setText(str(streak))  # Study Streak
                
    def update_progress_table(self, deck_id=None):
        """Update the daily progress table"""
        stats = self.db_manager.get_study_statistics(deck_id, 30)
        daily_stats = stats['daily_stats']
        
        self.progress_table.setRowCount(len(daily_stats))
        
        for row, day_stat in enumerate(daily_stats):
            # Date
            date_item = QTableWidgetItem(day_stat['date'])
            self.progress_table.setItem(row, 0, date_item)
            
            # Cards studied
            cards_item = QTableWidgetItem(str(day_stat['cards_studied']))
            self.progress_table.setItem(row, 1, cards_item)
            
            # Accuracy
            accuracy = 0
            if day_stat['cards_studied'] > 0:
                accuracy = (day_stat['correct_answers'] / day_stat['cards_studied']) * 100
            accuracy_item = QTableWidgetItem(f"{accuracy:.1f}%")
            self.progress_table.setItem(row, 2, accuracy_item)
            
            # Study time
            study_time = day_stat['study_time_seconds']
            time_str = f"{study_time // 60}m {study_time % 60}s"
            time_item = QTableWidgetItem(time_str)
            self.progress_table.setItem(row, 3, time_item)
