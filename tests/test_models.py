# tests the units checking each class behavior 

from models.patient import Patient
from models.staff import Staff
from models.hospital import Hospital
from models.department import Department
from models.person import Person
import unittest

class TestDepartment(unittest.TestCase):
    def test_addpatient(self):
        department = Department("cardiology")
        patient = Patient("ahmad mousa", 30, "heart condition")
        department.add_patient(patient)
        self.assertEqual(len(department.patients), 1)

    def test_addstaff(self):
        department = Department("cardiology")
        staff = Staff("hassan mousa", 32, "doctor")
        department.add_staff(staff)
        self.assertEqual(len(department.staff), 1)

    def test_addpatient_stores_the_correct_object(self):
        department = Department("cardiology")
        patient = Patient("ahmad mousa", 30, "heart condition")
        department.add_patient(patient)
        self.assertIn(patient, department.patients)

    def test_addstaff_stores_the_correct_object(self):
        department = Department("cardiology")
        staff = Staff("hassan mousa", 32, "doctor")
        department.add_staff(staff)
        self.assertIn(staff, department.staff)

    def test_adding_the_same_patient_twice_does_not_duplicate(self):
        # department.add_patient() checks "if patient not in self.patients"
        # before appending, so adding the same object twice should not grow
        # the list a second time.
        department = Department("cardiology")
        patient = Patient("ahmad mousa", 30, "heart condition")
        department.add_patient(patient)
        department.add_patient(patient)
        self.assertEqual(len(department.patients), 1)

    def test_adding_the_same_staff_twice_does_not_duplicate(self):
        department = Department("cardiology")
        staff = Staff("hassan mousa", 32, "doctor")
        department.add_staff(staff)
        department.add_staff(staff)
        self.assertEqual(len(department.staff), 1)

    def test_department_starts_empty(self):
        department = Department("cardiology")
        self.assertEqual(department.patients, [])
        self.assertEqual(department.staff, [])


class TestPerson(unittest.TestCase):
    def test_person_cannot_be_instantiated_directly(self):
        # Person is an ABC with an abstract view_info(), so it should not be
        # possible to create a bare Person() instance.
        with self.assertRaises(TypeError):
            Person("Jamie Lee", 29)


class TestPatient(unittest.TestCase):
    def setUp(self):
        self.patient = Patient(
            "Alice Johnson", 34, "No known allergies",
            patient_id="PT-1001", room="2A-05", status="Stable",
        )

    def test_patient_is_a_person(self):
        self.assertIsInstance(self.patient, Person)

    def test_view_info_includes_id_room_and_status(self):
        info = self.patient.view_info()
        self.assertIn("PT-1001", info)
        self.assertIn("Alice Johnson", info)
        self.assertIn("34", info)
        self.assertIn("2A-05", info)
        self.assertIn("Stable", info)

    def test_view_record_returns_medical_record(self):
        self.assertEqual(self.patient.view_record(), "No known allergies")

    def test_patient_id_is_auto_generated_when_not_given(self):
        auto_patient = Patient("Tommy Lee", 7, "Asthma, seasonal")
        self.assertTrue(auto_patient.patient_id.startswith("PT-"))

    def test_patient_id_is_kept_when_given(self):
        self.assertEqual(self.patient.patient_id, "PT-1001")

    def test_update_medical_record(self):
        self.patient.update_medical_record("Penicillin allergy noted")
        self.assertEqual(self.patient.view_record(), "Penicillin allergy noted")

    def test_update_status(self):
        self.patient.update_status("Critical")
        self.assertEqual(self.patient.status, "Critical")
        self.assertIn("Critical", self.patient.view_info())

    def test_assign_room(self):
        self.patient.assign_room("4C-10")
        self.assertEqual(self.patient.room, "4C-10")
        self.assertIn("4C-10", self.patient.view_info())

    def test_default_room_and_status(self):
        default_patient = Patient("Tommy Lee", 7, "Asthma, seasonal")
        self.assertEqual(default_patient.room, "N/A")
        self.assertEqual(default_patient.status, "Stable")


class TestStaff(unittest.TestCase):
    def setUp(self):
        self.staff_member = Staff("Dr. Sarah Smith", 45, "Cardiologist")

    def test_staff_is_a_person(self):
        self.assertIsInstance(self.staff_member, Person)

    def test_view_info_returns_expected_string(self):
        self.assertEqual(
            self.staff_member.view_info(),
            "Name: Dr. Sarah Smith, Age: 45, Position: Cardiologist",
        )


class TestHospital(unittest.TestCase):
    def setUp(self):
        self.hospital = Hospital("City General Hospital", "123 Main St")
        self.department = Department("Cardiology")

    def test_hospital_starts_with_no_departments(self):
        self.assertEqual(self.hospital.departments, [])

    def test_add_department_increases_department_list_size(self):
        self.hospital.add_department(self.department)
        self.assertEqual(len(self.hospital.departments), 1)

    def test_add_department_stores_the_correct_object(self):
        self.hospital.add_department(self.department)
        self.assertIn(self.department, self.hospital.departments)

    def test_adding_the_same_department_twice_does_not_duplicate(self):
        self.hospital.add_department(self.department)
        self.hospital.add_department(self.department)
        self.assertEqual(len(self.hospital.departments), 1)

    def test_hospital_attributes_are_stored(self):
        self.assertEqual(self.hospital.name, "City General Hospital")
        self.assertEqual(self.hospital.location, "123 Main St")


if __name__ == "__main__":
    unittest.main()