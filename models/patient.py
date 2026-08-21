from models.person import Person


class Patient(Person):
    """Represents a hospital patient and their medical record."""

    def __init__(self, name, age, medical_record):
        super().__init__(name, age)
        self.medical_record = medical_record

    def view_info(self):
        """Display the patient's basic information."""
        print(f"Patient Name: {self.name}")
        print(f"Age: {self.age}")

    def view_record(self):
        """Return the patient's medical record."""
        return self.medical_record

    def update_medical_record(self, new_record):
        """Update the patient's medical record."""
        self.medical_record = new_record

## testing the Patient class

if __name__ == "__main__":
    patient1 = Patient(
        "Ahmed Ali",
        30,
        "Diabetes - Taking insulin"
    )

    patient1.view_info()

    print("Medical Record:", patient1.view_record())

    patient1.update_medical_record(
        "Diabetes - Taking insulin and following a special diet"
    )

    print("Updated Record:", patient1.view_record())