from features.service import Service
from shell.windows import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    service = Service()
    service.start_tracking()

    window = MainWindow(service)

    # Applies CSS elements to GUI
    with open("mainwindow.qss", "r") as style_file:
        app.setStyleSheet(style_file.read())

    window.show()

    sys.exit(app.exec())
