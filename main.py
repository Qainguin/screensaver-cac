from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QComboBox, QSlider, QSizePolicy
from PySide6.QtGui import QColor, QFont, QFontDatabase
from PySide6.QtCore import QTimer, QTime, Qt, QPoint

class ColorPickerExample(QWidget):
    def __init__(self):
        super().__init__()

        # Create the color picker button
        self.color_button = QPushButton("Pick a Color", self)
        self.color_button.setStyleSheet("background-color: rgba(100,100,100,0.5);")
        self.color_button.clicked.connect(self.open_color_picker)

        # Create the font picker dropdown
        self.font_combo = QComboBox(self)
        self.populate_fonts()
        self.font_combo.setStyleSheet("background-color: rgba(100,100,100,0.5);")
        self.font_combo.currentTextChanged.connect(self.change_font)

        # Create the font size slider
        self.font_size_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.font_size_slider.setRange(48, 144)  # Set range for font sizes
        self.font_size_slider.setValue(72)  # Initial font size
        self.font_size_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.font_size_slider.setTickInterval(2)
        self.font_size_slider.setStyleSheet("background-color: rgba(100,100,100,0.5);")
        self.font_size_slider.valueChanged.connect(self.change_font_size)

        # Create a panel (frame) to hold the controls
        self.panel = QFrame(self)
        self.panel.setFrameShape(QFrame.StyledPanel)
        self.panel.setStyleSheet("background-color: rgba(100,100,100,0.5);")  # Panel color for visibility
        self.panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # Prevent stretching

        # Create a layout for the panel and add the controls to it
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.addWidget(self.color_button)
        panel_layout.addWidget(self.font_combo)
        panel_layout.addWidget(self.font_size_slider)
        panel_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins if needed
        panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # Create a time label
        self.time_label = QLabel(self)
        current_pos = self.time_label.pos()

        offset = 50

        new_pos = current_pos - QPoint(0, offset)
        self.time_label.move(new_pos)

        # Create a layout for the time label and center it
        time_layout = QVBoxLayout()
        time_layout.addWidget(self.time_label)
        
        time_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.panel, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        main_layout.addLayout(time_layout)
        main_layout.setStretch(1, 1)  # Allow the time_layout to expand and center

        self.setLayout(main_layout)

        # Set an initial style for the main widget
        self.setStyleSheet("background-color: white;")  # Set an initial background color

        # Set up a timer to update the time label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

        self.update_time()  # Initialize the time label
        self.setWindowTitle("Color Picker Example")
        self.resize(400, 300)  # Adjust size as needed

    def populate_fonts(self):
        # Populate the combo box with available font names
        fonts = QFontDatabase.families()
        self.font_combo.addItems(fonts)

    def change_font(self, font_name):
        # Change the font of the time label based on the selected font
        font = self.time_label.font()
        font.setFamily(font_name)
        self.time_label.setFont(font)
    
    def change_font_size(self, size):
        # Change the font size of the time label based on the slider value
        font = self.time_label.font()
        font.setPixelSize(size)
        self.time_label.setFont(font)
        print(size)

    def open_color_picker(self):
        # Open the color picker dialog
        color = QColorDialog.getColor()
        
        if color.isValid():
            # Change the background color of the main widget
            self.setStyleSheet(f"background-color: {color.name()};")

    def update_time(self):
        # Update the time label with the current time
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(current_time)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ColorPickerExample()
    window.change_font_size(72)
    window.showFullScreen()
    sys.exit(app.exec())
