from PySide6.QtWidgets import QDialog, QPushButton, QGridLayout
from PySide6.QtCore import Qt

class PositionChanger(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Change Label Position")
        self.setGeometry(100, 100, 300, 50)  # Ensure the window is visible with appropriate size
        self.setStyleSheet("border-image: none; background: #1e1e1e;")

        layout = QGridLayout()

        self.topLeftButton = QPushButton("Top-Left")
        self.topLeftButton.setMinimumHeight(100)
        self.topLeftButton.setMinimumWidth(100)
        layout.addWidget(self.topLeftButton, 0, 0)
        self.topLeftButton.pressed.connect(lambda: parent.change_label_position(0))
        self.topButton = QPushButton("Top")
        self.topButton.setMinimumHeight(100)
        self.topButton.setMinimumWidth(100)
        layout.addWidget(self.topButton, 0, 1)
        self.topButton.pressed.connect(lambda: parent.change_label_position(1))
        self.topRightButton = QPushButton("Top-Right")
        self.topRightButton.setMinimumHeight(100)
        self.topRightButton.setMinimumWidth(100)
        layout.addWidget(self.topRightButton, 0, 2)
        self.topRightButton.pressed.connect(lambda: parent.change_label_position(2))

        self.centerLeftButton = QPushButton("Center-Left")
        self.centerLeftButton.setMinimumHeight(100)
        self.centerLeftButton.setMinimumWidth(100)
        layout.addWidget(self.centerLeftButton, 1, 0)
        self.centerLeftButton.pressed.connect(lambda: parent.change_label_position(3))
        self.centerButton = QPushButton("Center")
        self.centerButton.setMinimumHeight(100)
        self.centerButton.setMinimumWidth(100)
        layout.addWidget(self.centerButton, 1, 1)
        self.centerButton.pressed.connect(lambda: parent.change_label_position(4))
        self.centerRightButton = QPushButton("Center-Right")
        self.centerRightButton.setMinimumHeight(100)
        self.centerRightButton.setMinimumWidth(100)
        layout.addWidget(self.centerRightButton, 1, 2)
        self.centerRightButton.pressed.connect(lambda: parent.change_label_position(5))

        self.bottomLeftButton = QPushButton("Bottom-Left")
        self.bottomLeftButton.setMinimumHeight(100)
        self.bottomLeftButton.setMinimumWidth(100)
        layout.addWidget(self.bottomLeftButton, 2, 0)
        self.bottomLeftButton.pressed.connect(lambda: parent.change_label_position(6))
        self.bottomButton = QPushButton("Bottom")
        self.bottomButton.setMinimumHeight(100)
        self.bottomButton.setMinimumWidth(100)
        layout.addWidget(self.bottomButton, 2, 1)
        self.bottomButton.pressed.connect(lambda: parent.change_label_position(7))
        self.bottomRightButton = QPushButton("Bottom-Right")
        self.bottomRightButton.setMinimumHeight(100)
        self.bottomRightButton.setMinimumWidth(100)
        layout.addWidget(self.bottomRightButton, 2, 2)
        self.bottomRightButton.pressed.connect(lambda: parent.change_label_position(8))

        layout.setContentsMargins(16, 16, 16, 16)  # (left, top, right, bottom)
        layout.setVerticalSpacing(0)  # Space between widgets in the layout
        layout.setHorizontalSpacing(0)
        layout.setRowStretch(0, 10)
        layout.setRowStretch(1, 10)
        layout.setRowStretch(2, 10)
        self.setLayout(layout)

        