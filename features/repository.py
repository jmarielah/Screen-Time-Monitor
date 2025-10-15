from core.db import get_connection
from datetime import *
from features.models import DailyUsage, AppUsage, AppLimit


class Repository:

    def __init__(self, connection=get_connection):
        self.connection = connection
        conn = self.connection()
        cursor = conn.cursor()

        # Create tables in database(screentime, app usage, app limits)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dailyusage(
                    date TEXT PRIMARY KEY,
                    total_seconds REAL
                    )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS appusage(
                    app_name TEXT,
                    date TEXT,
                    total_seconds REAL,
                    PRIMARY KEY (app_name, date)
                        )""")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applimit (
                app_name TEXT PRIMARY KEY,
                limit_seconds INTEGER
            )
        ''')

        conn.commit()
        conn.close()

    # Logs screentime(in seconds) and date in database
    def log_screentime(self, elapsed: float):
        conn = self.connection()
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            "INSERT OR IGNORE INTO dailyusage (date, total_seconds) VALUES (?,?)", (today, 0))
        # Updates screentime according to the date
        cursor.execute(
            "UPDATE dailyusage set total_seconds = total_seconds + ? WHERE date =?", (
                elapsed, today)
        )
        conn.commit()
        conn.close()

    # Logs app usage (with name of app, date used, and the total seconds it was used for) into database
    def log_app_usage(self, app: str, elapsed: float):
        conn = self.connection()
        cursor = conn.cursor()

        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("INSERT OR IGNORE INTO appusage (app_name, date, total_seconds) VALUES (?, ?, ?)",
                       (app, today, 0))
        # Updates app usage according to date and name of app
        cursor.execute("UPDATE appusage SET total_seconds = total_seconds + ? WHERE app_name = ? AND date = ?",
                       (elapsed, app, today))

        conn.commit()
        conn.close()

    # Saves the time limit the user sets into database
    def save_app_limit(self, app_name, seconds):
        conn = self.connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO applimit (app_name, limit_seconds)
            VALUES (?, ?)
            ON CONFLICT(app_name) DO UPDATE SET limit_seconds = excluded.limit_seconds
        ''', (app_name, seconds))

        conn.commit()
        conn.close()

    # Retrieves data from dailyusage database
    def get_screentime(self):
        conn = self.connection()
        cursor = conn.cursor()
        rows = cursor.execute(
            "SELECT date, total_seconds FROM dailyusage ORDER BY date ASC").fetchall()
        conn.close()
        return [DailyUsage.from_row(row) for row in rows]

    # Retrieves data from appusage database
    def get_usage(self):
        conn = self.connection()
        cursor = conn.cursor()
        rows = cursor.execute("""SELECT app_name, date, SUM(total_seconds)
                       FROM appusage
                       GROUP BY app_name, date
                       ORDER BY date DESC, SUM(total_seconds) DESC""").fetchall()

        conn.close()
        return [AppUsage.from_row(row) for row in rows]

    # Retrieves data from applimit database
    def get_app_limits(self):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute("SELECT app_name, limit_seconds FROM applimit")
        rows = cursor.fetchall()
        conn.close()
        return [AppLimit.from_row(row) for row in rows]

    # Gets screentime for today only
    def get_screentime_today(self):
        today = date.today().isoformat()

        conn = self.connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT total_seconds FROM dailyusage WHERE date = ?", (today,))
        result = cursor.fetchone()

        conn.close()
        return result[0] if result else 0
