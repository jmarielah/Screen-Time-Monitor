<h1 align="center"> Screen Time Monitor </h1>

<p align="center">
  <i>An application developed with Python that helps you track, visualize, and limit your screen time usage.</i>
</p>

---

## Proponent(s)
-> Jeannie Mariel D. Hernandez - BSCS

---

## Project Overview
-> This Screen Time Monitor written in **Python and AppleScript** is designed for macOS users who wish to track and limit their daily screen time usage. It is a system that allows the user to view their screen time via graphs and limit their individual app usage. Moreover, it includes a simple and minimalistic interface styled using **PyQt6, Matplotlib, and QSS (Qt Style Sheet)**, allowing the user to navigate through the app easily. With this, users can become more aware of their computer habits and take action to make them healthier.

---

## Features

- Tracks application usage daily.
- Presents calculated screen time usage.
- Displays usage graphs from matplotlib and different screen time facts.
- App time limit (set by user).
- Automatically exits applications after exceeding time limit.
- Stores data into SQLite3 database.
- Minimalistic and user-frieldny interface.

---

## Code Design and Structure

1. main.py - Main part where the app is launched and the main window is displayed with styles applied.
2. core/ - File where the core modules ofthe app are located
   - db.py - Creates a connection with SQLite database.
3. features/ - File that contains all the application logic and functionalities.
   - models.py - Defines data models used throughout the application's development.
   - repository.py - Where data is logged into and retrieved from the database.
   - service.py - Defines app functionalities.
   - utils.py - Defines functionalities written in AppleScript.
   - view.py - Plots and customizes graphs to be displayed.
4. shell/ - Contains the Graphical User Interface (GUI)
   - windows.py - Contains code defining interaction logic and templates for each window.
   - appusagewindow.qss - Contains the Qt Style Sheet for the application usage window.
   - notes.txt - Text file containing different screen time facts.
5. mainwindow.qss - Contains the Qt Style Sheet for the main window.

---

## Screenshots

### Main Window
<img width="1272" height="858" alt="Screenshot 2025-10-15 at 8 17 09 PM" src="https://github.com/user-attachments/assets/9d7f4931-29de-4640-bafd-32e12064f407" />

### App Usage Window
<img width="993" height="822" alt="Screenshot 2025-10-15 at 8 16 53 PM" src="https://github.com/user-attachments/assets/bed6f380-2bfc-40d4-999f-144cc6219c47" />

### Choose App to Limit
<img width="675" height="470" alt="Screenshot 2025-10-15 at 8 17 53 PM" src="https://github.com/user-attachments/assets/56c08b3d-0ae7-4723-9b2a-e2d1cfa89066" />

### Set App Limit (In hour(s) and seconds (s))
<img width="218" height="149" alt="Screenshot 2025-10-15 at 8 18 06 PM" src="https://github.com/user-attachments/assets/a2a2a170-0693-42ab-8a3f-83a0da38c56e" />
<img width="245" height="148" alt="Screenshot 2025-10-15 at 8 18 21 PM" src="https://github.com/user-attachments/assets/6ad37ece-9b1f-42fc-a4bc-b975fe9ae001" />

### Pop-Up Warning
<img width="966" height="709" alt="Screenshot 2025-10-15 at 8 21 07 PM" src="https://github.com/user-attachments/assets/d5eaa4d5-7940-4c95-badd-3b6b0b8721b6" />

---

## How to Run the Program

1. **Install Python 3.x**
   - Ensure that Python 3.x is installed. It can be downloaded on [Python's official website](https://www.python.org)
2. **Install the necessary packages**
   - Open a new terminal in your code editor and create a virtual environment:
     ```bash
     python -m venv myenv
     ```
   - Activate the virtual environment you just created:
     ```bash
     source myenv/bin/activate
     ```
   - Install the following packages:
     ```bash
     pip install PyQt6
     pip install matplotlib
     ```
3. **Run the Application**
   - Navigate towards the main file (main.py) and click on the "Run Python File" button.
   - Or execute the file using the following command:
     ```bash
     python3 main.py
     ```
