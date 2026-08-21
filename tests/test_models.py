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
        self.assertEqual(len(department.patients),1)

    def test_addstaff(self):
        department = Department("cardiology")
        staff = Staff("hassan mousa", 32, "doctor")
        department.add_staff(staff)
        self.assertEqual(len(department.staff),1)

