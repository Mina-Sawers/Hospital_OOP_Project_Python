import tkinter as tk
from tkinter import messagebox
import os

from PIL import Image, ImageTk

from models.department import Department


# =========================
# COLORS
# =========================

GREEN = "#2E7D32"
DARK_GREEN = "#1B5E20"
LIGHT_GREEN = "#E8F5E9"
WHITE = "#FFFFFF"
DARK_TEXT = "#263238"


class AddDepartmentDialog(tk.Toplevel):
    """GUI window for adding a new department."""

    def __init__(self, parent, on_department_added=None):

        super().__init__(parent)

        self.parent = parent

        self.on_department_added = on_department_added

        self.title("Add New Department")

        self.geometry("600x450")

        self.resizable(False, False)

        self.configure(bg=WHITE)

        self.transient(parent)

        self.grab_set()

        self.create_widgets()

    def create_widgets(self):

        # =========================
        # Header
        # =========================

        header_frame = tk.Frame(
            self,
            bg=GREEN,
            height=70
        )

        header_frame.pack(
            fill="x"
        )

        title_label = tk.Label(
            header_frame,
            text="Add New Department",
            font=("Arial", 22, "bold"),
            bg=GREEN,
            fg=WHITE
        )

        title_label.pack(
            pady=18
        )

        # =========================
        # Department Image
        # =========================

        image_frame = tk.Frame(
            self,
            bg=WHITE
        )

        image_frame.pack(
            pady=(20, 5)
        )

        image_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "department.png"
        )

        image = Image.open(image_path)

        image.thumbnail((120, 120))

        self.department_image = ImageTk.PhotoImage(image)

        image_label = tk.Label(
            image_frame,
            image=self.department_image,
            bg=WHITE
        )

        image_label.pack()

        # =========================
        # Form
        # =========================

        form_frame = tk.Frame(
            self,
            bg=LIGHT_GREEN,
            bd=1,
            relief="solid"
        )

        form_frame.pack(
            padx=45,
            pady=15,
            fill="x"
        )

        # =========================
        # Department Name
        # =========================

        tk.Label(
            form_frame,
            text="Department Name:",
            font=("Arial", 11, "bold"),
            bg=LIGHT_GREEN,
            fg=DARK_TEXT
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=20
        )

        self.name_entry = tk.Entry(
            form_frame,
            width=38,
            font=("Arial", 11),
            bg=WHITE,
            fg=DARK_TEXT,
            relief="solid",
            bd=1
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=20,
            pady=20
        )

        # =========================
        # Buttons
        # =========================

        button_frame = tk.Frame(
            self,
            bg=WHITE
        )

        button_frame.pack(
            pady=15
        )

        # Add Department
        add_button = tk.Button(
            button_frame,
            text="Add Department",
            command=self.add_department,
            width=16,
            font=("Arial", 11, "bold"),
            bg=GREEN,
            fg=WHITE,
            activebackground=DARK_GREEN,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        add_button.grid(
            row=0,
            column=0,
            padx=10,
            ipady=5
        )

        # Cancel
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=16,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=GREEN,
            activebackground=LIGHT_GREEN,
            activeforeground=DARK_GREEN,
            relief="solid",
            bd=1,
            cursor="hand2"
        )

        cancel_button.grid(
            row=0,
            column=1,
            padx=10,
            ipady=5
        )

        self.name_entry.focus()

    # =========================
    # ADD DEPARTMENT
    # =========================

    def add_department(self):

        name = self.name_entry.get().strip()

        # =========================
        # Validation
        # =========================

        if not name:

            messagebox.showerror(
                "Invalid Input",
                "Please enter the department name.",
                parent=self
            )

            self.name_entry.focus()

            return

        # =========================
        # Create Department
        # =========================

        department = Department(name)

        # =========================
        # Send to Main Window
        # =========================

        if self.on_department_added:

            self.on_department_added(department)

        # =========================
        # Success
        # =========================

        messagebox.showinfo(
            "Success",
            f"Department added successfully!\n\n"
            f"Department: {department.name}",
            parent=self
        )

        self.destroy()


# =========================
# TEST WINDOW
# =========================

if __name__ == "__main__":

    root = tk.Tk()

    root.title("Hospital OOP - Test")

    root.geometry("300x150")

    root.configure(bg=WHITE)

    AddDepartmentDialog(root)

    root.mainloop()