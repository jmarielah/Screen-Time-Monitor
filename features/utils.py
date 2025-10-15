import subprocess


class Utils:

    # Finds the app being used and returns its name
    def get_active_app(self):
        script = 'tell application "System Events" to get name of first process whose frontmost is true'
        return subprocess.check_output(["osascript", "-e", script], text=True).strip()

    # Lists down all apps on the device and allows the user to choose which app to limit
    @staticmethod
    def choose_app():
        script = '''
        set chosenApp to choose application with prompt "Select an app to limit:"
        set appName to name of chosenApp
        return appName
        '''
        try:
            return subprocess.check_output(["osascript", "-e", script], text=True).strip()
        except subprocess.CalledProcessError:
            return None

    # Shows a warning when an app is a few seconds away from automatically closing
    def show_warning(self, app_name, seconds):
        script = f'display dialog "{app_name} will close in {seconds} seconds!" buttons {{"OK"}} default button "OK" giving up after {seconds}'
        subprocess.run(["osascript", "-e", script])

    # Closes an app
    def close_app(self, app_name):
        script = f'tell application "{app_name}" to quit'
        subprocess.run(["osascript", "-e", script])

    # Converts time limit of hours and minutes into seconds
    @staticmethod
    def convert(hours=0, minutes=0):
        total_seconds = int(hours * 3600 + minutes * 60)
        return total_seconds
