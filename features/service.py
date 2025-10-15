import time
import threading
import datetime
from features.repository import Repository
from features.utils import Utils
from collections import defaultdict


class Service:
    def __init__(self):
        self.repo = Repository()
        self.utils = Utils()
        # Creates a dictionary of floats for daily usage
        self.daily_usage = defaultdict(float)
        # Creates a dictionary of floats for app usage
        self.usage_log = defaultdict(float)
        # Records the time of when the screentime starts
        self.screentime_start = time.time()
        self.usage_start = time.time()  # Records the time of when app usage starts
        self.app_limits = {}  # Dictionary for app limits
        self.load_app_limits()
        self.current_app = None
        self.running = True

    # Starts tracking screentime
    def track_screentime(self):
        while self.running:
            # Gets the name of active app and date
            active_app = self.utils.get_active_app()
            today = datetime.datetime.now().strftime("%Y-%m-%d")

            if active_app:
                # Gets total seconds of screentime(elapsed) by subtracting current time with the time of when the program started
                elapsed = time.time() - self.screentime_start
                # Adds elapsed to daily usage dictionary
                self.daily_usage[today] += elapsed
                self.repo.log_screentime(elapsed)  # Logs info into database

            self.screentime_start = time.time()  # Resets the start of screentime
            time.sleep(1)  # 1 second delay before tracking

    def track_usage(self):
        while self.running:
            # Gets the name of active app
            active_app = self.utils.get_active_app()

            # Tracks when you switch apps
            if active_app != self.current_app:
                if self.current_app:  # Only records usage data of the previous app
                    usage_time = time.time() - self.usage_start
                    self.usage_log[self.current_app] += usage_time
                    # Logs info into database
                    self.repo.log_app_usage(self.current_app, usage_time)
                    # Shows which apps the user switches from and switches to
                    print(f"Switched from {self.current_app} to {active_app}")

                # Turns active app into current app if the user switches or exits
                self.current_app = active_app
                self.usage_start = time.time()  # Resets the start of app usage

            # Track app usage live (every second)
            if self.current_app:
                usage_time = time.time() - self.usage_start
                total_seconds = self.usage_log[self.current_app] + usage_time
                limit_seconds = self.app_limits.get(self.current_app)

                # Closes the app if the usage exceeds app limit
                if limit_seconds and total_seconds >= limit_seconds:
                    print(f"Limit reached for {self.current_app}")
                    self.utils.show_warning(self.current_app, 5)
                    self.utils.close_app(self.current_app)
                    self.current_app = None
                    self.usage_start = time.time()

            time.sleep(1)

    # Threads track_screentime and track_usage together so that they run at the same time
    def start_tracking(self):
        thread1 = threading.Thread(target=self.track_screentime, daemon=True)
        thread2 = threading.Thread(target=self.track_usage, daemon=True)

        thread1.start()
        thread2.start()

        print("Tracking started. (Press Ctrl + C to stop.)")

    # Stops tracking
    def stop_tracking(self):
        self.running = False
        print("Tracking stopped.")

    # Formats screentime for GUI
    def format_screentime_today(self):
        total_seconds = self.repo.get_screentime_today()
        if total_seconds is None:
            return "0h 0min"
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}min"

    # Allows the user to set an app limit for a chosen app and saves it into applimit database
    def set_app_limit(self, app_name, hours, minutes):
        total_seconds = Utils.convert(hours, minutes)
        self.repo.save_app_limit(app_name, total_seconds)
        self.app_limits[app_name] = total_seconds
        print(
            f"Limit set for {app_name}: {hours} hour(s) and {minutes} minute(s)")

    # Loads the app limits from applimit database
    def load_app_limits(self):
        limits = self.repo.get_app_limits()
        for app_limit in limits:
            self.app_limits[app_limit.app_name] = app_limit.limit_seconds
