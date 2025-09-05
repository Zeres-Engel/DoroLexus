#!/usr/bin/env python3
"""
DoroLexus - A vocabulary flashcard application
A PySide6-based flashcard app similar to Anki for studying vocabulary
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QPixmap

from src.ui.theme import apply_global_theme
from src.main import DoroLexusApp


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("DoroLexus")
    app.setApplicationVersion("1.0.0")
    apply_global_theme(app)
    
    # Create and show main window
    window = DoroLexusApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
