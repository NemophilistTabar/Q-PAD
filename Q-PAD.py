# import libraries
import random
import os
import pandas as pd
from PIL import Image
from customtkinter import (CTk, set_appearance_mode, set_default_color_theme, CTkLabel, CTkButton, CTkFrame,
                           CTkScrollableFrame, CTkImage, CTkToplevel, CTkEntry)


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

            # dummy widgets
            for i in range(50):
                label = CTkLabel(self, text=f"Item {i + 1}", font=("Arial", 16))
                label.pack(pady=5)

# Database Page
class databasePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Sidebar
        Sidebar(self, controller, "Database", [
            ("Home", lambda: controller.showFrame("homePage")),
            ("Issue Equipment", self.issue_equipment),
            ("Return Equipment", self.return_equipment),
            ("Add Equipment to Database", self.add_equipment),
            ("Remove Equipment from Database", self.remove_equipment)
        ])

        # Main content
        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # === Top Section ===
        top_frame = CTkFrame(content)
        top_frame.pack(fill="x", pady=(0, 10))

        # Left: Image of item
        self.image_label = CTkLabel(top_frame, text="", width=150, height=150, corner_radius=5)
        self.image_label.pack(side="left", padx=10)

        # Center: Item Info
        item_info_frame = CTkFrame(top_frame)
        item_info_frame.pack(side="left", padx=10, pady=10)

        CTkLabel(item_info_frame, text="Bushhat", font=("Arial", 16)).pack(anchor="w")
        CTkLabel(item_info_frame, text="ID No.: 0001").pack(anchor="w")
        CTkLabel(item_info_frame, text="Stock Qty.: 12").pack(anchor="w")
        CTkLabel(item_info_frame, text="Issued Qty.: 5").pack(anchor="w")

        # Right: Cadets Issued
        issued_to_frame = CTkFrame(top_frame)
        issued_to_frame.pack(side="left", padx=10, pady=10)

        CTkLabel(issued_to_frame, text="Cadets Issued:", font=("Arial", 16)).pack(anchor="w")
        for name in ["Larry", "Bill", "Fred", "Jess", "Frank"]:
            CTkLabel(issued_to_frame, text=name).pack(anchor="w")

        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # This is where your equipment table will be shown
        self.table_frame = CTkScrollableFrame(content)
        self.table_frame.pack(fill="both", expand=True, pady=10)

    def issue_equipment(self):
        print("Issue Equipment")

    def return_equipment(self):
        print("Return Equipment")

    def add_equipment(self):
        window = CTkToplevel(self)
        window.title("Add New Equipment")
        window.geometry("400x500")
        window.grab_set()  # Prevent interacting with main window while open

        # Generate unique ID
        def generate_unique_id():
            existing_ids = set(self.controller.equipment_df["ID No."].astype(str))
            while True:
                new_id = f"{random.randint(1000, 9999)}"
                if new_id not in existing_ids:
                    return new_id

        new_id = generate_unique_id()

        # Labels and Entry Fields
        entries = {}

        # Field list (excluding ID for now)
        labels = ["Item Name", "Size", "Stock QTY", "Issued QTY", "Item Description"]
        for label in labels:
            CTkLabel(window, text=label).pack(pady=(10, 0))
            entry = CTkEntry(window)
            entry.pack(pady=(0, 10))
            entries[label] = entry

        # ID field (auto-generated and disabled)
        CTkLabel(window, text="ID No. (Auto-generated)").pack(pady=(10, 0))
        id_entry = CTkEntry(window)
        id_entry.insert(0, new_id)
        id_entry.configure(state="disabled")
        id_entry.pack(pady=(0, 10))

        # Submit Button
        def submit():
            try:
                new_row = {
                    "Item Name": entries["Item Name"].get(),
                    "Size": entries["Size"].get(),
                    "ID No.": new_id,
                    "Stock QTY": int(entries["Stock QTY"].get()),
                    "Issued QTY": int(entries["Issued QTY"].get()),
                    "Item Description": entries["Item Description"].get()
                }

                self.controller.equipment_df.loc[len(self.controller.equipment_df)] = new_row
                self.controller.save_dataframe()
                self.controller.populate_table(self.controller.equipment_df)
                window.destroy()

            except ValueError:
                print("Invalid input: Stock and Issued QTY must be numbers.")

        CTkButton(window, text="Add", command=submit).pack(pady=20)

    def remove_equipment(self):
        print("Remove Equipment")

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

        csv_path = "equipment_data.csv"
        if os.path.exists(csv_path):
            self.equipment_df = pd.read_csv(csv_path)
        else:
            self.equipment_df = pd.DataFrame(columns=[
                "Item Name", "Size", "ID No.", "Stock QTY", "Issued QTY", "Item Description"
            ])
            self.equipment_df.to_csv(csv_path, index=False)

        self.container = CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (homePage, databasePage, equipmentPage, reportPage):
            pageName = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            if pageName == "databasePage":
                self.database_table_container = frame

        self.showFrame("homePage")

    def save_dataframe(self):
        self.equipment_df.to_csv("equipment_data.csv", index=False)

    def populate_table(self, df):
        # Assume databasePage has attribute table_frame (a CTkScrollableFrame)
        table_frame = self.database_table_container.table_frame

        # Clear old widgets
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Headers
        headers = list(df.columns)
        for col, header in enumerate(headers):
            CTkLabel(table_frame, text=header, font=("Arial", 14, "bold")).grid(row=0, column=col, padx=10, pady=5)

        # Rows
        for row_index, row in df.iterrows():
            for col_index, col in enumerate(headers):
                CTkLabel(table_frame, text=str(row[col]), font=("Arial", 12)).grid(row=row_index + 1, column=col_index,
                                                                                   padx=10, pady=2)

    # Frame Switcher
    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

if __name__ == "__main__":
    app = QPAD()
    app.mainloop()