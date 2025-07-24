# import libraries
import pandas as pd
from PIL import Image
from customtkinter import (CTk, set_appearance_mode, set_default_color_theme, CTkLabel, CTkButton, CTkFrame,
                           CTkScrollableFrame, CTkImage)


# HomePage
class homePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Sidebar
        Sidebar(self, controller, "Q-PAD", [
            ("View Database", lambda: controller.showFrame("databasePage")),
            ("View Cadet Equipment", lambda: controller.showFrame("equipmentPage")),
            ("Generate Report", lambda: controller.showFrame("reportPage"))
        ])

        # Main content area
        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True)

        self.my_frame = self.notifFrame(content)
        self.my_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.my_frame.pack_propagate(False)

    class notifFrame(CTkScrollableFrame):
        def __init__(self, parent):
            super().__init__(parent, width=800, height=600)

            # Add dummy widgets
            for i in range(50):
                label = CTkLabel(self, text=f"Item {i + 1}", font=("Arial", 16))
                label.pack(pady=5)



# Database Page
class databasePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Sidebar
        Sidebar(self, controller, "Database", [
            ("Home", lambda: controller.showFrame("homePage"))
        ])

        # Main content area
        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True)

# Cadet Equipment Page
class equipmentPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Sidebar
        Sidebar(self, controller, "Cadet Equipment", [
            ("Home", lambda: controller.showFrame("homePage"))
        ])

        # Main content area
        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True)

# Report Page
class reportPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Sidebar
        Sidebar(self, controller, "Database", [
            ("Home", lambda: controller.showFrame("homePage"))
        ])

        # Main content area
        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True)

# Sidebar
class Sidebar(CTkFrame):
    def __init__(self, parent, controller, title, buttons=None):
        super().__init__(parent, width=200, fg_color="#2e2e2e")
        self.pack(side="left", fill="y")
        self.pack_propagate(False)

        if buttons is None:
            buttons = []

        # Page title
        CTkLabel(self, text=title, font=("Arial", 20)).pack(pady=20)

        # Add each button
        for label, command in buttons:
            CTkButton(self, text=label, font=("Arial", 16), command=command).pack(pady=10)

        # Logo image
        if controller.shared_image:
            CTkLabel(self, image=controller.shared_image, text="").pack(side="bottom", pady=10)

# establish application
class QPAD(CTk):
    def __init__(self):
        super().__init__()
        self.title("Q-PAD")
        self.geometry("1200x700")

        # Set appearance parameters
        set_appearance_mode("system")
        set_default_color_theme("blue")

        # Load logo image
        try:
            Logo = Image.open("Images/bcacu.png")
            self.shared_image = CTkImage(light_image=Logo, dark_image=Logo, size=(100, 100))
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.shared_image = None

        self.container = CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (homePage, databasePage, equipmentPage, reportPage):
            pageName = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("homePage")

    # Frame Switcher
    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

if __name__ == "__main__":
    app = QPAD()
    app.mainloop()