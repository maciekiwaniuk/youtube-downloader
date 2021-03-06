import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from pages.page import Page
from pytube import YouTube
from helper import Helper


class MainPanelPage(Page):
    def __init__(self, settings_file, downloaded_videos_file):
        Page.__init__(self)
        self.helper = Helper()
        self.settings = settings_file
        self.downloaded_videos = downloaded_videos_file

        self.show_content()

    def show(self):
        self.lift()
        self.show_content()

    def show_content(self):
        self.show_download_content()
        self.show_selected_options()
        self.show_last_downloaded_info()

    def show_download_content(self):
        title_label = tk.Label(self, text="Podaj link do wideo na YouTube", font=("Arial", 20))
        title_label.place(x=60, y=10)

        self.url_video_input = tk.Entry(self, font=12)
        self.url_video_input.place(width=390, height=30, x=60, y=50)

        self.confirm_button = tk.Button(self, text="Pobierz", font=11, borderwidth=4, relief="groove",
                                        command=self.download_video)
        self.confirm_button.place(x=196, y=95, width=125, height=35)

        self.download_status_label = tk.Label(self, text="Trwa pobieranie, może to chwilę potrwać...", fg="green",
                                              font=("Arial", 14))

    def show_selected_options(self):
        labelframe_selected_options_widget = tk.LabelFrame(self, text="Wybrane ustawienia", font=("Arial", 14), width=225, height=169)
        labelframe_selected_options_widget.place(x=25, y=185)

        if self.settings.type == "video": type = "Dźwięk oraz wideo"
        elif self.settings.type == "audio": type = "Tylko dźwięk"
        label_selected_type = tk.Label(labelframe_selected_options_widget, text=f"Typ: {type}", font=("Arial", 13))
        label_selected_type.place(x=3, y=12)

        if self.settings.resolution == "lowest": resolution = "Najniższa"
        elif self.settings.resolution == "360p": resolution = "360p"
        elif self.settings.resolution == "720p": resolution = "720p"
        elif self.settings.resolution == "highest": resolution = "Najwyższa"
        label_selected_resolution = tk.Label(labelframe_selected_options_widget, text=f"Rozdzielczość: {resolution}", font=("Arial", 13))
        label_selected_resolution.place(x=3, y=40)

        if self.settings.extension == "mp4": extension = "MP4"
        elif self.settings.extension == "webm": extension = "WEBM"
        label_selected_extension = tk.Label(labelframe_selected_options_widget, text=f"Rozszerzenie: {extension}", font=("Arial", 13))
        label_selected_extension.place(x=3, y=68)

        if self.settings.directory == "desktop": directory = "Pulpit"
        elif self.settings.directory == "downloads": directory = "Folder pobrane"
        elif self.settings.directory == "custom": directory = "Własny folder"
        label_selected_directory = tk.Label(labelframe_selected_options_widget, text=f"Ścieżka: {directory}", font=("Arial", 13))
        label_selected_directory.place(x=3, y=96)

    def show_last_downloaded_info(self):
        labelframe_last_downloaded_info_widget = tk.LabelFrame(self, text="Ostatnie pobranie", font=("Arial", 14), width=225, height=169)
        labelframe_last_downloaded_info_widget.place(x=265, y=185)

        try:
            test_key = list(self.downloaded_videos.get_downloaded_videos().keys())[-1]
        except:
            return

        key_of_last_downloaded_video = list(self.downloaded_videos.get_downloaded_videos().keys())[-1]
        last_downloaded_video_info_dict = self.downloaded_videos.get_downloaded_videos()[key_of_last_downloaded_video]

        label_title = tk.Label(labelframe_last_downloaded_info_widget, text=f"Tytuł: {last_downloaded_video_info_dict['title'][:20]}", font=("Arial", 13))
        label_title.place(x=3, y=5)

        label_views = tk.Label(labelframe_last_downloaded_info_widget, text=f"Wyświetlenia: {last_downloaded_video_info_dict['views']}", font=("Arial", 13))
        label_views.place(x=3, y=29)

        label_likes = tk.Label(labelframe_last_downloaded_info_widget, text=f"Łapek w górę: {last_downloaded_video_info_dict['likes']}", font=("Arial", 13))
        label_likes.place(x=3, y=51)

        label_length = tk.Label(labelframe_last_downloaded_info_widget, text=f"Długość: {last_downloaded_video_info_dict['length']}", font=("Arial", 13))
        label_length.place(x=3, y=73)

        label_publish_date = tk.Label(labelframe_last_downloaded_info_widget, text=f"Data publikacji: {last_downloaded_video_info_dict['publish_date']}", font=("Arial", 13))
        label_publish_date.place(x=3, y=95)

        label_download_date = tk.Label(labelframe_last_downloaded_info_widget, text=f"Data pobrania: {last_downloaded_video_info_dict['download_date'][:10]}", font=("Arial", 13))
        label_download_date.place(x=3, y=117)

    def download_video(self):
        url_to_video = self.url_video_input.get()
        if len(url_to_video) < 12:
            return

        if not self.helper.check_internet_connection():
            tk.messagebox.showerror(title="Brak połączenia z internetem", message="Sprawdź swoje połączenie z internetem.")
            return

        try:
            video = YouTube(url_to_video)

            self.download_status_label.place(x=78, y=143)
            self.confirm_button["state"] = "disabled"
            self.update()

            # handle selected settings
            video = self.handle_settings(video)

            if self.settings.directory == "desktop": directory = self.helper.get_desktop_path()
            elif self.settings.directory == "downloads": directory = self.helper.get_download_path()
            elif self.settings.directory == "custom": directory = self.settings.custom_directory_path
            else: directory = self.helper.get_desktop_path()

            # download video
            video.download(directory)

            self.confirm_button["state"] = "normal"
            self.download_status_label.place_forget()
            self.update()

            # save info about downloaded video
            self.save_downloaded_video_info_into_file(url_to_video)
            self.show()
            self.update()

            tk.messagebox.showinfo(title="Pomyślnie pobrano!", message="Wideo zostało pobrane pomyślnie!")
        except Exception as e:
            print(e)
            tk.messagebox.showerror(title="Wystąpił błąd", message="Coś poszło nie tak... Sprawdź poprawność linka.")

    def handle_settings(self, video):
        video = video.streams

        # selected type is audio
        if self.settings.type == "audio":
            return video.filter(
                file_extension=self.settings.extension,
                type="audio"
            ).first()

        # selected type is video
        if self.settings.resolution == "lowest":
            video = video.filter(progressive=True, file_extension=self.settings.extension).order_by("resolution").asc().first()
        elif self.settings.resolution == "highest":
            video = video.filter(progressive=True, file_extension=self.settings.extension).order_by("resolution").desc().first()
        else:
            # check if selected video resolution is higher than available in video
            test_resolution_video = video.filter(progressive=True, file_extension=self.settings.extension).order_by("resolution").desc().first()
            if test_resolution_video.resolution < self.settings.resolution:
                return test_resolution_video

            video = video.filter(
                progressive=True,
                res=self.settings.resolution,
                file_extension=self.settings.extension
            ).first()

        return video

    def save_downloaded_video_info_into_file(self, url_to_video):
        video = YouTube(url_to_video)

        current_datetime_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        likes_amount = video.initial_data['contents'] \
            ['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer'] \
            ['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['simpleText']

        downloaded_video_info = {
            "title": self.helper.get_string_without_polish_characters(video.title),
            "views": video.views,
            "length": self.helper.get_good_looking_length(video.length),
            "publish_date": self.helper.get_simple_date_from_datetime(video.publish_date),
            "likes": self.helper.get_good_units_of_size(likes_amount),
            "download_date": current_datetime_string
        }
        self.downloaded_videos.save_new_downloaded_video_info(downloaded_video_info)
