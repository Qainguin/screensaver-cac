import json
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMenu, QColorDialog, QScrollArea, QPushButton, QLineEdit, QDialog, QFileDialog
from PySide6.QtGui import QFont, QFontDatabase, QAction, QCursor
from PySide6.QtCore import QTimer, QTime, Qt, QPoint
import sys

class FontSelector(QDialog):
    def __init__(self, parent, fonts, font_change_callback):
        super().__init__(parent)
        self.font_change_callback = font_change_callback
        self.setWindowTitle("Select Font")
        self.setGeometry(100, 100, 300, 400)  # Ensure the window is visible with appropriate size
        self.setStyleSheet("")

        # Set up layout
        layout = QVBoxLayout(self)

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setStyleSheet("")
        self.search_bar.setPlaceholderText("Search fonts...")
        self.search_bar.textChanged.connect(self.filter_fonts)
        layout.addWidget(self.search_bar)

        # Font list
        self.font_list_widget = QWidget(self)
        self.font_list_widget.setStyleSheet("")
        self.font_list_layout = QVBoxLayout(self.font_list_widget)
        self.font_list_widget.setLayout(self.font_list_layout)

        # Scroll area for font list
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.font_list_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("")
        layout.addWidget(scroll_area)

        # Populate the font list
        self.all_fonts = fonts
        self.filtered_fonts = fonts
        self.update_font_list()

        self.setLayout(layout)

    def update_font_list(self):
        # Clear current font list
        for i in reversed(range(self.font_list_layout.count())):
            widget = self.font_list_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add font buttons to the layout
        for font_name in self.filtered_fonts:
            button = QPushButton(font_name, self)
            button.setFont(QFont(font_name, 12))  # Set font size for visibility in menu
            button.setStyleSheet("color: white;")
            button.setFixedWidth(250)  # Set fixed width for the buttons
            button.clicked.connect(lambda checked, font=font_name: self.change_font(font))
            self.font_list_layout.addWidget(button)

    def filter_fonts(self):
        search_term = self.search_bar.text().lower()
        self.filtered_fonts = [font for font in self.all_fonts if search_term in font.lower()]
        self.update_font_list()

    def change_font(self, font_name):
        self.font_change_callback(font_name)
        self.accept()  # Close the dialog when a font is selected

class TimeWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Time Window")
        self.resize(400, 300)

        # Create and configure the time label
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont("Bahnschrift SemiLight Condensed", 100))

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        self.setLayout(layout)

        # Set up the timer to update the time label every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Initialize the time label
        self.update_time()

        # Load styles if they exist
        self.load_styles()

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(current_time)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("background-color: white; color: black;")

        # Create actions
        change_bg_action = QAction("Change Background Color", self)
        change_font_action = QAction("Change Font", self)
        change_bg_image_action = QAction("Change Background Image", self)
        change_font_color_action = QAction("Change Font Color", self)
        save_styles_action = QAction("Save Styles", self)
        load_styles_action = QAction("Load Styles", self)

        # Connect actions to slots
        change_bg_action.triggered.connect(self.change_background_color)
        change_font_action.triggered.connect(self.show_font_selector)
        change_bg_image_action.triggered.connect(self.change_background_image)
        change_font_color_action.triggered.connect(self.change_font_color)
        save_styles_action.triggered.connect(self.save_styles)
        load_styles_action.triggered.connect(self.load_styles)

        # Add actions to the menu
        menu.addAction(change_bg_action)
        menu.addAction(change_font_color_action)
        menu.addAction(change_font_action)
        menu.addAction(change_bg_image_action)
        menu.addAction(save_styles_action)
        menu.addAction(load_styles_action)

        # Execute the menu at the right-click position
        menu.exec(event.globalPos())

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()};")

    def change_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.time_label.setStyleSheet(f"color: {color.name()};")

    def show_font_selector(self):
        fonts = sorted(set(QFontDatabase.families()))
        font_selector = FontSelector(self, fonts, self.change_font)

        # Position the font selector dialog at the cursor position
        cursor_position = QCursor.pos()
        font_selector.setGeometry(cursor_position.x(), cursor_position.y(), font_selector.width(), font_selector.height())
        
        font_selector.setStyleSheet("background: #1e1e1e;")
        font_selector.search_bar.setStyleSheet("background: #1e1e1e;")
        font_selector.exec()  # Show the font selector as a modal dialog

    def change_background_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.setStyleSheet(f"background-image: url({file_name}); background-repeat: no-repeat; background-position: center; background-size: cover;")
        else:
            self.setStyleSheet("background-color: lightblue;")  # Reset to default if no file is selected

    def save_styles(self):
        # Create a dictionary with current styles
        styles = {
            "background-color": self.palette().color(self.backgroundRole()).name(),
            "font-color": self.time_label.palette().color(self.time_label.foregroundRole()).name(),
            "font-family": self.time_label.font().family(),
            "background-image": self.styleSheet().split("background-image: url(")[-1].split(");")[0] if "background-image" in self.styleSheet() else ""
        }

        # Convert dictionary to JSON
        json_string = json.dumps(styles, indent=4)

        # Save to file
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Styles", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'w') as file:
                file.write(json_string)

    def load_styles(self):
        # Load JSON file
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Styles", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as file:
                json_string = file.read()

            # Apply styles from JSON
            self.apply_styles_from_json(json_string)

    def apply_styles_from_json(self, json_string):
        styles = json.loads(json_string)

        # Construct the stylesheet from the parsed JSON
        stylesheet_parts = []
        if "background-color" in styles:
            stylesheet_parts.append(f"background-color: {styles['background-color']};")
        if "background-image" in styles and styles["background-image"]:
            stylesheet_parts.append(f"background-image: url({styles['background-image']}); background-repeat: no-repeat; background-position: center; background-size: cover;")
        
        stylesheet = " ".join(stylesheet_parts)
        self.setStyleSheet(stylesheet)
        
        # Apply font settings separately
        if "font-color" in styles:
            self.time_label.setStyleSheet(f"color: {styles['font-color']};")
        if "font-family" in styles:
            current_size = self.time_label.font().pointSize()
            new_font = QFont(styles['font-family'], current_size)
            self.time_label.setFont(new_font)

    def change_font(self, font_name):
        current_font = self.time_label.font()
        new_font = QFont(font_name, current_font.pointSize())
        self.time_label.setFont(new_font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeWindow()
    window.show()
    sys.exit(app.exec())
