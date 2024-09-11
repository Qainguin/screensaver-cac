from PySide6.QtWidgets import QColorDialog, QFileDialog

class BackgroundHandler:
    def __init__(self, parent):
        self.parent = parent

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent.setStyleSheet(f"background: {color.name()};")
            self.parent.file_handler.save_styles(False)
    
    def change_background_image(self, path: str = ""):
        if path == "" or path == "\n":
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "", "Images (*.png *.jpg *.bmp)")
        else:
            file_name = path

        if file_name:
            self.parent.setStyleSheet(f"border-image: url({file_name}) 0 0 0 0 stretch stretch; background-repeat: no-repeat; background-position: center; margin: 0rem; padding: 0;")
            self.parent.file_handler.save_styles(False)