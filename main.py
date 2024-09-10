from PySide6.QtWidgets import QApplication
from src.time_window import *
import sys

if sys.platform.startswith('darwin'):
    # Set app name, if PyObjC is installed
    # Python 2 has PyObjC preinstalled
    # Python 3: pip3 install pyobjc-framework-Cocoa
    try:
        from Foundation import NSBundle
        bundle = NSBundle.mainBundle()
        if bundle:
            app_name = "Screensaver"
            app_info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
            if app_info:
                app_info['CFBundleName'] = app_name
    except ImportError:
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeWindow()
    window.showMaximized()
    sys.exit(app.exec())
