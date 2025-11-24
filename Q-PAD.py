# import libraries
import os
import random
from collections import Counter
from datetime import datetime
from tkinter import filedialog

import pandas as pd
from PIL import Image
from customtkinter import (
    CTk, set_appearance_mode, set_default_color_theme, CTkLabel, CTkButton, CTkFrame,
    CTkScrollableFrame, CTkImage, CTkToplevel, CTkEntry, CTkComboBox)


# Homepage
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
            for i in range(50):
                CTkLabel(self, text=f"Item {i + 1}", font=("Arial", 16)).pack(pady=5)

# Database Page
class databasePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        Sidebar(self, controller, "Database", [
            ("Home", lambda: controller.showFrame("homePage")),
            ("Issue Equipment", self.issue_equipment),
            ("Return Equipment", self.return_equipment),
            ("Add Equipment to Database", self.add_equipment),
            ("Remove Equipment from Database", self.remove_equipment)
        ])

        content = CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.top_frame = CTkFrame(content)
        self.top_frame.pack(fill="x", pady=(0, 10))

        self.item_info_frame = CTkFrame(self.top_frame)
        self.item_info_frame.pack(side="left", padx=10, pady=10)

        self.issued_to_frame = CTkFrame(self.top_frame)
        self.issued_to_frame.pack(side="left", padx=10, pady=10)
        CTkLabel(self.issued_to_frame, text="Cadets Issued:", font=("Arial", 16)).pack(anchor="w")

        self.table_frame = CTkScrollableFrame(content)
        self.table_frame.pack(fill="both", expand=True, pady=10)

    def generate_unique_id(self):
        import random
        existing_ids = set(self.controller.equipment_df["ID No."].astype(str))
        while True:
            new_id = f"{random.randint(1000, 9999)}"
            if new_id not in existing_ids:
                return new_id

    def update_item_details(self, item):
        for widget in self.item_info_frame.winfo_children():
            widget.destroy()

        CTkLabel(self.item_info_frame, text=item["Item Name"], font=("Arial", 16)).pack(anchor="w")
        CTkLabel(self.item_info_frame, text=f"ID No.: {item['ID No.']}").pack(anchor="w")
        CTkLabel(self.item_info_frame, text=f"Size: {item['Size']}").pack(anchor="w")
        CTkLabel(self.item_info_frame, text=f"Stock Qty.: {item['Stock QTY']}").pack(anchor="w")
        CTkLabel(self.item_info_frame, text=f"Issued Qty.: {item['Issued QTY']}").pack(anchor="w")
        CTkLabel(self.item_info_frame, text=item["Item Description"]).pack(anchor="w")

        for widget in self.issued_to_frame.winfo_children():
            if isinstance(widget, CTkLabel) and widget.cget("text") != "Cadets Issued:":
                widget.destroy()

        # Show cadets issued this item
        item_id = item["ID No."]
        df = self.controller.cadet_equip_df
        issued_cadets = df[df["ID No."] == item_id]["Cadet IDs"].tolist()

        unique_cadets = []
        seen = set()
        for cadet_id in issued_cadets:
            if cadet_id not in seen:
                unique_cadets.append(cadet_id)
                seen.add(cadet_id)

        cadet_df = self.controller.cadet_df
        for cadet_id in unique_cadets:
            cadet_row = cadet_df[cadet_df["ID No."] == cadet_id]
            if not cadet_row.empty:
                cadet_name = cadet_row.iloc[0]["Cadet Name"]
                CTkLabel(self.issued_to_frame, text=cadet_name).pack(anchor="w")
            else:
                # fallback to show ID if name not found
                CTkLabel(self.issued_to_frame, text=cadet_id).pack(anchor="w")

    def issue_equipment(self):
        top = CTkToplevel(self)
        top.title("Issue Equipment")
        top.geometry("800x800")

        title_label = CTkLabel(top, text="Issue Equipment", font=("Arial", 20))
        title_label.pack(pady=10)

        # Load cadet list
        cadet_names = self.controller.cadet_df["Cadet Name"].astype(str).tolist()
        cadet_ids = self.controller.cadet_df["ID No."].tolist()
        cadet_name_id_map = dict(zip(cadet_names, cadet_ids))

        # Cadet dropdown
        CTkLabel(top, text="Select Cadet:").pack(pady=(10, 0))
        cadet_id_entry = CTkComboBox(top, values=cadet_names)
        cadet_id_entry.pack(pady=(0, 10))

        # Search bar
        search_frame = CTkFrame(top)
        search_frame.pack(pady=5)
        search_entry = CTkEntry(search_frame, placeholder_text="Search by name or ID...")
        search_entry.pack(side="left", padx=(0, 10))
        search_button = CTkButton(search_frame, text="Search")
        search_button.pack(side="left")

        checklist_frame = CTkScrollableFrame(top, width=500, height=400)
        checklist_frame.pack(pady=10)

        # Build UI entries
        equipment_entries = []
        equipment_quantities = {}

        def populate_equipment_list(filter_query=""):
            for (qty_entry, item_id_entry) in equipment_entries:
                equipment_quantities[item_id_entry] = qty_entry.get()

            for widget in checklist_frame.winfo_children():
                widget.destroy()
            equipment_entries.clear()

            for _, row in self.controller.equipment_df.iterrows():
                item_id = str(row["ID No."])
                item_name = str(row["Item Name"])
                item_size = str(row["Size"])

                if filter_query and (filter_query not in item_name.lower() and filter_query not in item_id.lower()):
                    continue

                row_frame = CTkFrame(checklist_frame)
                row_frame.pack(fill="x", pady=2, padx=10)

                label = CTkLabel(row_frame, text=f"{item_name} (Size: {item_size})")
                label.pack(side="left", padx=(0, 10))

                qty_entry = CTkEntry(row_frame, width=50, placeholder_text="0")
                qty_entry.pack(side="left")

                # Restore Qty Values
                if item_id in equipment_quantities:
                    qty_entry.insert(0, equipment_quantities[item_id])

                def on_entry_change(item, entry):
                    equipment_quantities[item] = entry.get()

                qty_entry.bind("<KeyRelease>", lambda e, item=item_id, entry=qty_entry: on_entry_change(item, entry))
                equipment_entries.append((qty_entry, item_id))

        def perform_search():
            query = search_entry.get().lower().strip()
            populate_equipment_list(query)

        search_entry.bind("<KeyRelease>", lambda e: perform_search())
        populate_equipment_list()

        def assign():
            cadet_name = cadet_id_entry.get()
            if not cadet_name:
                print("Cadet name is required.")
                return

            cadet_id = cadet_name_id_map.get(cadet_name)
            if not cadet_id:
                print("Cadet ID not found.")
                return

            df = self.controller.equipment_df
            issued = []

            for item_id, qty_str in equipment_quantities.items():
                try:
                    qty = int(qty_str)
                    if qty <= 0:
                        continue
                except ValueError:
                    continue

                match = df[df["ID No."].astype(str) == str(item_id)]
                if match.empty:
                    print(f"Item ID {item_id} not found.")
                    continue

                stock_qty = int(match["Stock QTY"].values[0])
                if stock_qty < qty:
                    print(f"Not enough stock for Item {item_id}. Available: {stock_qty}, Requested: {qty}")
                    continue

                df.loc[df["ID No."].astype(str) == str(item_id), "Issued QTY"] += qty
                df.loc[df["ID No."].astype(str) == str(item_id), "Stock QTY"] -= qty

                date_issued = datetime.now().strftime("%Y-%m-%d")

                for _ in range(qty):
                    self.controller.cadet_equip_df.loc[len(self.controller.cadet_equip_df)] = {
                        "Cadet IDs": str(cadet_id).strip(),
                        "ID No.": str(item_id).strip(),
                        "Date Issued": date_issued
                    }

                issued.append((item_id, qty))

            self.controller.populate_table(self.controller.equipment_df)
            self.controller.save_dataframe()
            top.destroy()

            if issued:
                print("Issued:", issued)

        assign_button = CTkButton(top, text="Assign Equipment", command=assign)
        assign_button.pack(pady=10)
        assign_button.lift()

    def return_equipment(self):
     print("return equipment")

    def add_equipment(self):
        window = CTkToplevel(self)
        window.title("Add New Equipment")
        window.geometry("400x600")
        window.grab_set()

        new_id = self.generate_unique_id()
        entries = {}
        labels = ["Item Name", "Size", "Stock QTY", "Issued QTY", "Item Description"]
        for label in labels:
            CTkLabel(window, text=label).pack(pady=(10, 0))
            entry = CTkEntry(window)
            entry.pack(pady=(0, 10))
            entries[label] = entry

        CTkLabel(window, text="ID No. (Auto-generated)").pack(pady=(10, 0))
        id_entry = CTkEntry(window)
        id_entry.insert(0, new_id)
        id_entry.configure(state="disabled")
        id_entry.pack(pady=(0, 10))

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
                print("Invalid input.")

        def import_page():
            top = CTkToplevel(self)
            top.title("Mass import...")
            top.geometry("500x600")
            top.grab_set()
            top.resizable(False, False)

            def select_file():
                file = filedialog.askopenfilename(
                    filetypes=[("Excel File", "*.xlsx"), ("CSV File", "*.csv")]
                )
                if file:
                    print("Selected file:", file)
                    if file.endswith(".xlsx"):
                        import_df = pd.DataFrame(pd.read_excel(file))
                        print(import_df.head(10))
                    else:
                        import_df = pd.read_csv(file)

                    if "ID No." in import_df.columns:
                        import_df = import_df.drop(columns=["ID No."])

                    print(import_df)

                    for col in self.controller.equipment_df.columns:
                        if col not in import_df.columns:
                            import_df[col] = ""

                    import_df = import_df[self.controller.equipment_df.columns.drop("ID No.")]
                    import_df["ID No."] = [self.generate_unique_id() for _ in range(len(import_df))]

                    self.controller.equipment_df = pd.concat(
                        [self.controller.equipment_df, import_df],
                        ignore_index=True
                    ).drop_duplicates(subset=["ID No."], ignore_index=True)

                    self.controller.save_dataframe()
                    self.controller.populate_table(self.controller.equipment_df)

                else:
                    print("No selected file.")

            select_button = CTkButton(top, text="Select File", command=select_file)
            select_button.pack(pady=20)
            info_label = CTkLabel(top, text="Drag/drop to be added (it very hard)")
            info_label.pack(pady=20)



        CTkButton(window, text="Add", command=submit).pack(pady=20)
        CTkButton(window, text="Mass Import", command=import_page).pack(pady=20)

    def remove_equipment(self):
        print("Remove Equipment")

# Cadet Equipment Page
class equipmentPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        Sidebar(self, controller, "Cadet Equipment", [
            ("Home", lambda: controller.showFrame("homePage")),
             ("Add Cadet", self.add_Cadet)
        ])

        self.cadet_df = self.controller.cadet_df
        self.equipment_df = self.controller.equipment_df

        self.contentleft = CTkFrame(self, fg_color="transparent")
        self.contentleft.pack(side="left", fill="both", expand=True)

        self.table_frame = CTkScrollableFrame(self.contentleft)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.contentright = CTkFrame(self, fg_color="transparent")
        self.contentright.pack(side="right", fill="both", expand=True)

        self.equipment_display = CTkScrollableFrame(self.contentright)
        self.equipment_display.pack(fill="both", expand=True)

    # refresh the cadet list and clear equipment display
    def refresh(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.display_cadet_list()
        for widget in self.equipment_display.winfo_children():
            widget.destroy()

    def display_cadet_list(self):
        CTkLabel(self.table_frame, text="Cadets:", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)

        for index, row in self.cadet_df.iterrows():
            label = CTkLabel(self.table_frame, text=row["Cadet Name"], cursor="hand2")
            label.pack(pady=2, padx=10, anchor="w")
            cadet_id = row["ID No."]
            label.bind("<Button-1>", lambda e, cid=cadet_id: self.show_cadet_equipment(cid))

    def show_cadet_equipment(self, cadet_id):
        for widget in self.equipment_display.winfo_children():
            widget.destroy()

        assigned_ids = self.controller.cadet_equip_df[
            self.controller.cadet_equip_df["Cadet IDs"] == cadet_id
        ]["ID No."].tolist()

        if not assigned_ids:
            CTkLabel(self.equipment_display, text="No equipment assigned.").pack(anchor="w", padx=10, pady=5)
            return

        CTkLabel(self.equipment_display, text="Assigned Equipment:", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)

        item_counts = Counter(assigned_ids)

        for item_id, count in item_counts.items():
            item = self.controller.equipment_df[self.controller.equipment_df["ID No."].astype(str) == str(item_id)]
            if not item.empty:
                item = item.iloc[0]
                text = f"{item['Item Name']} (ID: {item['ID No.']}) - Size: {item['Size']}"
                if count > 1:
                    text += f" — x{count}"
                CTkLabel(self.equipment_display, text=text).pack(anchor="w", padx=10, pady=2)

    def add_Cadet(self):
        print("Add Cadet clicked")
        try:
            window = CTkToplevel(self)
            window.title("Add New Cadet")
            window.geometry("300x200")
            window.grab_set()

            CTkLabel(window, text="Cadet Name").pack(pady=(10, 0))
            name_entry = CTkEntry(window)
            name_entry.pack(pady=(0, 10))

            def generate_cadet_id():
                existing_ids = set(self.controller.cadet_df["ID No."].astype(str))
                while True:
                    new_id = f"C{random.randint(1000, 9999)}"
                    if new_id not in existing_ids:
                        return new_id

            def submit():
                try:
                    new_row = {
                        "Cadet Name": name_entry.get(),
                        "ID No.": generate_cadet_id()
                    }

                    self.controller.cadet_df.loc[len(self.controller.cadet_df)] = new_row
                    self.controller.save_dataframe()
                    self.controller.populate_cadet_table(self.controller.cadet_df)
                    window.destroy()
                except ValueError:
                    print("Invalid input.")

            CTkButton(window, text="Submit", command=submit).pack(pady=10)
        except Exception as e:
            print(f"Error creating Cadet window: {e}")

# Report Page
class reportPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        Sidebar(self, controller, "Reports", [
            ("Home", lambda: controller.showFrame("homePage"))
        ])

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

        CTkLabel(self, text=title, font=("Arial", 20)).pack(pady=20)

        for label, command in buttons:
            CTkButton(self, text=label, font=("Arial", 16), command=command).pack(pady=10)

        if controller.shared_image:
            CTkLabel(self, image=controller.shared_image, text="").pack(side="bottom", pady=10)


# App Controller
class QPAD(CTk):
    def __init__(self):
        super().__init__()

        self.title("Q-PAD")
        self.geometry("1200x700")

        set_appearance_mode("system")
        set_default_color_theme("blue")

        # Load Logo Image
        try:
            mstr_dir = os.path.dirname(__file__)
            img_path = os.path.join(mstr_dir, "Images", "bcacu.png")

            Logo = Image.open(img_path)
            self.shared_image = CTkImage(light_image=Logo, dark_image=Logo, size=(100, 100))
            Logo.save("logo.ico")
            self.iconbitmap("logo.ico")


        except Exception as e:
            print(f"Error loading logo: {e}")
            self.shared_image = None

        # Set paths to csv files
        eq_path = "equipment_data.csv"
        cadet_path = "cadet_data.csv"
        cadet_equip_path = "cadet_equipment.csv"

        # Validate existence of csvs and generate them if they dont
        self.equipment_df = pd.read_csv(eq_path) if os.path.exists(eq_path) else pd.DataFrame(
            columns=["Item Name", "Size", "ID No.", "Stock QTY", "Issued QTY", "Item Description"])
        self.equipment_df.to_csv(eq_path, index=False)

        self.cadet_df = pd.read_csv(cadet_path) if os.path.exists(cadet_path) else pd.DataFrame(
            columns=["Cadet Name", "ID No."])
        self.cadet_df.to_csv(cadet_path, index=False)

        self.cadet_equip_df = pd.read_csv(cadet_equip_path) if os.path.exists(cadet_equip_path) else pd.DataFrame(
            columns=["ID No.", "Cadet IDs", "Date Issued"])
        self.cadet_equip_df.to_csv(cadet_equip_path, index=False)

        self.container = CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (homePage, databasePage, equipmentPage, reportPage):
            name = F.__name__
            frame = F(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            if name == "databasePage":
                self.database_table_container = frame
            elif name == "equipmentPage":
                self.equipment_table_container = frame

        self.showFrame("homePage")

    def save_dataframe(self):
        self.equipment_df.to_csv("equipment_data.csv", index=False)
        self.cadet_df.to_csv("cadet_data.csv", index=False)
        self.cadet_equip_df.to_csv("cadet_equipment.csv", index=False)

    def populate_table(self, df):
        table_frame = self.database_table_container.table_frame
        for widget in table_frame.winfo_children():
            widget.destroy()

        display_columns = ["Item Name", "Size", "Stock QTY", "Issued QTY", "Item Description"]

        for col, header in enumerate(display_columns):
            CTkLabel(table_frame, text=header, font=("Arial", 14, "bold")).grid(
                row=0, column=col, padx=10, pady=5, sticky="w"
            )

        for row_index, row in df.iterrows():
            for col_index, col in enumerate(display_columns):
                label = CTkLabel(table_frame, text=str(row[col]), font=("Arial", 12))
                label.grid(row=row_index + 1, column=col_index, padx=10, pady=2, sticky="w")
                label.bind("<Button-1>", lambda e, item=row: self.database_table_container.update_item_details(item))

    def populate_cadet_table(self, df):
        table_frame = self.equipment_table_container.table_frame
        for widget in table_frame.winfo_children():
            widget.destroy()

        columns = df.columns.tolist()
        for col_index, col_name in enumerate(columns):
            CTkLabel(table_frame, text=col_name, font=("Arial", 14, "bold")).grid(row=0, column=col_index, padx=10,
                                                                                  pady=5, sticky="w")

        for row_index, (_, row) in enumerate(df.iterrows()):
            for col_index, col_name in enumerate(columns):
                label = CTkLabel(table_frame, text=str(row[col_name]), font=("Arial", 12))
                label.grid(row=row_index + 1, column=col_index, padx=10, pady=2, sticky="w")

    # Function to allow the switching of frames
    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()
        if pageName == "databasePage":
            self.populate_table(self.equipment_df)
        elif pageName == "equipmentPage":
            self.frames["equipmentPage"].refresh()

if __name__ == "__main__":
    app = QPAD()
    app.mainloop()
