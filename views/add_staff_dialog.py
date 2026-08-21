import tkinter as tk
from tkinter import messagebox
import os

from PIL import Image, ImageTk

from models.staff import Staff


# =========================
# COLORS
# =========================

GREEN = "#2E7D32"
DARK_GREEN = "#1B5E20"
LIGHT_GREEN = "#E8F5E9"
WHITE = "#FFFFFF"
DARK_TEXT = "#263238"


class AddStaffDialog(tk.Toplevel):
    """GUI window for adding a new staff member."""

    def __init__(self, parent, on_staff_added=None):

        super().__init__(parent)

        self.parent = parent

        self.on_staff_added = on_staff_added

        self.title("Add New Staff")

        self.geometry("600x550")

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
            text="Add New Staff",
            font=("Arial", 22, "bold"),
            bg=GREEN,
            fg=WHITE
        )

        title_label.pack(
            pady=18
        )

        # =========================
        # Staff Image
        # =========================

        image_frame = tk.Frame(
            self,
            bg=WHITE
        )

        image_frame.pack(
            pady=(15, 5)
        )

        image_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "staff.png"
        )

        image = Image.open(image_path)

        image.thumbnail((120, 120))

        self.staff_image = ImageTk.PhotoImage(image)

        image_label = tk.Label(
            image_frame,
            image=self.staff_image,
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
            pady=10,
            fill="x"
        )

        # =========================
        # Name
        # =========================

        tk.Label(
            form_frame,
            text="Staff Name:",
            font=("Arial", 11, "bold"),
            bg=LIGHT_GREEN,
            fg=DARK_TEXT
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 10)
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
            pady=(18, 10)
        )

        # =========================
        # Age
        # =========================

        tk.Label(
            form_frame,
            text="Age:",
            font=("Arial", 11, "bold"),
            bg=LIGHT_GREEN,
            fg=DARK_TEXT
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=10
        )

        self.age_entry = tk.Entry(
            form_frame,
            width=38,
            font=("Arial", 11),
            bg=WHITE,
            fg=DARK_TEXT,
            relief="solid",
            bd=1
        )

        self.age_entry.grid(
            row=1,
            column=1,
            padx=20,
            pady=10
        )

        # =========================
        # Position
        # =========================

        tk.Label(
            form_frame,
            text="Position:",
            font=("Arial", 11, "bold"),
            bg=LIGHT_GREEN,
            fg=DARK_TEXT
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(10, 18)
        )

        self.position_entry = tk.Entry(
            form_frame,
            width=38,
            font=("Arial", 11),
            bg=WHITE,
            fg=DARK_TEXT,
            relief="solid",
            bd=1
        )

        self.position_entry.grid(
            row=2,
            column=1,
            padx=20,
            pady=(10, 18)
        )

        # =========================
        # Buttons
        # =========================

        button_frame = tk.Frame(
            self,
            bg=WHITE
        )

        button_frame.pack(
            pady=18
        )

        # Add Staff
        add_button = tk.Button(
            button_frame,
            text="Add Staff",
            command=self.add_staff,
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
    # ADD STAFF
    # =========================

    def add_staff(self):

        name = self.name_entry.get().strip()

        age_text = self.age_entry.get().strip()

        position = self.position_entry.get().strip()

        # =========================
        # Validation
        # =========================

        if not name:

            messagebox.showerror(
                "Invalid Input",
                "Please enter the staff member's name.",
                parent=self
            )

            self.name_entry.focus()

            return

        if not age_text:

            messagebox.showerror(
                "Invalid Input",
                "Please enter the staff member's age.",
                parent=self
            )

            self.age_entry.focus()

            return

        try:

            age = int(age_text)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Age must be a number.",
                parent=self
            )

            self.age_entry.focus()

            return

        if age <= 0:

            messagebox.showerror(
                "Invalid Input",
                "Age must be greater than 0.",
                parent=self
            )

            self.age_entry.focus()

            return

        if not position:

            messagebox.showerror(
                "Invalid Input",
                "Please enter the staff position.",
                parent=self
            )

            self.position_entry.focus()

            return

        # =========================
        # Create Staff
        # =========================

        staff = Staff(
            name=name,
            age=age,
            position=position
        )

        # =========================
        # Send to Main Window
        # =========================

        if self.on_staff_added:

            self.on_staff_added(staff)

        # =========================
        # Success
        # =========================

        messagebox.showinfo(
            "Success",
            f"Staff member added successfully!\n\n"
            f"Name: {staff.name}\n"
            f"Age: {staff.age}\n"
            f"Position: {staff.position}",
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

    AddStaffDialog(root)

    root.mainloop()