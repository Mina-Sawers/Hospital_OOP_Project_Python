class Hospital:
    """Class representing a hospital containing multiple departments."""
    
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.departments = []

    def add_department(self, department) -> None:
        """Add a department to the hospital if it doesn't already exist."""
        if department not in self.departments:
            self.departments.append(department)
            print(f"Department '{department.name}' has been added to {self.name} hospital.")
        else:
            print(f"Department '{department.name}' already exists in this hospital.")