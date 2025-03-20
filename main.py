import sys
from PySide6.QtWidgets import QApplication
from src.app_manager import AppManager

def start():

    app = QApplication(sys.argv)

    manager = AppManager()

    manager.start_app()



    sys.exit(app.exec())


if __name__ == "__main__":
    start()