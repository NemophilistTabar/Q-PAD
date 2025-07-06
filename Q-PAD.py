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
        self.geometry("1200x700")

        # configure grid layout
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(15):
            self.grid_rowconfigure(i, weight=1)

        # frame configeration
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=3, column=1, rowspan=3, padx=20, pady=10)

        # images repository
        image = Image.open("Images/bcacu.png")
        resized_image = image.resize((200, 200))
        self.logo = ImageTk.PhotoImage(resized_image)

        # app buttons
        button_width = 500
        button_height = 100

        self.databasebutton = customtkinter.CTkButton(
            self.button_frame,
            command=self.button_click,
            text="View Database",
            width=button_width,
            height=button_height)
        self.databasebutton.pack(pady=20)

        self.individualbutton = customtkinter.CTkButton(
            self.button_frame,
            command=self.button_click,
            text="View Cadet Equipment",
            width=button_width,
            height=button_height)
        self.individualbutton.pack(pady=20)

        self.reportbutton = customtkinter.CTkButton(
            self.button_frame,
            command=self.button_click,
            text="Generate Report",
            width=button_width,
            height=button_height)
        self.reportbutton.pack(pady=20)

        # app labels
        self.bcacu = customtkinter.CTkLabel(self, image=self.logo, text="")
        self.bcacu.grid(row=14, column=1, padx=20, pady=10)

        self.titlelabel = customtkinter.CTkLabel(self, text="Welcome to Q-PAD", font=("Arial", 24, "bold"))
        self.titlelabel.grid(row=0, column=1, pady=20)

    # app functions
    def button_click(self):
        print("button click")

app = QPAD()
app.mainloop()
