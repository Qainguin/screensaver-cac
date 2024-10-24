from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSystemTrayIcon, QMenu, QApplication, QColorDialog, QFileDialog, QMenuBar
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont, QIcon, QAction, QFontDatabase, QCursor
from PySide6.QtCore import Qt, QTime, QTimer, QEasingCurve, QPropertyAnimation

from src.handlers.context_menu_handler import ContextMenuHandler
from src.handlers.file_handler import FileHandler
from src.handlers.background_handler import BackgroundHandler
from src.handlers.label_position_handler import LabelPositionHandler
from src.handlers.font_handler import FontHandler

from src.sticky_note import *
from src.font_selector import *
from src.font_size_slider import *
from src.integrations_window import *
from src.position_changer import *

from idleTime import idle

import platform, json, sys, spotipy

class TimeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.context_menu_handler = ContextMenuHandler(self)
        self.file_handler = FileHandler(self)
        self.background_handler = BackgroundHandler(self)
        self.label_position_handler = LabelPositionHandler(self)
        self.font_handler = FontHandler(self)

        # Initialize fullscreen and seconds booleans
        self.is_fullscreen = False
        self.show_seconds = True

        # Set up the window
        self.setWindowTitle("Screensaver")
        self.resize(400, 300)

        # Create and configure the time label
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.time_label.setFont(QFont("Bahnschrift SemiLight Condensed", 100))

        # Set up the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.time_label)
        self.layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        self.layout.setSpacing(0)  # Space between widgets in the layout
        self.setLayout(self.layout)

        # Set up the timer to update the time label every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Initialize the time label
        self.update_time()

        # Initialize sticky notes
        self.sticky_notes = []

        # Load styles if they exist
        self.file_handler.load_styles(False)

        # Save styles (prevent unloading)
        self.file_handler.save_styles(False)

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
                self.background_handler.change_background_image(filepath)

    def contextMenuEvent(self, event):
        self.context_menu_handler.contextMenuEvent(event)

    def update_time(self):
        print("idle: " + str(idle.get_idle_duration()))
        if idle.get_idle_duration() > 300:
            if not self.is_fullscreen:
                self.showFullScreen()
            
        time_format = "HH:mm:ss"
        if not self.show_seconds:
            time_format = "HH:mm"

        current_time = QTime.currentTime().toString(time_format)

        time_array = current_time.split(":")

        hour = int(time_array[0])

        if hour > 12:
            time_array[0] = str(hour-12)
            hour = int(hour-12)
        if hour < 10:
            time_array[0] = str(hour)

        time_string = ":".join(str(x) for x in time_array)

        self.time_label.setText(time_string)

    def keyPressEvent(self, event):
        if event.key() in {Qt.Key_F11, Qt.Key_Return, Qt.Key_Enter}:
            self.toggle_fullscreen()

    def add_sticky_note(self):
        self.sticky_notes.append(StickyNoteWidget(self))
        self.layout.addWidget(self.sticky_notes[-1])
        self.sticky_notes[-1].show()

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
        font_selector = FontSelector(self, fonts, self.font_handler.change_font)

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
        
    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showMaximized()  # Exit fullscreen
        else:
            self.showFullScreen()  # Enter fullscreen
        self.is_fullscreen = not self.is_fullscreen  # Toggle the state

    def toggle_show_seconds(self, val: bool):
        self.show_seconds = not self.show_seconds
        self.update_time()
        self.file_handler.save_styles(False)
