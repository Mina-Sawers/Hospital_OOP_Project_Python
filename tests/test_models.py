# tests the units checking each class behavior 
#testing add patient
from models.patient import Patient
from models.staff import Staff
from models.hospital import Hospital
from models.department import Department
import unittest

class TestDepartment(unittest.TestCase):
    def test_addpatient(self):
        department = Department("cardiology")
        patient = Patient("ahmad mousa", 30, "heart condition")
        department.add_patient(patient)
        self.assertEqual(len(Department.patients),1)

