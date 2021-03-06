import os
import requests
from datetime import datetime


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def get_download_path():
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')

    @staticmethod
    def get_desktop_path():
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    @staticmethod
    def get_appdata_project_folder_path():
        return f"{os.getenv('APPDATA')}/YoutubeDownloader"

    @staticmethod
    def get_settings_file_path():
        return f"{Helper.get_appdata_project_folder_path()}/settings.json"

    @staticmethod
    def get_downloaded_videos_file_path():
        return f"{Helper.get_appdata_project_folder_path()}/downloaded_videos.json"

    @staticmethod
    def check_internet_connection():
        url = "https://youtube.com"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
            return True
        except:
            return False

    @staticmethod
    def get_string_without_polish_characters(string):
        string = string.replace("ą", "a")
        string = string.replace("ć", "c")
        string = string.replace("ę", "e")
        string = string.replace("ł", "l")
        string = string.replace("ń", "n")
        string = string.replace("ó", "o")
        string = string.replace("ś", "s")
        string = string.replace("ź", "z")
        string = string.replace("ż", "z")
        return string

    @staticmethod
    def get_good_units_of_size(string):
        string = string.replace("K", " tys.")
        string = string.replace("M", " mln")
        return string

    @staticmethod
    def get_simple_date_from_datetime(date):
        only_date = str(date).split(" ")[0]
        d = datetime.strptime(only_date, "%Y-%m-%d")
        return d.strftime("%d/%m/%Y")



    @staticmethod
    def get_good_looking_length(length):
        minutes = length // 60
        seconds = length % 60
        if minutes == 0: return f"{seconds}s"

        return f"{minutes}min {seconds}s"
