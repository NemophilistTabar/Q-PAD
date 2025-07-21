# import libraries
from customtkinter import CTk, set_appearance_mode, set_default_color_theme, CTkLabel, CTkButton, CTkFrame, CTkScrollableFrame


# HomePage
class homePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = CTkLabel(self, text="Home Page", font=("Arial", 20))
        label.pack(pady=20)

        dataBaseButton = CTkButton(self, text="View Database", font=("Arial", 20),
                            command=lambda: controller.showFrame("databasePage"))
        dataBaseButton.pack(pady=100)
        equipButton = CTkButton(self, text="View Cadet Equipment", font=("Arial", 20),
                            command=lambda: controller.showFrame("equipmentPage"))
        equipButton.pack(pady=100)
        reportButton = CTkButton(self, text="Generate Report", font=("Arial", 20),
                            command=lambda: controller.showFrame("reportPage"))
        reportButton.pack(pady=100)

        self.my_frame = self.MyFrame(self)
        self.my_frame.place(relx=1.0, rely=0.5, anchor="e")
        self.my_frame.pack_propagate(False)

    class MyFrame(CTkScrollableFrame):
        def __init__(self, parent):
            super().__init__(parent)

            # add widgets onto the frame...
            for i in range(20):
                label = CTkLabel(self, text=f"Item {i + 1}")
                label.pack(pady=5)


# Database Page
class databasePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = CTkLabel(self, text="Database", font=("Arial", 20))
        label.pack(pady=20)

        homeButton = CTkButton(self, text="Home", font=("Arial", 20), command=lambda: controller.showFrame("homePage"))
        homeButton.pack(pady=10)

# Cadet Equipment Page
class equipmentPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = CTkLabel(self, text="Cadet Equipment", font=("Arial", 20))
        label.pack(pady=20)

        homeButton = CTkButton(self, text="Home", font=("Arial", 20), command=lambda: controller.showFrame("homePage"))
        homeButton.pack(pady=10)

# Report Page
class reportPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = CTkLabel(self, text="Report", font=("Arial", 20))
        label.pack(pady=20)

        homeButton = CTkButton(self, text="Home", font=("Arial", 20), command=lambda: controller.showFrame("homePage"))
        homeButton.pack(pady=10)

# establish application
class QPAD(CTk):
    def __init__(self):
        super().__init__()
        self.title("Q-PAD")
        self.geometry("1200x700")

        # Set appearance parameters
        set_appearance_mode("system")
        set_default_color_theme("blue")

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