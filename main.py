from PySide6.QtWidgets import QApplication
from src.time_window import *
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeWindow()
    window.showMaximized()
    sys.exit(app.exec())
