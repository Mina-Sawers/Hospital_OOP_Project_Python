import json
from models.department import Department
from models.staff import Staff
from models.person import Person
from models.patient import Patient
from models.hospital import Hospital


def _patient_to_dict(patient: Patient) -> dict:
    """Convert a single Patient object into a JSON-friendly dict."""
    return {
        "patient_id": patient.patient_id,
        "name": patient.name,
        "age": patient.age,
        "medical_record": patient.medical_record,
        "room": patient.room,
        "status": patient.status,
    }


def _staff_to_dict(staff_member: Staff) -> dict:
    """Convert a single Staff object into a JSON-friendly dict."""
    return {
        "name": staff_member.name,
        "age": staff_member.age,
        "position": staff_member.position,
    }


def _department_to_dict(department: Department) -> dict:
    """Convert a Department (and everyone inside it) into a dict."""
    return {
        "name": department.name,
        "patients": [_patient_to_dict(p) for p in department.patients],
        "staff": [_staff_to_dict(s) for s in department.staff],
    }


def Save_data(hospital: Hospital, filePath: str) -> None:
    '''
    this function writes the hospital's current state to JSON file

    Arg: hospital: the Hospital object holding the app's current state.
         filePath: the path to the JSON file to write to.
    '''
    data = {
        "name": hospital.name,
        "location": hospital.location,
        "departments": [_department_to_dict(d) for d in hospital.departments],
    }

    with open(filePath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def Load_data(filePath: str) -> Hospital:
    '''
    this function reads hospital data from a JSON file and returns a populated Hospital object

    Arg: filepath as string. the path to the JSON file

    Return: a Hospital object, or None if the file doesn't exist yet / is
    empty / is corrupted, so main.py can fall back to a brand-new Hospital
    instead of crashing on first run.
    '''
    try:
        with open(filePath, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except OSError:
        return None

    if not content:
        # Brand-new / empty data file (e.g. first run of the app).
        return None

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return None

    try:
        hospital = Hospital(data["name"], data["location"])

        for dept_data in data.get("departments", []):
            department = Department(dept_data["name"])

            for patient_data in dept_data.get("patients", []):
                patient = Patient(
                    name=patient_data["name"],
                    age=patient_data["age"],
                    medical_record=patient_data["medical_record"],
                    patient_id=patient_data.get("patient_id"),
                    room=patient_data.get("room", "N/A"),
                    status=patient_data.get("status", "Stable"),
                )
                department.add_patient(patient)

            for staff_data in dept_data.get("staff", []):
                staff_member = Staff(
                    staff_data["name"],
                    staff_data["age"],
                    staff_data["position"],
                )
                department.add_staff(staff_member)

            hospital.add_department(department)

        return hospital
    except KeyError:
        return None






