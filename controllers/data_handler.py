import json
from models.department import Department
from models.staff import Staff
from models.person import Person
from models.patient import Patient
from models.hospital import Hospital


def Load_data(filePath: str) -> Hospital:
    '''
    this function reads hospital data from a JSON file and returns a populated Hospital object
    
    Arg: filepath as string. the path to the JSON file
    
    Return: a Hospital object
    '''
    pass

def Save_data(hospital: Hospital, filePath: str)->None:
    '''
    this function writes the hospital's current state to JSON file
    '''
    pass

