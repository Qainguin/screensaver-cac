from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QWidget, QScrollArea, QPushButton
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt

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
        self.save_styles(False)
        self.accept()  # Close the dialog when a font is selected