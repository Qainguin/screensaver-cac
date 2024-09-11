from PySide6.QtCore import Qt

class LabelPositionHandler:
    def __init__(self, parent):
        self.parent = parent

    def change_label_position(self, position: int):
        match position:
            case 0:
                self.parent.time_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            case 1:
                self.parent.time_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
            case 2:
                self.parent.time_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
            case 3:
                self.parent.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            case 4:
                self.parent.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            case 5:
                self.parent.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
            case 6:
                self.parent.time_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
            case 7:
                self.parent.time_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
            case 8:
                self.parent.time_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.parent.file_handler.save_styles(False)