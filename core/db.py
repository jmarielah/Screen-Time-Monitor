import sqlite3


# Create connection to database
def get_connection():
    return sqlite3.connect("screentime.db")
