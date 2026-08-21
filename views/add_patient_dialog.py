import tkinter as tk
from tkinter import ttk, messagebox
import os

from PIL import Image, ImageTk

from models.patient import Patient


# =========================
# COLORS
# =========================

GREEN = "#2E7D32"
DARK_GREEN = "#1B5E20"
LIGHT_GREEN = "#E8F5E9"
WHITE = "#FFFFFF"
DARK_TEXT = "#263238"
BORDER_GREEN = "#66BB6A"


class AddPatientDialog(tk.Toplevel):
    """GUI window for adding a new patient."""

    def __init__(self, parent, on_patient_added=None):
        super().__init__(parent)

        self.parent = parent
        self.on_patient_added = on_patient_added

        self.title("Add New Patient")
        self.geometry("600x720")
        self.resizable(False, False)

        # Window background
        self.configure(bg=WHITE)

        # Keep window above main window
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
            text="Add New Patient",
            font=("Arial", 22, "bold"),
            bg=GREEN,
            fg=WHITE
        )
        title_label.pack(
            pady=18
        )

        # =========================
        # Patient Image
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
            "patient.png"
        )

        image = Image.open(image_path)

        # Resize while keeping aspect ratio
        image.thumbnail((120, 120))

        self.patient_image = ImageTk.PhotoImage(image)

        image_label = tk.Label(
            image_frame,
            image=self.patient_image,
            bg=WHITE
        )
        image_label.pack()

        # =========================
        # Form Container
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
        # Patient Name
        # =========================

        tk.Label(
            form_frame,
            text="Patient Name:",
            font=("Arial", 11, "bold"),
            bg=LIGHT_GREEN,
            fg=DARK_TEXT
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 8)
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
            pady=(18, 8)
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
            pady=8
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
            pady=8
        )

        # =========================
        # Medical Record
        # =========================

        tk.Label(
            form_frame,
            text="Medical Record:",
            font=("Arial", 11, "bold"),
            bg=LIGHT_GREEN,
            fg=DARK_TEXT
        ).grid(
            row=2,
            column=0,
            sticky="nw",
            padx=20,
            pady=8
        )

        self.medical_record_text = tk.Text(
            form_frame,
            width=38,
            height=4,
            font=("Arial", 11),
            bg=WHITE,
            fg=DARK_TEXT,
            relief="solid",
            bd=1
        )

        self.medical_record_text.grid(
            row=2,
            column=1,
            padx=20,
            pady=8
        )

        # =========================
        # Room
        # =========================

        tk.Label(
            form_frame,
            text="Room:",
            font=("Arial", 11, "bold"),
            bg=LIGHT_GREEN,
            fg=DARK_TEXT
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=8
        )

        self.room_entry = tk.Entry(
            form_frame,
            width=38,
            font=("Arial", 11),
            bg=WHITE,
            fg=DARK_TEXT,
            relief="solid",
            bd=1
        )

        self.room_entry.grid(
            row=3,
            column=1,
            padx=20,
            pady=8
        )

        # =========================
        # Status
        # =========================

        tk.Label(
            form_frame,
            text="Status:",
            font=("Arial", 11, "bold"),
            bg=LIGHT_GREEN,
            fg=DARK_TEXT
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=20,
            pady=(8, 18)
        )

        self.status_combobox = ttk.Combobox(
            form_frame,
            values=[
                "Stable",
                "Observation",
                "Critical"
            ],
            state="readonly",
            width=36,
            font=("Arial", 11)
        )

        self.status_combobox.grid(
            row=4,
            column=1,
            padx=20,
            pady=(8, 18)
        )

        self.status_combobox.set("Stable")

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

        # Add Patient Button
        self.add_button = tk.Button(
            button_frame,
            text="Add Patient",
            command=self.add_patient,
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

        self.add_button.grid(
            row=0,
            column=0,
            padx=10,
            ipady=5
        )

        # Cancel Button
        self.cancel_button = tk.Button(
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

        self.cancel_button.grid(
            row=0,
            column=1,
            padx=10,
            ipady=5
        )

        # Put cursor in first field
        self.name_entry.focus()

    # =========================
    # ADD PATIENT
    # =========================

    def add_patient(self):

        name = self.name_entry.get().strip()

        age_text = self.age_entry.get().strip()

        medical_record = self.medical_record_text.get(
            "1.0",
            tk.END
        ).strip()

        room = self.room_entry.get().strip()

        status = self.status_combobox.get()

        # =========================
        # Validation
        # =========================

        if not name:

            messagebox.showerror(
                "Invalid Input",
                "Please enter the patient's name.",
                parent=self
            )

            self.name_entry.focus()

            return

        if not age_text:

            messagebox.showerror(
                "Invalid Input",
                "Please enter the patient's age.",
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

        if not medical_record:

            messagebox.showerror(
                "Invalid Input",
                "Please enter the medical record.",
                parent=self
            )

            self.medical_record_text.focus()

            return

        if not room:
            room = "N/A"

        if not status:
            status = "Stable"

        # =========================
        # Create Patient Object
        # =========================

        patient = Patient(
            name=name,
            age=age,
            medical_record=medical_record,
            room=room,
            status=status
        )

        # =========================
        # Send Patient to Main Window
        # =========================

        if self.on_patient_added:

            self.on_patient_added(patient)

        # =========================
        # Success Message
        # =========================

        messagebox.showinfo(
            "Success",
            f"Patient added successfully!\n\n"
            f"Patient ID: {patient.patient_id}\n"
            f"Name: {patient.name}",
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

    AddPatientDialog(root)

    root.mainloop()