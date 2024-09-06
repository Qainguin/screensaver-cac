from PySide6.QtWidgets import QDialog, QSlider, QVBoxLayout
from PySide6.QtCore import Qt

class FontSizeSlider(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Choose Font Size")
        self.setGeometry(100, 100, 300, 50)  # Ensure the window is visible with appropriate size
        self.setStyleSheet("border-image: none; background: #1e1e1e;")

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(72)
        self.slider.setMaximum(288)
        self.slider.setTickInterval(8)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setValue(72)
        self.slider.setTracking(True)
        self.slider.valueChanged.connect(parent.change_font_size)

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        layout.setContentsMargins(16, 0, 16, 0)  # (left, top, right, bottom)
        layout.setSpacing(0)  # Space between widgets in the layout
        self.setLayout(layout)

        