# import libraries
from customtkinter import (CTk, set_appearance_mode, set_default_color_theme, CTkLabel, CTkButton, CTkFrame,
                           CTkScrollableFrame, CTkImage)
from PIL import Image



# HomePage
class homePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Sidebar
        sidebar = CTkFrame(self, width=200, fg_color="#2e2e2e")
        sidebar.pack(side="left", fill="y")

        label = CTkLabel(sidebar, text="Home Page", font=("Arial", 20)) # Page Title
        label.pack(pady=20)

        dataBaseButton = CTkButton(sidebar, text="View Database", font=("Arial", 16),
                                   command=lambda: controller.showFrame("databasePage"))
        dataBaseButton.pack(pady=20)
        equipButton = CTkButton(sidebar, text="View Cadet Equipment", font=("Arial", 16),
                                command=lambda: controller.showFrame("equipmentPage"))
        equipButton.pack(pady=20)
        reportButton = CTkButton(sidebar, text="Generate Report", font=("Arial", 16),
                                 command=lambda: controller.showFrame("reportPage"))
        reportButton.pack(pady=20)

        logo_label = CTkLabel(sidebar, image=controller.shared_image, text="", anchor="s")
        logo_label.pack(side="bottom", pady=10)

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
        sidebar = CTkFrame(self, width=200, fg_color="#2e2e2e")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        label = CTkLabel(sidebar, text="Database", font=("Arial", 20)) # Page Title
        label.pack(pady=20)

        homeButton = CTkButton(sidebar, text="Home", font=("Arial", 20), command=lambda:
                                                            controller.showFrame("homePage"))
        homeButton.pack(pady=10)

        logo_label = CTkLabel(sidebar, image=controller.shared_image, text="", anchor="s") # Braemar Collage Cadets Logo
        logo_label.pack(side="bottom", pady=10)

        # Main content area
        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True)

# Cadet Equipment Page
class equipmentPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Sidebar
        sidebar = CTkFrame(self, width=200, fg_color="#2e2e2e")
        sidebar.pack(side="left", fill="y")

        label = CTkLabel(sidebar, text="Cadet Equipment", font=("Arial", 20)) # Page Title
        label.pack(pady=20)

        homeButton = CTkButton(sidebar, text="Home", font=("Arial", 20), command=lambda:
                                                            controller.showFrame("homePage"))
        homeButton.pack(pady=10)

        logo_label = CTkLabel(sidebar, image=controller.shared_image, text="", anchor="s") # Braemar Collage Cadets Logo
        logo_label.pack(side="bottom", pady=10)

        # Main content area
        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True)

# Report Page
class reportPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Sidebar
        sidebar = CTkFrame(self, width=200, fg_color="#2e2e2e")
        sidebar.pack(side="left", fill="y")

        label = CTkLabel(sidebar, text="Report", font=("Arial", 20)) # Page Title
        label.pack(pady=20)

        homeButton = CTkButton(sidebar, text="Home", font=("Arial", 20), command=lambda:
                                                            controller.showFrame("homePage"))
        homeButton.pack(pady=10)

        logo_label = CTkLabel(sidebar, image=controller.shared_image, text="", anchor="s") # Braemar Collage Cadets Logo
        logo_label.pack(side="bottom", pady=10)

        # Main content area
        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True)

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
        Logo = Image.open("Images/bcacu.png")
        self.shared_image = CTkImage(light_image=Logo, dark_image=Logo, size=(100, 100))

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