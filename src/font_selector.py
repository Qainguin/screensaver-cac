from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QScrollArea
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class FontSelector(QDialog):
    def __init__(self, parent, fonts, font_change_callback):
        super().__init__(parent)
        self.font_change_callback = font_change_callback
        self.setWindowTitle("Select Font")
        self.setGeometry(100, 100, 300, 400)  # Ensure the window is visible with appropriate size
        self.setStyleSheet("background: #1e1e1e; color: white;")

        # Set up layout
        layout = QVBoxLayout(self)

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setStyleSheet("color: white;")
        self.search_bar.setPlaceholderText("Search fonts...")
        self.search_bar.textChanged.connect(self.filter_fonts)
        layout.addWidget(self.search_bar)

        # Font list
        self.font_list = QListWidget(self)
        self.font_list.setStyleSheet("color: white;")
        self.font_list.itemClicked.connect(self.change_font)
        layout.addWidget(self.font_list)

        # Populate the font list
        self.all_fonts = fonts
        self.filtered_fonts = fonts
        self.update_font_list()

        self.setLayout(layout)

    def update_font_list(self):
        # Clear current font list
        self.font_list.clear()

        # Add fonts to the list
        self.font_list.addItems(self.filtered_fonts)

    def filter_fonts(self):
        search_term = self.search_bar.text().lower()
        self.filtered_fonts = [font for font in self.all_fonts if search_term in font.lower()]
        self.update_font_list()

    def change_font(self, item):
        font_name = item.text()
        print("Changing Font")
        self.font_change_callback(font_name)
        self.accept()  # Close the dialog when a font is selected
