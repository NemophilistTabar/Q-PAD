# import libraries
import customtkinter
from customtkinter import CTk, set_appearance_mode, set_default_color_theme
import PIL
from PIL import Image, ImageTk
import tkinter as tk

# Set appearance parameters
set_appearance_mode("system")
set_default_color_theme("blue")

# establish application
class QPAD(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Q-PAD")
        self.geometry("400x400")

        # app widgets
        self.button = customtkinter.CTkButton(self, command=self.button_click)
        self.button.grid(row=0, column=0, padx=20, pady=10)

    # app methods
    def button_click(self):
        print("button click")

app = QPAD()
app.mainloop()
