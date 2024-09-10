from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QDialog, QLabel, QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt

from .spotify_integration import *

import json

class Integrations(QDialog):
    def save_integrations(self):
        integrations_dict = {
            "spotify_username": self.spotify_username.text()
        }

        json_string = json.dumps(integrations_dict)

        f = open("integrations.json", "w")
        f.write(json_string)
        f.close()
    
    def load_integrations(self):
        f = open("integrations.json", "r")
        integrations_dict = json.loads(f.read())
        f.close()

        if 'spotify_username' in integrations_dict:
            spotify_authentication(integrations_dict['spotify_username'])

    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Integrations")
        self.setGeometry(100, 100, 300, 50)  # Ensure the window is visible with appropriate size
        self.setStyleSheet("border-image: none; background: #1e1e1e; color: white;")

        spotify_widget = QWidget(self)

        spot_layout = QHBoxLayout()
        spot_layout.addStretch()

        spotify_label = QLabel("Spotify")
        spot_layout.addWidget(spotify_label)

        self.spotify_username = QLineEdit()
        self.spotify_username.setPlaceholderText("Spotify Username")
        self.spotify_username.resize(200, 50)
        spot_layout.addWidget(self.spotify_username)
        
        spotify_link = QPushButton("Link")
        spotify_link.resize(165, 50)
        spotify_link.pressed.connect(lambda: spotify_authentication(self.spotify_username.text()))
        spotify_link.pressed.connect(self.save_integrations)
        spot_layout.addWidget(spotify_link)

        spot_layout.addStretch()
        spotify_widget.setLayout(spot_layout)

        layout = QVBoxLayout()
        layout.addWidget(spotify_widget)
        layout.setContentsMargins(16, 0, 16, 0)  # (left, top, right, bottom)
        layout.setSpacing(0)  # Space between widgets in the layout
        self.setLayout(layout)

        self.load_integrations()