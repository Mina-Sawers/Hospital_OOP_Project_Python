from models.patient import Patient
from models.staff import Staff

class Department:
    """Class representing a department in the hospital, managing patients and staff."""
    
    def __init__(self, name: str):
        self.name = name
        self.patients = [] 
        self.staff = []    

    def add_patient(self, patient: Patient) -> None:
        """Add a patient object to the department."""
        if patient not in self.patients:
            self.patients.append(patient)
            print(f"Patient '{patient.name}' added to {self.name} department.")
        else:
            print(f"Patient '{patient.name}' is already in this department.")

    def add_staff(self, staff_member: Staff) -> None:
        """Add a staff member object to the department."""
        if staff_member not in self.staff:
            self.staff.append(staff_member)
            print(f"Staff member '{staff_member.name}' added to {self.name} department.")
        else:
            print(f"Staff member '{staff_member.name}' is already in this department.")