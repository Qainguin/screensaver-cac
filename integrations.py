from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt

from spotify_integration import *

class Integrations(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Integrations")
        self.setGeometry(100, 100, 300, 50)  # Ensure the window is visible with appropriate size
        self.setStyleSheet("border-image: none; background: #1e1e1e;")

        spotify_widget = QWidget(self)

        spot_layout = QHBoxLayout()
        spot_layout.addStretch()

        spotify_label = QLabel("Spotify")
        spot_layout.addWidget(spotify_label)

        spotify_username = QLineEdit()
        spotify_username.setPlaceholderText("Spotify Username")
        spotify_username.resize(200, 50)
        spot_layout.addWidget(spotify_username)
        
        spotify_link = QPushButton("Link")
        spotify_link.resize(165, 50)
        spotify_link.pressed.connect(lambda: spotify_authentication(spotify_username.text()))
        spot_layout.addWidget(spotify_link)

        spot_layout.addStretch()
        spotify_widget.setLayout(spot_layout)

        layout = QVBoxLayout()
        layout.addWidget(spotify_widget)
        layout.setContentsMargins(16, 0, 16, 0)  # (left, top, right, bottom)
        layout.setSpacing(0)  # Space between widgets in the layout
        self.setLayout(layout)

        