import os
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon

from src.core import DatabaseManager
from src.ui.buttons import IconTextButton
from src.modes import DeckManager, StudyMode, StatsWidget
from src.core.paths import asset_path
from src.animation import AnimatedIconLabel, AnimatedWelcomeBanner, SwordTomatoAnim, show_logo_popup


class DoroLexusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_deck = None
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        self.setWindowTitle("DoroLexus - Vocabulary Flashcard App")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)

        icon_path = asset_path("data", "images", "svg", "doro_lexus logo.svg")
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(0.96)
        self.apply_dark_theme()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.create_header(main_layout)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.init_views()
        self.stacked_widget.setCurrentWidget(self.main_menu)
        # Pop-up logo quick reveal on startup
        if icon_path:
            show_logo_popup(self, icon_path, size=96, lifespan_ms=900)

    def create_header(self, layout):
        header_layout = QHBoxLayout()

        logo_path = asset_path("data", "images", "svg", "doro_lexus logo.svg")
        if logo_path:
            logo_widget = AnimatedIconLabel(logo_path, size=48)
            logo_widget.start()
            logo_widget.clicked.connect(lambda: show_logo_popup(self, logo_path, size=120, lifespan_ms=1000))
            header_layout.addWidget(logo_widget)

        title_label = QLabel("DoroLexus")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #E0E0E0; margin: 10px 0px 10px 10px;")

        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.back_button = QPushButton("← Back")
        self.back_button.clicked.connect(self.show_main_menu)
        self.back_button.setVisible(False)

        header_layout.addWidget(self.back_button)
        layout.addLayout(header_layout)

    def init_views(self):
        self.main_menu = self.create_main_menu()
        self.stacked_widget.addWidget(self.main_menu)

        self.deck_manager = DeckManager(self.db_manager)
        self.stacked_widget.addWidget(self.deck_manager)

        self.study_mode = StudyMode(self.db_manager)
        self.stacked_widget.addWidget(self.study_mode)

        self.stats_widget = StatsWidget(self.db_manager)
        self.stacked_widget.addWidget(self.stats_widget)

    def create_main_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout(menu_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        banner = AnimatedWelcomeBanner("Welcome to DoroLexus!")
        layout.addWidget(banner)
        banner.play()

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)

        sword_icon_path = asset_path("data", "images", "svg", "sword-svgrepo-com.svg") or ""
        study_btn = IconTextButton("Study Flashcards", sword_icon_path)
        study_btn.setMinimumHeight(50)
        study_btn.clicked.connect(self.start_study)
        buttons_layout.addWidget(study_btn)

        tomato_icon_path = asset_path("data", "images", "svg", "tomato-svgrepo-com.svg") or ""
        manage_btn = IconTextButton("Manage Decks", tomato_icon_path)
        manage_btn.setMinimumHeight(50)
        manage_btn.clicked.connect(self.manage_decks)
        buttons_layout.addWidget(manage_btn)

        stats_btn = QPushButton("  Statistics")
        stats_btn.setMinimumHeight(50)
        stats_btn.clicked.connect(self.show_stats)
        buttons_layout.addWidget(stats_btn)

        exit_btn = QPushButton("🚪 Exit")
        exit_btn.setMinimumHeight(50)
        exit_btn.setStyleSheet("background-color: #f44336;")
        exit_btn.clicked.connect(self.close)
        buttons_layout.addWidget(exit_btn)

        layout.addLayout(buttons_layout)

        # Sword → Tomato intro animation under buttons
        sword_tomato = SwordTomatoAnim(size=36)
        layout.addWidget(sword_tomato)
        sword_tomato.play()

        # Quick demo: icon popup buttons
        from PySide6.QtWidgets import QHBoxLayout
        icon_row = QHBoxLayout()
        icon_row.setSpacing(12)
        icon_row.setContentsMargins(0, 8, 0, 0)

        def make_icon_btn(svg_name: str, tooltip: str):
            btn = QPushButton()
            path = asset_path("data", "images", "svg", svg_name) or ""
            if path:
                btn.setIcon(QIcon(path))
                btn.setIconSize(QSize(24, 24))
                btn.clicked.connect(lambda: show_logo_popup(self, path, size=110, lifespan_ms=1000))
            btn.setFixedSize(36, 36)
            btn.setToolTip(tooltip)
            btn.setStyleSheet("QPushButton{background-color:#1E1E1E;border:1px solid #2D2D2D;border-radius:8px;}")
            return btn

        icon_row.addWidget(make_icon_btn("doro_lexus logo.svg", "Show App Logo"))
        icon_row.addWidget(make_icon_btn("sword-svgrepo-com.svg", "Show Sword"))
        icon_row.addWidget(make_icon_btn("tomato-svgrepo-com.svg", "Show Tomato"))
        icon_row.addWidget(make_icon_btn("student-svgrepo-com.svg", "Show Student"))
        icon_row.addStretch()
        layout.addLayout(icon_row)
        layout.addStretch()

        return menu_widget

    def apply_dark_theme(self):
        dark_stylesheet = """
            QWidget { background-color: #121212; color: #E0E0E0; }
            QMainWindow { background-color: rgba(18,18,18,230); }
            QLabel { color: #E0E0E0; font-size: 14px; }
            QPushButton {
                background-color: #1F6FEB;
                color: #FFFFFF;
                border: 1px solid #2D333B;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2A7FFF; }
            QPushButton:pressed { background-color: #1964D0; }
            QFrame { background-color: #1E1E1E; border: 1px solid #2D2D2D; border-radius: 10px; }
            QComboBox, QLineEdit, QTextEdit {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #2D2D2D;
                border-radius: 6px;
                padding: 6px 10px;
            }
            QListWidget { background-color: #151515; border: 1px solid #2D2D2D; }
            QProgressBar {
                border: 1px solid #2D2D2D;
                border-radius: 6px;
                text-align: center;
                color: #E0E0E0;
                background-color: #1E1E1E;
            }
            QProgressBar::chunk { background-color: #2EA043; }
            QHeaderView::section { background-color: #1E1E1E; color: #E0E0E0; border: none; border-bottom: 1px solid #2D2D2D; }
            QTableWidget { background-color: #151515; color: #E0E0E0; gridline-color: #2D2D2D; }
        """
        self.setStyleSheet(dark_stylesheet)

    def setup_connections(self):
        self.deck_manager.deck_selected.connect(self.on_deck_selected)

    def start_study(self):
        decks = self.db_manager.get_all_decks()
        if not decks:
            QMessageBox.information(self, "No Decks", "Please create a deck first before studying.")
            return
        self.study_mode.load_decks()
        self.stacked_widget.setCurrentWidget(self.study_mode)
        self.back_button.setVisible(True)

    def manage_decks(self):
        self.deck_manager.refresh_decks()
        self.stacked_widget.setCurrentWidget(self.deck_manager)
        self.back_button.setVisible(True)

    def show_stats(self):
        self.stats_widget.refresh_stats()
        self.stacked_widget.setCurrentWidget(self.stats_widget)
        self.back_button.setVisible(True)

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
        self.back_button.setVisible(False)

    def on_deck_selected(self, deck_id):
        self.current_deck = deck_id
        self.study_mode.set_current_deck(deck_id)


