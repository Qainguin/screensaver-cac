# context_menu.py

from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

class ContextMenuHandler:
    def __init__(self, parent):
        self.parent = parent

    def contextMenuEvent(self, event):
        menu = QMenu(self.parent)
        menu.setStyleSheet("background: #1e1e1e; color: white; border-image: none; padding: 8 0 8 0")

        # Create actions
        change_bg_action = QAction("Change Background Color", self.parent)
        change_bg_image_action = QAction("Change Background Image", self.parent)
        change_font_color_action = QAction("Change Font Color", self.parent)
        change_font_action = QAction("Change Font", self.parent)
        change_font_size_action = QAction("Change Font Size", self.parent)
        show_label_position_changer_action = QAction("Change Label Position", self.parent)
        show_seconds_toggle_action = QAction("Show Seconds", self.parent)
        show_seconds_toggle_action.setCheckable(True)
        show_seconds_toggle_action.setChecked(self.parent.show_seconds)
        save_styles_action = QAction("Save Styles", self.parent)
        load_styles_action = QAction("Load Styles", self.parent)
        integrations_action = QAction("Integrations", self.parent)

        # Connect actions to slots
        change_bg_action.triggered.connect(self.parent.background_handler.change_background_color)
        change_bg_image_action.triggered.connect(lambda: self.parent.background_handler.change_background_image(""))
        change_font_color_action.triggered.connect(self.parent.font_handler.change_font_color)
        change_font_action.triggered.connect(self.parent.show_font_selector)
        change_font_size_action.triggered.connect(self.parent.show_font_size_slider)
        show_label_position_changer_action.triggered.connect(self.parent.show_label_position_changer)
        show_seconds_toggle_action.triggered.connect(self.parent.toggle_show_seconds)
        save_styles_action.triggered.connect(lambda: self.parent.file_handler.save_styles(True))
        load_styles_action.triggered.connect(self.parent.file_handler.load_styles)
        integrations_action.triggered.connect(self.parent.show_integrations)

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
        menu.addAction(show_seconds_toggle_action)
        menu.addSection("Data")
        menu.addAction(save_styles_action)
        menu.addAction(load_styles_action)
        menu.addSection("Misc")
        menu.addAction(integrations_action)

        # Execute the menu at the right-click position
        menu.exec(event.globalPos())
