# import libraries
import customtkinter
from customtkinter import CTk, set_appearance_mode, set_default_color_theme, CTkLabel, CTkButton, CTkFrame
import PIL
from PIL import Image, ImageTk
import tkinter as tk

# Set appearance parameters
set_appearance_mode("system")
set_default_color_theme("blue")

# HomePage
class homePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = CTkLabel(self, text="Home Page", font=("Arial", 20))
        label.pack(pady=20)

        CTkButton(self, text="View Database", font=("Arial", 20),
                  command=lambda: controller.showFrame("databasePage")).pack(pady=100)
        CTkButton(self, text="View Cadet Equipment", font=("Arial", 20),
                  command=lambda: controller.showFrame("equipmentPage")).pack(pady=100)
        CTkButton(self, text="Generate Report", font=("Arial", 20),
                  command=lambda: controller.showFrame("reportPage")).pack(pady=100)

# Database Page
class databasePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = CTkLabel(self, text="Database", font=("Arial", 20))
        label.pack(pady=20)

        CTKButton = CTkButton(self, text="Home", font=("Arial", 20),
                              command=lambda: controller.showFrame("homePage")).pack(pady=10)

# Cadet Equipment Page
class equipmentPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = CTkLabel(self, text="Cadet Equipment", font=("Arial", 20))
        label.pack(pady=20)

        CTKButton = CTkButton(self, text="Home", font=("Arial", 20),
                              command=lambda: controller.showFrame("homePage")).pack(pady=10)

# Report Page
class reportPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = CTkLabel(self, text="Report", font=("Arial", 20))
        label.pack(pady=20)

        CTKButton = CTkButton(self, text="Home", font=("Arial", 20),
                              command=lambda: controller.showFrame("homePage")).pack(pady=10)

# establish application
class QPAD(CTk):
    def __init__(self):
        super().__init__()
        self.title("Q-PAD")
        self.geometry("1200x700")

        self.container = CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (homePage, databasePage, equipmentPage, reportPage):
            pageName = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("homePage")

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

if __name__ == "__main__":
    app = QPAD()
    app.mainloop()