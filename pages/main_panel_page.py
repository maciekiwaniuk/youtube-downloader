import requests
import tkinter as tk
from tkinter import messagebox
from pages.page import Page
from pytube import YouTube
from helper import Helper
from settings import Settings


class MainPanelPage(Page):
    def __init__(self):
        Page.__init__(self)
        self.helper = Helper()
        self.settings = Settings()

        self.show_content()

    def show_content(self):
        title_label = tk.Label(self, text="Podaj link do wideo na YouTube", font=("Arial", 20))
        title_label.place(x=60, y=30)

        self.url_video_input = tk.Entry(self, font=12)
        self.url_video_input.place(width=390, height=30, x=60, y=80)

        self.confirm_button = tk.Button(self, text="Pobierz", font=11, borderwidth=4, relief="groove", command=self.download_video)
        self.confirm_button.place(y=130, x=196, width=125, height=35)

        self.download_status_label = tk.Label(self, text="Trwa pobieranie, może to chwilę potrwać...", fg="green", font=("Arial", 14))

    def download_video(self):
        if not self.check_internet_connection():
            tk.messagebox.showerror(title="Brak połączenia z internetem", message="Sprawdź swoje połączenie z internetem.")
            return

        try:
            video = YouTube(self.url_video_input.get())

            self.download_status_label.place(y=180, x=78)
            self.confirm_button["state"] = "disabled"
            self.update()

            video = self.handle_settings(video)

            video.download(self.settings.directory)

            self.confirm_button["state"] = "normal"
            self.download_status_label.place_forget()
            self.update()

            tk.messagebox.showinfo(title="Pomyślnie pobrano!", message="Wideo zostało pobrane pomyślnie!")
        except:
            tk.messagebox.showerror(title="Wystąpił błąd", message="Coś poszło nie tak... Sprawdź poprawność linka.")

        self.download_status_label.place_forget()

    @staticmethod
    def check_internet_connection():
        url = "https://youtube.com"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
            return True
        except:
            return False

    def handle_settings(self, video):
        video = video.streams

        if self.settings.resolution == "lowest":
            video = video.get_lowest_resolution()
        elif self.settings.resolution == "highest":
            video = video.get_highest_resolution()
        else:
            video = video.filter(
                resolution=self.settings.resolution
            ).first()

        return video

