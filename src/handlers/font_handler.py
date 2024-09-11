from PySide6.QtWidgets import QColorDialog
from PySide6.QtGui import QFont

class FontHandler:
    def __init__(self, parent):
        self.parent = parent
    
    def change_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent.time_label.setStyleSheet(f"color: {color.name()};")
            self.parent.file_handler.save_styles(False)
    
    def change_font(self, font_name):
        current_font = self.parent.time_label.font()
        new_font = QFont(font_name, current_font.pointSize())
        self.parent.time_label.setFont(new_font)
        self.parent.file_handler.save_styles(False)
    
    def change_font_size(self, font_size):
        current_font = self.parent.time_label.font()
        new_font = QFont(current_font.family(), font_size)
        self.parent.time_label.setFont(new_font)
        self.parent.file_handler.save_styles(False)