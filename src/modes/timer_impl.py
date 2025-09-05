"""
Timer mode for study sessions with easy/hard difficulty modes and customizable reminders
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QComboBox, QSpinBox, QProgressBar, 
                               QGroupBox, QFormLayout, QCheckBox, QSlider,
                               QMessageBox, QFrame)
from PySide6.QtCore import Qt, QTimer, Signal, QTime, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon
from PySide6.QtMultimedia import QSoundEffect
from src.core.paths import asset_path
import os


class StudyTimerWidget(QWidget):
    """Study timer with difficulty modes and customizable reminders"""
    
    # Signals
    timer_finished = Signal()
    break_started = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.study_time = 25  # minutes
        self.break_time = 5   # minutes
        self.difficulty = "Normal"  # Easy, Normal, Hard
        self.remaining_seconds = 0
        self.is_study_session = True
        self.is_running = False
        self.session_count = 0
        
        # Timer settings based on difficulty
        self.difficulty_settings = {
            "Easy": {"study": 15, "break": 10, "sessions": 2},
            "Normal": {"study": 25, "break": 5, "sessions": 4}, 
            "Hard": {"study": 45, "break": 5, "sessions": 6}
        }
        
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        """Initialize the timer UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Study Timer")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #1F6FEB;")
        
        clock_icon_path = asset_path('data', 'images', 'svg', 'clock-svgrepo-com.svg')
        if clock_icon_path:
            self.setWindowIcon(QIcon(clock_icon_path))
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Timer display card
        self.timer_card = self.create_timer_display()
        layout.addWidget(self.timer_card)
        
        # Settings card
        self.settings_card = self.create_settings_panel()
        layout.addWidget(self.settings_card)
        
        # Control buttons
        self.controls_layout = self.create_control_buttons()
        layout.addLayout(self.controls_layout)
        
        # Progress and stats
        self.progress_card = self.create_progress_panel()
        layout.addWidget(self.progress_card)
        
    def create_timer_display(self):
        """Create the main timer display"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(31, 111, 235, 0.1),
                    stop:1 rgba(46, 125, 50, 0.1));
                border-radius: 20px;
                border: 2px solid rgba(31, 111, 235, 0.3);
                padding: 20px;
            }
        """)
        card.setMinimumHeight(200)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        
        # Session type label
        self.session_label = QLabel("Study Session")
        session_font = QFont()
        session_font.setPointSize(16)
        session_font.setBold(True)
        self.session_label.setFont(session_font)
        self.session_label.setAlignment(Qt.AlignCenter)
        self.session_label.setStyleSheet("color: #1F6FEB; margin-bottom: 10px;")
        layout.addWidget(self.session_label)
        
        # Time display
        self.time_display = QLabel("25:00")
        time_font = QFont()
        time_font.setPointSize(48)
        time_font.setBold(True)
        time_font.setFamily("Courier New")
        self.time_display.setFont(time_font)
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setStyleSheet("""
            QLabel {
                color: #1F6FEB;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }
        """)
        layout.addWidget(self.time_display)
        
        # Progress bar
        self.time_progress = QProgressBar()
        self.time_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #1F6FEB;
                border-radius: 10px;
                text-align: center;
                background-color: rgba(255, 255, 255, 0.1);
                height: 20px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1F6FEB, stop:1 #2EA043);
                border-radius: 8px;
            }
        """)
        self.time_progress.setTextVisible(False)
        layout.addWidget(self.time_progress)
        
        return card
        
    def create_settings_panel(self):
        """Create the settings panel"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 0.5);
                border-radius: 15px;
                border: 1px solid #2D2D2D;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        # Difficulty selection
        diff_layout = QHBoxLayout()
        diff_layout.addWidget(QLabel("Difficulty:"))
        
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Normal", "Hard"])
        self.difficulty_combo.setCurrentText("Normal")
        self.difficulty_combo.currentTextChanged.connect(self.on_difficulty_changed)
        self.difficulty_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 6px;
                background-color: #1E1E1E;
                border: 1px solid #2D2D2D;
                color: #E0E0E0;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)
        diff_layout.addWidget(self.difficulty_combo)
        diff_layout.addStretch()
        
        # Settings info
        self.settings_info = QLabel("Normal: 25min study, 5min break, 4 sessions")
        self.settings_info.setStyleSheet("color: #888; font-size: 12px;")
        diff_layout.addWidget(self.settings_info)
        
        layout.addLayout(diff_layout)
        
        # Reminder settings
        reminder_layout = QHBoxLayout()
        self.reminder_checkbox = QCheckBox("Sound reminders")
        self.reminder_checkbox.setChecked(True)
        self.reminder_checkbox.setStyleSheet("""
            QCheckBox {
                color: #E0E0E0;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #1F6FEB;
                border: 2px solid #1F6FEB;
                border-radius: 3px;
            }
            QCheckBox::indicator:unchecked {
                background-color: transparent;
                border: 2px solid #666;
                border-radius: 3px;
            }
        """)
        reminder_layout.addWidget(self.reminder_checkbox)
        reminder_layout.addStretch()
        
        layout.addLayout(reminder_layout)
        
        return card
        
    def create_control_buttons(self):
        """Create control buttons"""
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Start/Pause button
        self.start_pause_btn = QPushButton("Start")
        self.start_pause_btn.setMinimumHeight(50)
        self.start_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #2EA043;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 0px 30px;
            }
            QPushButton:hover {
                background-color: #269534;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.start_pause_btn.clicked.connect(self.toggle_timer)
        layout.addWidget(self.start_pause_btn)
        
        # Reset button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setMinimumHeight(50)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 0px 30px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #a02330;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_timer)
        layout.addWidget(self.reset_btn)
        
        # Skip button
        self.skip_btn = QPushButton("Skip")
        self.skip_btn.setMinimumHeight(50)
        self.skip_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 0px 30px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #495057;
            }
        """)
        self.skip_btn.clicked.connect(self.skip_session)
        layout.addWidget(self.skip_btn)
        
        return layout
        
    def create_progress_panel(self):
        """Create progress tracking panel"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 0.3);
                border-radius: 10px;
                border: 1px solid #2D2D2D;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        # Session counter
        self.session_counter = QLabel("Session 0 of 4")
        self.session_counter.setAlignment(Qt.AlignCenter)
        self.session_counter.setStyleSheet("color: #E0E0E0; font-size: 14px; font-weight: bold;")
        layout.addWidget(self.session_counter)
        
        # Session progress
        self.session_progress = QProgressBar()
        self.session_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #2D2D2D;
                border-radius: 8px;
                text-align: center;
                background-color: rgba(255, 255, 255, 0.1);
                height: 15px;
            }
            QProgressBar::chunk {
                background-color: #2EA043;
                border-radius: 7px;
            }
        """)
        self.session_progress.setTextVisible(False)
        layout.addWidget(self.session_progress)
        
        return card
        
    def setup_timer(self):
        """Setup the main timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.setInterval(1000)  # 1 second
        
        # Initialize with normal difficulty
        self.on_difficulty_changed("Normal")
        
    def on_difficulty_changed(self, difficulty):
        """Handle difficulty change"""
        self.difficulty = difficulty
        settings = self.difficulty_settings[difficulty]
        
        self.study_time = settings["study"]
        self.break_time = settings["break"]
        self.total_sessions = settings["sessions"]
        
        # Update settings info
        self.settings_info.setText(
            f"{difficulty}: {self.study_time}min study, {self.break_time}min break, {self.total_sessions} sessions"
        )
        
        # Reset timer if not running
        if not self.is_running:
            self.reset_timer()
            
    def toggle_timer(self):
        """Start or pause the timer"""
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()
            
    def start_timer(self):
        """Start the timer"""
        if self.remaining_seconds == 0:
            # Starting new session
            if self.is_study_session:
                self.remaining_seconds = self.study_time * 60
                self.session_label.setText("Study Session")
                self.session_label.setStyleSheet("color: #1F6FEB; margin-bottom: 10px;")
            else:
                self.remaining_seconds = self.break_time * 60
                self.session_label.setText("Break Time")
                self.session_label.setStyleSheet("color: #2EA043; margin-bottom: 10px;")
                
        self.is_running = True
        self.start_pause_btn.setText("Pause")
        self.start_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: #212529;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 0px 30px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        
        # Set progress bar maximum
        total_time = self.study_time * 60 if self.is_study_session else self.break_time * 60
        self.time_progress.setMaximum(total_time)
        
        self.timer.start()
        
    def pause_timer(self):
        """Pause the timer"""
        self.is_running = False
        self.start_pause_btn.setText("Start")
        self.start_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #2EA043;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 0px 30px;
            }
            QPushButton:hover {
                background-color: #269534;
            }
        """)
        self.timer.stop()
        
    def reset_timer(self):
        """Reset the timer"""
        self.timer.stop()
        self.is_running = False
        self.is_study_session = True
        self.session_count = 0
        self.remaining_seconds = self.study_time * 60
        
        self.start_pause_btn.setText("Start")
        self.start_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #2EA043;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 0px 30px;
            }
            QPushButton:hover {
                background-color: #269534;
            }
        """)
        
        self.session_label.setText("Study Session")
        self.session_label.setStyleSheet("color: #1F6FEB; margin-bottom: 10px;")
        
        self.update_display()
        self.update_progress()
        
    def skip_session(self):
        """Skip current session"""
        if self.is_running:
            self.timer.stop()
            self.session_finished()
            
    def update_timer(self):
        """Update timer every second"""
        self.remaining_seconds -= 1
        self.update_display()
        self.update_progress()
        
        if self.remaining_seconds <= 0:
            self.session_finished()
            
    def update_display(self):
        """Update the time display"""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.time_display.setText(f"{minutes:02d}:{seconds:02d}")
        
    def update_progress(self):
        """Update progress bars"""
        # Time progress
        total_time = self.study_time * 60 if self.is_study_session else self.break_time * 60
        elapsed = total_time - self.remaining_seconds
        self.time_progress.setValue(elapsed)
        
        # Session progress
        self.session_counter.setText(f"Session {self.session_count} of {self.total_sessions}")
        self.session_progress.setMaximum(self.total_sessions)
        self.session_progress.setValue(self.session_count)
        
    def session_finished(self):
        """Handle session completion"""
        self.timer.stop()
        self.is_running = False
        
        # Play reminder sound if enabled
        if self.reminder_checkbox.isChecked():
            self.play_notification_sound()
            
        if self.is_study_session:
            # Study session completed
            self.session_count += 1
            
            if self.session_count >= self.total_sessions:
                # All sessions completed
                self.show_completion_message()
                self.reset_timer()
            else:
                # Switch to break
                self.is_study_session = False
                self.remaining_seconds = self.break_time * 60
                self.session_label.setText("Break Time")
                self.session_label.setStyleSheet("color: #2EA043; margin-bottom: 10px;")
                self.break_started.emit()
                self.start_timer()
        else:
            # Break completed, back to study
            self.is_study_session = True
            self.remaining_seconds = self.study_time * 60
            self.session_label.setText("Study Session")
            self.session_label.setStyleSheet("color: #1F6FEB; margin-bottom: 10px;")
            self.start_timer()
            
        self.timer_finished.emit()
        
    def play_notification_sound(self):
        """Play notification sound"""
        try:
            # Try to play a simple beep sound
            # Note: This might need additional setup for sound files
            pass
        except:
            # Fallback: show message box as notification
            if self.is_study_session:
                QMessageBox.information(self, "Break Time!", "Time for a break! 🎉")
            else:
                QMessageBox.information(self, "Study Time!", "Back to studying! 📚")
                
    def show_completion_message(self):
        """Show completion message"""
        difficulty_emoji = {"Easy": "😊", "Normal": "💪", "Hard": "🏆"}
        emoji = difficulty_emoji.get(self.difficulty, "🎉")
        
        QMessageBox.information(
            self, 
            "Session Complete!",
            f"Congratulations! {emoji}\n\n"
            f"You've completed all {self.total_sessions} study sessions "
            f"on {self.difficulty} difficulty!\n\n"
            f"Total study time: {self.total_sessions * self.study_time} minutes"
        )
