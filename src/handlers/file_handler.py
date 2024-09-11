from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

import json

class FileHandler:
    def __init__(self, parent):
        self.parent = parent

    def save_styles(self, picker):
        # Create a dictionary with current styles
        styles = {
            "background": {
                "background-color": self.parent.palette().color(self.parent.backgroundRole()).name(),
                "border-image": self.parent.styleSheet().split("border-image: url(")[-1].split(")")[0] if "border-image" in self.parent.styleSheet() else ""
            },
            "font": {
                "font-color": self.parent.time_label.palette().color(self.parent.time_label.foregroundRole()).name(),
                "font-family": self.parent.time_label.font().family(),
                "font-size": self.parent.time_label.font().pointSize(),
            },
            "label": {
                "label-position": self.parent.time_label.alignment(),
                "show-seconds": self.parent.show_seconds
            }
        }


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

        stylesheet = " ".join(stylesheet_parts)
        self.parent.setStyleSheet(stylesheet)

        if "border-image" in styles["background"]:
            if styles['background']['border-image'] != "":
                self.parent.background_handler.change_background_image(styles['background']['border-image'])
        
        # Apply font settings separately
        if "font" in styles:
            if "font-color" in styles['font']:
                self.parent.time_label.setStyleSheet(f"color: {styles['font']['font-color']};")
            if "font-size" in styles['font']:
                new_font = QFont(self.parent.time_label.font().family(), styles['font']['font-size'])
                self.parent.time_label.setFont(new_font)
            if "font-family" in styles['font']:
                current_size = self.parent.time_label.font().pointSize()
                new_font = QFont(styles['font']['font-family'], current_size)
                self.parent.time_label.setFont(new_font)
        if 'label' in styles:
            if "label-position" in styles['label']:
                new_alignment = styles['label']['label-position']
                match new_alignment:
                    case 33:
                        self.parent.time_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                    case 36:
                        self.parent.time_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
                    case 34:
                        self.parent.time_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
                    case 129:
                        self.parent.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                    case 132:
                        self.parent.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                    case 130:
                        self.parent.time_label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
                    case 65:
                        self.parent.time_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
                    case 68:
                        self.parent.time_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
                    case 66:
                        self.parent.time_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
            if "show-seconds" in styles['label']:
                self.show_seconds = styles['label']['show-seconds']
                self.parent.update_time()