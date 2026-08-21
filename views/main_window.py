import customtkinter
import tkinter.ttk as ttk
from PIL import Image, ImageOps, ImageTk
import os

# --- Custom Colors ---
TEAL_PRIMARY = "#0EA582"
TEAL_HOVER = "#0B8266"
WHITE = "#FFFFFF"
BG_LIGHT = "#F4F7F6"
TEXT_DARK = "#2B2B2B"

# --- Image Helper Function ---
def invert_icon_color(image_path):
    """Inverts the colors of a PNG image while keeping the background transparent."""
    original_image = Image.open(image_path).convert("RGBA")
    r, g, b, alpha = original_image.split()
    
    # Invert only the RGB colors
    rgb_image = Image.merge("RGB", (r, g, b))
    inverted_rgb = ImageOps.invert(rgb_image)
    ir, ig, ib = inverted_rgb.split()
    
    # Merge back with original transparency
    return Image.merge("RGBA", (ir, ig, ib, alpha))


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("MediCare - Hospital Management System")
        self.geometry("1100x700")

        # Set up assets directory path first
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(current_dir, "assets")

        # Set Window Title Bar Icon (Converts PNG to ICO format for Windows Title Bar)
        try:
            logo_path = os.path.join(assets_dir, "logo.png")
            if os.path.exists(logo_path):
                ico_path = os.path.join(assets_dir, "logo.ico")
                # Convert PNG to ICO if ICO does not exist yet
                if not os.path.exists(ico_path):
                    img = Image.open(logo_path)
                    img.save(ico_path, format="ICO", sizes=[(32, 32)])
                
                # Apply .ico to Windows Title Bar
                self.iconbitmap(ico_path)
        except Exception as e:
            print(f"Could not load window icon: {e}")

        customtkinter.set_appearance_mode("Light")
        self.configure(fg_color=BG_LIGHT)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)



        # 1. Logo (Stays the same in both modes)
        logo_path = os.path.join(assets_dir, "logo.png")
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path)
            self.logo_icon = customtkinter.CTkImage(light_image=logo_img, dark_image=logo_img, size=(32, 32))
        else:
            self.logo_icon = None

        # 2. Helper function to load and invert other icons
        def load_dynamic_icon(filename, size=(20, 20)):
            path = os.path.join(assets_dir, filename)
            if not os.path.exists(path):
                return None
            light_img = Image.open(path)               # Black version for Light Mode
            dark_img = invert_icon_color(path)         # White version for Dark Mode
            return customtkinter.CTkImage(light_image=light_img, dark_image=dark_img, size=size)

        # Load dynamic icons
        self.patient_icon = load_dynamic_icon("patient.png")
        self.staff_icon = load_dynamic_icon("staff.png")
        self.dept_icon = load_dynamic_icon("department.png")
        self.dark_mode_icon = load_dynamic_icon("dark_mode.png", size=(24, 24))


        # ==========================================
        # LEFT SIDEBAR
        # ==========================================
        self.sidebar = customtkinter.CTkFrame(self, width=220, corner_radius=0, fg_color=WHITE)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Logo Area (Using frame for precise distance)
        self.logo_frame = customtkinter.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.pack(pady=(30, 20), padx=20, anchor="w")

        self.logo_icon_label = customtkinter.CTkLabel(self.logo_frame, text="", image=self.logo_icon)
        self.logo_icon_label.pack(side="left")

        self.logo_text_label = customtkinter.CTkLabel(
            self.logo_frame, text="MediCare", font=("Arial", 16, "bold"), text_color=TEXT_DARK
        )
        self.logo_text_label.pack(side="left", padx=(12, 0))

        # Departments Section
        self.dept_label = customtkinter.CTkLabel(self.sidebar, text="DEPARTMENTS", font=("Arial", 11, "bold"), text_color="gray50")
        self.dept_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.dept_dropdown = customtkinter.CTkOptionMenu(
            self.sidebar, values=["Cardiology", "Pediatrics"], 
            fg_color=TEAL_PRIMARY, button_color=TEAL_HOVER, button_hover_color=TEAL_HOVER
        )
        self.dept_dropdown.pack(padx=20, pady=5, fill="x")
        
        self.add_dept_btn = customtkinter.CTkButton(
            self.sidebar, text=" Add Dept", image=self.dept_icon, compound="left",
            fg_color="transparent", border_width=1, text_color=TEXT_DARK, 
            border_color="gray70", hover_color="gray90"
        )
        self.add_dept_btn.pack(padx=20, pady=(5, 20), fill="x")

        # Menu Section
        self.menu_label = customtkinter.CTkLabel(self.sidebar, text="MENU", font=("Arial", 11, "bold"), text_color="gray50")
        self.menu_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.btn_patients = customtkinter.CTkButton(
            self.sidebar, text=" Patients", image=self.patient_icon, compound="left", 
            fg_color=TEAL_PRIMARY, text_color=WHITE, hover_color=TEAL_HOVER, anchor="w",
            command=self.show_patients_view
        )
        self.btn_patients.pack(padx=20, pady=5, fill="x")

        self.btn_staff = customtkinter.CTkButton(
            self.sidebar, text=" Staff", image=self.staff_icon, compound="left", 
            fg_color="transparent", text_color=TEXT_DARK, hover_color="gray90", anchor="w",
            command=self.show_staff_view
        )
        self.btn_staff.pack(padx=20, pady=5, fill="x")

        # Dark Mode Toggle Area
        self.theme_frame = customtkinter.CTkFrame(self.sidebar, fg_color="transparent")
        self.theme_frame.pack(side="bottom", pady=30, padx=20, fill="x")
        
        self.theme_icon_label = customtkinter.CTkLabel(self.theme_frame, text="", image=self.dark_mode_icon)
        self.theme_icon_label.pack(side="left", padx=(0, 8))

        self.theme_text = customtkinter.CTkLabel(
            self.theme_frame, text="Dark Mode  ", font=("Arial", 12, "bold"), text_color=TEXT_DARK
        )
        self.theme_text.pack(side="left")

        self.theme_switch = customtkinter.CTkSwitch(
            self.theme_frame, text="", command=self.toggle_theme, 
            progress_color=TEAL_PRIMARY, switch_width=38, switch_height=20
        )
        self.theme_switch.pack(side="right")


        # ==========================================
        # MAIN CONTENT AREA
        # ==========================================
        self.main_content = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # Header
        self.header_frame = customtkinter.CTkFrame(self.main_content, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        self.page_title = customtkinter.CTkLabel(self.header_frame, text="Patients", font=("Arial", 28, "bold"), text_color=TEXT_DARK)
        self.page_title.pack(side="left")

        self.add_record_btn = customtkinter.CTkButton(
            self.header_frame, text="+ Add New Patient", font=("Arial", 14, "bold"), 
            fg_color=TEAL_PRIMARY, hover_color=TEAL_HOVER, height=40
        )
        self.add_record_btn.pack(side="right")

        # Data Card
        self.data_card = customtkinter.CTkFrame(self.main_content, fg_color=WHITE, corner_radius=10)
        self.data_card.pack(fill="both", expand=True)

        self.setup_table()
        self.show_patients_view() # Load patients view on startup

    def setup_table(self):
        """Initializes treeview styles and tag configurations."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=WHITE, foreground=TEXT_DARK, rowheight=45, borderwidth=0, font=("Arial", 11))
        style.configure("Treeview.Heading", background=WHITE, foreground="gray50", font=("Arial", 10, "bold"), borderwidth=0)
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        self.table = ttk.Treeview(self.data_card, show="headings", style="Treeview")
        self.table.pack(fill="both", expand=True, padx=20, pady=20)

        # Configure Status Tags
        self.table.tag_configure("Stable", foreground="#28A745")
        self.table.tag_configure("Observation", foreground="#D97706")
        self.table.tag_configure("Critical", foreground="#DC2626")

    def show_patients_view(self):
        """Displays Patients table view."""
        self.page_title.configure(text="Patients")
        self.add_record_btn.configure(text="+ Add New Patient")

        self.btn_patients.configure(fg_color=TEAL_PRIMARY, text_color=WHITE)
        self.btn_staff.configure(fg_color="transparent", text_color=WHITE if self.theme_switch.get() == 1 else TEXT_DARK)

        for item in self.table.get_children():
            self.table.delete(item)

        columns = ("Name", "ID", "Age", "Record", "Room", "Status")
        self.table.configure(columns=columns)
        
        self.table.heading("Name", text="PATIENT NAME", anchor="w")
        self.table.heading("ID", text="ID", anchor="w")
        self.table.heading("Age", text="AGE", anchor="w")
        self.table.heading("Record", text="MEDICAL RECORD", anchor="w")
        self.table.heading("Room", text="ROOM", anchor="w")
        self.table.heading("Status", text="STATUS", anchor="w")

        self.table.column("Name", width=180)
        self.table.column("ID", width=80)
        self.table.column("Age", width=60)
        self.table.column("Record", width=280)
        self.table.column("Room", width=80)
        self.table.column("Status", width=120)

        self.table.insert("", "end", values=("Eleanor Whitfield", "PT-1042", "67", "Hypertension, Type 2 Diabetes", "3A-12", "● Observation"), tags=("Observation",))
        self.table.insert("", "end", values=("Marcus Lindqvist", "PT-1043", "34", "Post-op recovery, Appendectomy", "2B-04", "● Stable"), tags=("Stable",))
        self.table.insert("", "end", values=("Priya Nair", "PT-1044", "28", "Asthma, Seasonal allergies", "1C-09", "● Stable"), tags=("Stable",))
        self.table.insert("", "end", values=("Hassan Al-Farsi", "PT-1045", "71", "Cardiac arrhythmia, Pacemaker", "ICU-02", "● Critical"), tags=("Critical",))

    def show_staff_view(self):
        """Displays Staff table view."""
        self.page_title.configure(text="Staff")
        self.add_record_btn.configure(text="+ Add New Staff")

        self.btn_staff.configure(fg_color=TEAL_PRIMARY, text_color=WHITE)
        self.btn_patients.configure(fg_color="transparent", text_color=WHITE if self.theme_switch.get() == 1 else TEXT_DARK)

        for item in self.table.get_children():
            self.table.delete(item)

        columns = ("Name", "Age", "Position")
        self.table.configure(columns=columns)
        
        self.table.heading("Name", text="STAFF NAME", anchor="w")
        self.table.heading("Age", text="AGE", anchor="w")
        self.table.heading("Position", text="POSITION", anchor="w")

        self.table.column("Name", width=250)
        self.table.column("Age", width=100)
        self.table.column("Position", width=350)

        self.table.insert("", "end", values=("Dr. Sarah Connor", "42", "Chief Surgeon"))
        self.table.insert("", "end", values=("John Doe", "29", "Registered Nurse"))
        self.table.insert("", "end", values=("Emily Watson", "35", "Cardiologist"))

    def toggle_theme(self):
        style = ttk.Style()
        if self.theme_switch.get() == 1:
            customtkinter.set_appearance_mode("Dark")
            self.configure(fg_color="#121212")
            self.sidebar.configure(fg_color="#1E1E1E")
            self.data_card.configure(fg_color="#1E1E1E")
            
            self.logo_text_label.configure(text_color=WHITE)
            self.add_dept_btn.configure(text_color=WHITE)
            self.page_title.configure(text_color=WHITE)
            self.theme_text.configure(text_color=WHITE)
            
            if self.btn_patients.cget("fg_color") == "transparent":
                self.btn_patients.configure(text_color=WHITE)
            if self.btn_staff.cget("fg_color") == "transparent":
                self.btn_staff.configure(text_color=WHITE)
            
            style.configure("Treeview", background="#1E1E1E", fieldbackground="#1E1E1E", foreground=WHITE)
            style.configure("Treeview.Heading", background="#1E1E1E", foreground="gray70")

        else:
            customtkinter.set_appearance_mode("Light")
            self.configure(fg_color=BG_LIGHT)
            self.sidebar.configure(fg_color=WHITE)
            self.data_card.configure(fg_color=WHITE)
            
            self.logo_text_label.configure(text_color=TEXT_DARK)
            self.add_dept_btn.configure(text_color=TEXT_DARK)
            self.page_title.configure(text_color=TEXT_DARK)
            self.theme_text.configure(text_color=TEXT_DARK)
            
            if self.btn_patients.cget("fg_color") == "transparent":
                self.btn_patients.configure(text_color=TEXT_DARK)
            if self.btn_staff.cget("fg_color") == "transparent":
                self.btn_staff.configure(text_color=TEXT_DARK)
            
            style.configure("Treeview", background=WHITE, fieldbackground=WHITE, foreground=TEXT_DARK)
            style.configure("Treeview.Heading", background=WHITE, foreground="gray50")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()