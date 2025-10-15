from features.view import GraphScreentime, GraphAppUsage
from features.utils import Utils
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import os
import random


class MainWindow(QMainWindow):
    def __init__(self, service):
        super().__init__()
        self.setWindowTitle("Screen Time Monitor")
        self.setGeometry(90, 50, 1280, 832)
        self.service = service
        self.utils = Utils()

        central = QWidget()
        layout = QVBoxLayout()
        self.setCentralWidget(central)

        # section1

        self.time_lbl = QLabel(self)
        self.screentime_lbl = QLabel(self)
        self.text_lbl = QLabel("Screentime Today", self)
        self.time_lbl.setContentsMargins(30, 0, 0, 0)

        formatted_screentime = self.service.format_screentime_today()
        self.screentime_lbl.setText(f"{formatted_screentime}")

        layout.addWidget(
            self.time_lbl, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(
            self.text_lbl, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(
            self.screentime_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)

        # graph
        self.graph_screentime = GraphScreentime(self.service.repo)
        layout.addWidget(self.graph_screentime)
        layout.addStretch()

        # section2
        section2 = QHBoxLayout()
        self.pie_btn = QPushButton("App Usage", self)
        self.note_lbl = QLabel(self)
        self.limit_btn = QPushButton("Set App Limit", self)
        layout.addWidget(
            self.note_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)
        section2.addWidget(self.pie_btn)
        section2.addWidget(self.limit_btn)
        layout.addLayout(section2)

        # set for css
        central.setObjectName("centralwidget")
        self.time_lbl.setObjectName("timelbl")
        self.screentime_lbl.setObjectName("screentimelbl")
        self.text_lbl.setObjectName("textlbl")
        self.pie_btn.setObjectName("piebtn")
        self.note_lbl.setObjectName("notelbl")
        self.limit_btn.setObjectName("limitbtn")

        self.pie_btn.clicked.connect(self.open_appusage)
        self.limit_btn.clicked.connect(self.set_limit)

        central.setLayout(layout)

        # Updates time every minute
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()
        self.random_note()
        self.start_updating_screentime()

    # Update time
    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm ap")
        self.time_lbl.setText(current_time)

    # Randomly chooses a fact from notes.txt and displays a different one everytime the program runs
    def random_note(self):
        file = os.path.join(os.path.dirname(__file__), "notes.txt")
        try:
            with open(file, "r") as f:
                notes = [line.strip() for line in f if line.strip()]

                if notes:
                    random_note = random.choice(notes)
                    self.note_lbl.setText(random_note)

        except FileNotFoundError:
            self.note_lbl.setText("Error: notes.txt not found!")

    # Displays pop ups where user can set app limits
    def set_limit(self):
        app_name = Utils.choose_app()
        if not app_name:
            QMessageBox.warning(self, "Error", "No app selected.")
            return

        # Get hour limit
        hours, ok1 = QInputDialog.getDouble(
            self, "Set Limit", f"Enter limit for {app_name} (in hours):", 0.0, 0, 24, 1)
        if not ok1:
            return

        # Get minute limit
        minutes, ok2 = QInputDialog.getInt(
            self, "Set Limit", f"Enter additional minutes for {app_name}:", 0, 0, 59, 1)
        if not ok2:
            return

        # Set as app limit and display confirmation
        self.service.set_app_limit(app_name, hours, minutes)
        QMessageBox.information(
            self, "Limit Set", f"Limit for {app_name}: {int(hours)} hour(s) and {int(minutes)} minute(s)")

    # Opens AppUsageWindow
    def open_appusage(self):
        self.app_usage_window = AppUsageWindow(self.service.repo)
        self.app_usage_window.show()

    # Closes app and stops tracker when the user closes the window
    def closeEvent(self, event):
        print("Closing app and stopping tracker...")
        self.service.stop_tracking()
        event.accept()

    # Updates the screentime live
    def start_updating_screentime(self):
        self.timer_screentime = QTimer(self)
        self.timer_screentime.timeout.connect(self.update_screentime)
        self.timer_screentime.start(1000)

    def update_screentime(self):
        formatted = self.service.format_screentime_today()
        self.screentime_lbl.setText(formatted)


class AppUsageWindow(QWidget):
    def __init__(self, repo):
        super().__init__()
        self.repo = repo
        self.setWindowTitle("App Usage")
        self.setGeometry(250, 60, 1000, 800)

        layout = QVBoxLayout()

        self.graph_app_usage = GraphAppUsage(self.repo)
        layout.addWidget(self.graph_app_usage)

        self.back_btn = QPushButton("Close")
        layout.addWidget(
            self.back_btn, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.back_btn.clicked.connect(self.close)

        self.back_btn.setObjectName("backbtn")

        qss_path = os.path.join(os.path.dirname(
            __file__), "appusagewindow.qss")
        with open(qss_path, "r") as style_sheet2:
            self.setStyleSheet(style_sheet2.read())

        self.setLayout(layout)
