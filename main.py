from time_window import *
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeWindow()
    sys.exit(app.exec())
