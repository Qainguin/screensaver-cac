from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PySide6.QtCore import Qt, QPoint, QSize
import sys, json, random

class StickyNoteWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setFixedSize(200, 200)

        self.bg_color = "hsl(" + str(random.randrange(0, 255)) + ", 100%, 94%" + ")"
        self.setStyleSheet(f"background-color: { self.bg_color }; color: black; border: none;")
        
        # Create a layout and add a text edit and close button
        layout = QVBoxLayout()
        layout.setContentsMargins(16,16,16,16)
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(lambda: parent.file_handler.save_styles(False))
        self.text_edit.setPlaceholderText("Write your note here...")
        layout.addWidget(self.text_edit)

        # Create and style the close button
        self.close_button = QPushButton(self)
        self.close_button.setFixedSize(12, 12)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c;  /* Red color */
                border: none;
                border-radius: 6px;  /* Half of the size to make it a circle */
            }
            QPushButton:hover {
                background-color: #ff3b3b;  /* Darker red on hover */
            }
        """)
        self.close_button.setToolTip("Close")  # Optional: Tooltip for the close button
        self.close_button.clicked.connect(self.close_sticky)

        # Position the close button in the top left
        self.close_button.move(5, 5)
        self.close_button.hide()

        self.setLayout(layout)

        self.old_pos = self.pos()

    def close_sticky(self):
        self.parent.sticky_notes.remove(self)
        self.parent.file_handler.save_styles(False)
        self.close()

    def mousePressEvent(self, event):
        # Store the old position when the mouse is pressed
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        # Allow the window to move when dragging
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()
            self.parent.file_handler.save_styles(False)
        
    def enterEvent(self, event):
        self.close_button.show()
    
    def leaveEvent(self, event):
        self.close_button.hide()

    def to_dict(self):
        """Serialize widget properties to JSON."""
        return {
            'x': self.x(),
            'y': self.y(),
            'bg_color': self.bg_color,
            'text': self.text_edit.toPlainText()
        }

    def from_dict(self, sticky_dict):
        """Deserialize widget properties from JSON."""
        data = sticky_dict
    
        self.move(data.get('x', 0), data.get('y', 0))

        self.bg_color = data.get('bg_color', 0)
        self.setStyleSheet(f"background-color: { self.bg_color }; color: black; border: none;")
        
        self.text_edit.setPlainText(data.get('text', ''))

        return self