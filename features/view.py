from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
import matplotlib
matplotlib.use("QtAgg")


# Graphs the daily screentime as a bar graph using matplotlib
class GraphScreentime(FigureCanvas):

    def __init__(self, repo, parent=None):
        self.repo = repo
        # Creates figure
        fig = Figure(figsize=(6, 7))
        # Add area in figure where graph will be drawn
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.plot_screentime()

    def plot_screentime(self):
        # Gets data from dailyusage database
        data = self.repo.get_screentime()

        # Displays text if there is no data to plot
        if not data:
            self.ax.text(0.5, 0.5, "No data found", ha="center", va="center")
            self.draw()
            return

        # Loops through data in dailyusage and converts date(string) into datetime format
        dates = [datetime.datetime.strptime(d.date, "%Y-%m-%d") for d in data]
        # Loops through dates and converts into weekday abbreviations
        weekdays = [date.strftime("%a") for date in dates]
        # Loops through data in dailyusage and converts total_seconds into hours
        hours = [round(d.total_seconds / 3600, 2) for d in data]

        # Customize bar graph
        font_screentime = {"fontsize": 14, "fontname": "Charter"}
        tick_font = {"fontsize": 11, "fontname": "Charter", "color": "#523C3C"}
        self.ax.clear()
        # Shows weekdays at the bottom, hours at the side, and color bars
        self.ax.bar(weekdays, hours, color="#523C3C")
        self.ax.set_facecolor("#EDEEF0")
        self.figure.set_facecolor("#EDEEF0")
        self.ax.set_xlabel("Day of the Week", fontdict=font_screentime)
        self.ax.set_ylabel("Screen Time (Hours)", fontdict=font_screentime)
        self.ax.set_title("Screen Time per Day", fontdict=font_screentime)
        self.ax.tick_params(
            axis='x', colors=tick_font["color"], labelsize=tick_font["fontsize"])
        self.ax.tick_params(
            axis='y', colors=tick_font["color"], labelsize=tick_font["fontsize"])
        self.draw()

# Graphs the app usage as a pie chart using matplotlib


class GraphAppUsage(FigureCanvas):
    def __init__(self, repo, parent=None):
        self.repo = repo
        # Create figure
        fig = Figure(figsize=(12, 12))
        # Add area in figure where graph will be drawn
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.plot_usage()

    def plot_usage(self):
        # Gets data from appusage database
        data = self.repo.get_usage()

        # Displays text if there is no data to plot
        if not data:
            self.ax.text(0.5, 0.5, "No data found", ha="center", va="center")
            self.draw()
            return

        # Records today's date and converts it into a string
        today = datetime.date.today().strftime("%Y-%m-%d")
        # Loops through data in appusage and acquires only today's data records
        today_data = [row for row in data if row.date == today]

        # Displays text if no data has been found
        if not today_data:
            self.ax.text(0.5, 0.5, "No app usage today",
                         ha="center", va="center")
            self.draw()
            return

        # Loops through the apps used today and records the app name and total seconds before converting seconds to hours
        apps = [row.app_name for row in today_data]
        seconds = [row.total_seconds for row in today_data]
        hours = [round(sec / 3600, 2) for sec in seconds]

        font_appusage = {"fontsize": 13, "fontname": "Charter"}
        font_appname = {"fontsize": 11, "fontname": "Charter"}
        colors = ["#78290F", "#15616D", "#FFECD1", "#FF7D00", "#001524"]
        self.ax.clear()
        wedges, texts, autotexts = self.ax.pie(
            hours,              # Basis for the size of each slice
            labels=apps,        # App names as labels
            autopct=lambda p: f"{p:.1f}%",  # Percentage inside slices
            startangle=140,
            colors=colors
        )
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(12)
        for text in texts:
            text.set_fontfamily("Charter")
            text.set_fontsize(11)
        self.ax.set_title("App Usage for Today", fontdict=font_appusage)
        self.ax.set_facecolor("#EDEEF0")
        self.figure.set_facecolor("#EDEEF0")
        self.draw()
