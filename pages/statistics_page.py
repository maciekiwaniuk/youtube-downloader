import tkinter as tk
from pages.page import Page


class StatisticsPage(Page):
    def __init__(self):
        Page.__init__(self)
        label = tk.Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)
