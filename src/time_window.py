from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSystemTrayIcon, QMenu, QApplication, QColorDialog, QFileDialog, QMenuBar
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont, QIcon, QAction, QFontDatabase, QCursor
from PySide6.QtCore import Qt, QTime, QTimer

from src.font_selector import *
from src.font_size_slider import *
from src.integrations_window import *
from src.position_changer import *

import platform, json, sys, spotipy

class TimeWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Screensaver")
        self.resize(400, 300)

        # Create and configure the time label
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.time_label.setFont(QFont("Bahnschrift SemiLight Condensed", 100))

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        layout.setSpacing(0)  # Space between widgets in the layout
        self.setLayout(layout)

        # Set up the timer to update the time label every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Initialize the time label
        self.update_time()

        # Load styles if they exist
        self.load_styles(False)

        # Initialize system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        if platform.system() == "Darwin":  # macOS
            self.tray_icon.setIcon(QIcon("resource/black_icon.png"))  # Path to black icon
        else:  # Windows or other OS
            self.tray_icon.setIcon(QIcon("resource/white_icon.png"))  # Path to white icon
        self.tray_icon.setToolTip("Screensaver Application")

        # Create tray icon menu
        tray_menu = QMenu(self)
        show_action = QAction("Show Window", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.showMaximized)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        tray_menu.setStyleSheet("background: #1e1e1e; color: white; border-image: none;")
        self.tray_icon.setContextMenu(tray_menu)

        # Show the tray icon
        self.tray_icon.show()

        # Allow drag & drop
        self.setAcceptDrops(True)

        # Hide the main window initially
        self.hide()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                filepath = url.toLocalFile()
                print("Dropped file: ", filepath)
                self.change_background_image(filepath)

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")

        time_array = current_time.split(":")

        hour = int(time_array[0])

        if hour > 12:
            time_array[0] = str(hour-12)
            hour = int(hour-12)
        if hour < 10:
            time_array[0] = str(hour)

        time_string = ":".join(str(x) for x in time_array)

        self.time_label.setText(time_string)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("background: #1e1e1e; color: white; border-image: none;")

        # Create actions
        change_bg_action = QAction("Change Background Color", self)
        change_bg_image_action = QAction("Change Background Image", self)
        change_font_color_action = QAction("Change Font Color", self)
        change_font_action = QAction("Change Font", self)
        change_font_size_action = QAction("Change Font Size", self)
        show_label_position_changer_action = QAction("Change Label Position", self)
        save_styles_action = QAction("Save Styles", self)
        load_styles_action = QAction("Load Styles", self)
        integrations_action = QAction("Integrations", self)

        # Connect actions to slots
        change_bg_action.triggered.connect(self.change_background_color)
        change_bg_image_action.triggered.connect(lambda: self.change_background_image(""))
        change_font_color_action.triggered.connect(self.change_font_color)
        change_font_action.triggered.connect(self.show_font_selector)
        change_font_size_action.triggered.connect(self.show_font_size_slider)
        show_label_position_changer_action.triggered.connect(self.show_label_position_changer)
        save_styles_action.triggered.connect(self.save_style_to_file)
        load_styles_action.triggered.connect(self.load_styles)
        integrations_action.triggered.connect(self.show_integrations)

        # Add actions to the menu
        menu.addSection("Background")
        menu.addAction(change_bg_action)
        menu.addAction(change_bg_image_action)
        menu.addSection("Text")
        menu.addAction(change_font_color_action)
        menu.addAction(change_font_action)
        menu.addAction(change_font_size_action)
        menu.addSection("Label")
        menu.addAction(show_label_position_changer_action)
        menu.addSection("Data")
        menu.addAction(save_styles_action)
        menu.addAction(load_styles_action)
        menu.addSection("Misc")
        menu.addAction(integrations_action)

        # Execute the menu at the right-click position
        menu.exec(event.globalPos())

    def save_style_to_file(self):
        self.save_styles(True)

    def load_style_from_file(self):
        self.load_styles(True)

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background: {color.name()};")
            self.save_styles(False)

    def change_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.time_label.setStyleSheet(f"color: {color.name()};")
            self.save_styles(False)

    def show_label_position_changer(self):
        changer = PositionChanger(self)

        app = QApplication.instance()
        size = app.primaryScreen().size()
        changer.setGeometry((size.width()/2)-150, (size.height()/2)-150, 300, 300)

        changer.exec()

    def show_integrations(self):
        integ = Integrations(self)

        app = QApplication.instance()
        size = app.primaryScreen().size()
        integ.setGeometry((size.width()/2)-200, (size.height()/2)-50, 400, 100)

        integ.exec()


    def show_font_selector(self):
        fonts = sorted(set(QFontDatabase.families()))
        font_selector = FontSelector(self, fonts, self.change_font)

        app = QApplication.instance()
        size = app.primaryScreen().size()
        font_selector.setGeometry((size.width()/2)-(font_selector.width()/2), (size.height()/2)-(font_selector.height()/2), font_selector.width(), font_selector.height())
        
        font_selector.setStyleSheet("background: #1e1e1e; border-image: none; color: white;")
        font_selector.search_bar.setStyleSheet("background: #1e1e1e; border-image: none; color: white;")
        font_selector.exec()  # Show the font selector as a modal dialog

    def show_font_size_slider(self):
        slider = FontSizeSlider(self, self.time_label.font().pointSize())

        app = QApplication.instance()
        size = app.primaryScreen().size()
        slider.setGeometry((size.width()/2)-(slider.width()/2), (size.height()/2)-(slider.height()/2), slider.width(), slider.height())

        slider.setStyleSheet("background: 1e1e1e; border-image: none;")
        slider.exec()

    def change_background_image(self, path: str = ""):
        if path == "":
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "", "Images (*.png *.jpg *.bmp)")
        else:
            file_name = path

        if file_name:
            self.setStyleSheet(f"border-image: url({file_name}) 0 0 0 0 stretch stretch; background-repeat: no-repeat; background-position: center; margin: 0rem; padding: 0;")
            self.save_styles(False)
        else:
            self.setStyleSheet("background-color: lightblue;")  # Reset to default if no file is selected
        

    def save_styles(self, picker):
        # Create a dictionary with current styles
        styles = {
            "background": {
                "background-color": self.palette().color(self.backgroundRole()).name(),
                "border-image": self.styleSheet().split("border-image: url(")[-1].split(")")[0] if "border-image" in self.styleSheet() else ""
            },
            "font": {
                "font-color": self.time_label.palette().color(self.time_label.foregroundRole()).name(),
                "font-family": self.time_label.font().family(),
                "font-size": self.time_label.font().pointSize(),
            },
            "label": {
                "label-position": self.time_label.alignment()
            }
        }

        print(styles)


        # Convert dictionary to JSON
        json_string = json.dumps(styles, indent=4)

        # Save to file
        if picker:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Styles", "", "JSON Files (*.json)")
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(json_string)
        else:
            file_name = "save.json"
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(json_string)

    def load_styles(self, picker):
        # Load JSON file
        if picker:
            file_name, _ = QFileDialog.getOpenFileName(self, "Load Styles", "", "JSON Files (*.json)")
        else:
            file_name = "save.json"
        
        if file_name:
            with open(file_name, 'r') as file:
                json_string = file.read()

            # Apply styles from JSON
            self.apply_styles_from_json(json_string)

    def apply_styles_from_json(self, json_string):
        styles = json.loads(json_string)

        # Construct the stylesheet from the parsed JSON
        stylesheet_parts = []
        if 'background' in styles:
            if "background-color" in styles['background']:
                stylesheet_parts.append(f"background-color: {styles['background']['background-color']};")
            if "border-image" in styles and styles["border-image"]:
                stylesheet_parts.append(f"border-image: url({styles['background']['border-image']}) 0 0 0 0 stretch stretch; background-repeat: no-repeat; background-position: center;")

        stylesheet = " ".join(stylesheet_parts)
        self.setStyleSheet(stylesheet)
        
        # Apply font settings separately
        if "font" in styles:
            if "font-color" in styles['font']:
                self.time_label.setStyleSheet(f"color: {styles['font']['font-color']};")
            if "font-size" in styles['font']:
                new_font = QFont(self.time_label.font().family(), styles['font']['font-size'])
                self.time_label.setFont(new_font)
            if "font-family" in styles['font']:
                current_size = self.time_label.font().pointSize()
                new_font = QFont(styles['font']['font-family'], current_size)
                self.time_label.setFont(new_font)
        if 'label' in styles:
            if "label-position" in styles['label']:
                new_alignment = styles['label']['label-position']
                match new_alignment:
                    case 33:
                        self.time_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                    case 36:
                        self.time_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
                    case 34:
                        self.time_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
                    case 129:
                        self.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    case 132:
                        self.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                    case 130:
                        self.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    case 65:
                        self.time_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
                    case 68:
                        self.time_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
                    case 66:
                        self.time_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
            

    def change_font(self, font_name):
        current_font = self.time_label.font()
        new_font = QFont(font_name, current_font.pointSize())
        self.time_label.setFont(new_font)
        self.save_styles(False)
    
    def change_font_size(self, font_size):
        current_font = self.time_label.font()
        new_font = QFont(current_font.family(), font_size)
        self.time_label.setFont(new_font)
        self.save_styles(False)
    
    def change_label_position(self, position: int):
        match position:
            case 0:
                self.time_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            case 1:
                self.time_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
            case 2:
                self.time_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
            case 3:
                self.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            case 4:
                self.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            case 5:
                self.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
            case 6:
                self.time_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
            case 7:
                self.time_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
            case 8:
                self.time_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.save_styles(False)
