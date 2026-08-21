import random
from .person import Person


class Patient(Person):
    """Represents a hospital patient and their medical record."""

    def __init__(self, name: str, age: int, medical_record: str, patient_id: str = None, room: str = "N/A", status: str = "Stable"):
        super().__init__(name, age)
        # Auto-generate a unique Patient ID (e.g., PT-1042) if none is provided
        self.patient_id = patient_id if patient_id else f"PT-{random.randint(1000, 9999)}"
        self.medical_record = medical_record
        self.room = room
        self.status = status  # Expected values: "Stable", "Observation", "Critical"

    def view_info(self) -> str:
        """Return the patient's basic information as a formatted string for the GUI."""
        return (
            f"ID: {self.patient_id} | Name: {self.name} | Age: {self.age} | "
            f"Room: {self.room} | Status: {self.status}"
        )

    def view_record(self) -> str:
        """Return the patient's medical record."""
        return self.medical_record

    def update_medical_record(self, new_record: str) -> None:
        """Update the patient's medical record."""
        self.medical_record = new_record

    def update_status(self, new_status: str) -> None:
        """Update the patient's medical status (e.g., Stable, Observation, Critical)."""
        self.status = new_status

    def assign_room(self, new_room: str) -> None:
        """Assign or update the patient's assigned room."""
        self.room = new_room


# Testing the updated Patient class
if __name__ == "__main__":
    patient1 = Patient(
        name="Ahmed Ali",
        age=30,
        medical_record="Diabetes - Taking insulin",
        room="3A-12",
        status="Observation"
    )

    print(patient1.view_info())
    print("Medical Record:", patient1.view_record())

    patient1.update_medical_record("Diabetes - Taking insulin and following a special diet")
    patient1.update_status("Stable")
    
    print("Updated Info:", patient1.view_info())
    print("Updated Record:", patient1.view_record())