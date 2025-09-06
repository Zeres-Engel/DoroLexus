from PySide6.QtGui import QFont

DARK_STYLESHEET = """
    QWidget { 
        background-color: #121212; 
        color: #E0E0E0; 
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
    QMainWindow { 
        background-color: rgba(18,18,18,230); 
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
    QLabel { 
        color: #E0E0E0; 
        font-size: 14px; 
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
    QPushButton {
        background-color: #1F6FEB;
        color: #FFFFFF;
        border: 1px solid #2D333B;
        padding: 10px 20px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
    QPushButton:hover { background-color: #2A7FFF; }
    QPushButton:pressed { background-color: #1964D0; }
    QFrame { 
        background-color: #1E1E1E; 
        border: 1px solid #2D2D2D; 
        border-radius: 10px; 
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
    QComboBox, QLineEdit, QTextEdit {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 1px solid #2D2D2D;
        border-radius: 6px;
        padding: 6px 10px;
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
    QListWidget { 
        background-color: #151515; 
        border: 1px solid #2D2D2D; 
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
    QProgressBar {
        border: 1px solid #2D2D2D;
        border-radius: 6px;
        text-align: center;
        color: #E0E0E0;
        background-color: #1E1E1E;
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
    QProgressBar::chunk { background-color: #2EA043; }
    QHeaderView::section { 
        background-color: #1E1E1E; 
        color: #E0E0E0; 
        border: none; 
        border-bottom: 1px solid #2D2D2D; 
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
    QTableWidget { 
        background-color: #151515; 
        color: #E0E0E0; 
        gridline-color: #2D2D2D; 
        font-family: "Cascadia Code", "Cascadia Mono", "Fira Code", "Consolas", "Courier New", monospace;
    }
"""

PRIMARY_COLOR = "#1F6FEB"
DANGER_COLOR = "#DC3545"
SUCCESS_COLOR = "#2EA043"
WARNING_COLOR = "#E3B341"
TEXT_COLOR = "#E0E0E0"


def apply_global_theme(app):
    font = QFont("Cascadia Code", 11)
    if not font.exactMatch():
        for family in ["Cascadia Mono", "Fira Code", "Consolas", "Courier New", "Monospace"]:
            test = QFont(family, 11)
            if test.exactMatch():
                font = test
                break
    app.setFont(font)
    app.setStyleSheet(DARK_STYLESHEET)
