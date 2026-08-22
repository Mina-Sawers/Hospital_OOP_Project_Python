#tests the data handler behaviour

import json
import os
import tempfile
import unittest

from models.hospital import Hospital
from models.department import Department
from models.patient import Patient
from models.staff import Staff
from controllers.data_handler import Save_data, Load_data


class TestSaveData(unittest.TestCase):
    def setUp(self):
        # Every test gets its own temp file so tests never touch the real
        # data/hospital_data.json and never interfere with each other.
        fd, self.temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

    def tearDown(self):
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    def test_save_data_creates_a_file(self):
        hospital = Hospital("City General Hospital", "123 Main St")
        Save_data(hospital, self.temp_path)
        self.assertTrue(os.path.exists(self.temp_path))

    def test_save_data_writes_valid_json(self):
        hospital = Hospital("City General Hospital", "123 Main St")
        Save_data(hospital, self.temp_path)
        with open(self.temp_path, "r", encoding="utf-8") as f:
            data = json.load(f)  # raises if the file isn't valid JSON
        self.assertEqual(data["name"], "City General Hospital")
        self.assertEqual(data["location"], "123 Main St")


class TestLoadData(unittest.TestCase):
    def setUp(self):
        fd, self.temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

    def tearDown(self):
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    def test_load_data_returns_none_when_file_missing(self):
        os.remove(self.temp_path)
        result = Load_data(self.temp_path)
        self.assertIsNone(result)

    def test_load_data_returns_none_when_file_is_empty(self):
        # This is the state of data/hospital_data.json before the app has
        # ever saved anything -- Neamat's startup code needs this to come
        # back as None (not crash) so it can create a fresh Hospital.
        result = Load_data(self.temp_path)
        self.assertIsNone(result)

    def test_load_data_returns_none_on_corrupted_json(self):
        with open(self.temp_path, "w", encoding="utf-8") as f:
            f.write("{ this is not valid json ")
        result = Load_data(self.temp_path)
        self.assertIsNone(result)

    def test_load_data_returns_none_on_missing_fields(self):
        with open(self.temp_path, "w", encoding="utf-8") as f:
            json.dump({"name": "City General Hospital"}, f)  # no "location"
        result = Load_data(self.temp_path)
        self.assertIsNone(result)

    def test_load_data_rebuilds_a_hospital_with_no_departments(self):
        hospital = Hospital("City General Hospital", "123 Main St")
        Save_data(hospital, self.temp_path)

        loaded = Load_data(self.temp_path)
        self.assertIsInstance(loaded, Hospital)
        self.assertEqual(loaded.name, "City General Hospital")
        self.assertEqual(loaded.location, "123 Main St")
        self.assertEqual(loaded.departments, [])


class TestRoundTrip(unittest.TestCase):
    """Save a fully populated Hospital, load it back, and check every field
    (including Patient's id/room/status) survived the trip."""

    def setUp(self):
        fd, self.temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        self.hospital = Hospital("City General Hospital", "123 Main St")

        cardiology = Department("Cardiology")
        cardiology.add_patient(Patient(
            "Alice Johnson", 34, "No known allergies",
            patient_id="PT-1001", room="2A-05", status="Stable",
        ))
        cardiology.add_staff(Staff("Dr. Sarah Smith", 45, "Cardiologist"))
        self.hospital.add_department(cardiology)

        pediatrics = Department("Pediatrics")
        pediatrics.add_patient(Patient(
            "Tommy Lee", 7, "Asthma, seasonal",
            patient_id="PT-1002", room="3B-02", status="Observation",
        ))
        pediatrics.add_staff(Staff("Dr. Omar Hassan", 38, "Pediatrician"))
        self.hospital.add_department(pediatrics)

    def tearDown(self):
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    def test_round_trip_preserves_department_count_and_names(self):
        Save_data(self.hospital, self.temp_path)
        loaded = Load_data(self.temp_path)
        self.assertEqual(len(loaded.departments), 2)
        self.assertEqual(
            [d.name for d in loaded.departments], ["Cardiology", "Pediatrics"]
        )

    def test_round_trip_preserves_patient_data_including_id_room_status(self):
        Save_data(self.hospital, self.temp_path)
        loaded = Load_data(self.temp_path)

        patient = loaded.departments[0].patients[0]
        self.assertIsInstance(patient, Patient)
        self.assertEqual(patient.patient_id, "PT-1001")
        self.assertEqual(patient.name, "Alice Johnson")
        self.assertEqual(patient.age, 34)
        self.assertEqual(patient.medical_record, "No known allergies")
        self.assertEqual(patient.room, "2A-05")
        self.assertEqual(patient.status, "Stable")

    def test_round_trip_preserves_staff_data(self):
        Save_data(self.hospital, self.temp_path)
        loaded = Load_data(self.temp_path)

        staff_member = loaded.departments[0].staff[0]
        self.assertIsInstance(staff_member, Staff)
        self.assertEqual(staff_member.name, "Dr. Sarah Smith")
        self.assertEqual(staff_member.age, 45)
        self.assertEqual(staff_member.position, "Cardiologist")

    def test_loaded_objects_behave_like_the_originals(self):
        # Not just data equality -- the loaded Patient should be a real
        # object whose own methods (and default patient_id logic) still work.
        Save_data(self.hospital, self.temp_path)
        loaded = Load_data(self.temp_path)

        patient = loaded.departments[0].patients[0]
        self.assertEqual(patient.view_record(), "No known allergies")
        patient.update_status("Critical")
        self.assertIn("Critical", patient.view_info())


if __name__ == "__main__":
    unittest.main()