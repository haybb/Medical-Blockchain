"""
Here is defined the class of a medical record
"""



from medical_parts import *


class MedicalRecord:
    """ This class defines a medical record and all its different parts """
    def __init__(self, id: int) -> None:
        """ 
        :param int id: the id of the patient """
        self._id = id
        self._healthData = HealthData(self._id)
        self._medicalBackground = MedicalBackground(self._id)
        self._prescription = Prescription(self._id)
        self._privateData = PrivateData(self._id)


    def __eq__(self, __o: object) -> bool:
        """ A medical record is entirely defined by his id """
        return self._id == __o._id
    

    def split(self) -> tuple[HealthData, MedicalBackground, Prescription, PrivateData]:
        """ Returns all parts of the medical record splited in a tuple """
        return self._healthData, self._medicalBackground, self._prescription, self._privateData
        






if __name__ == "__main__":
    record = MedicalRecord(0)
    health_data = record._healthData
    print("from record:", record._healthData.x)
    print("from variable:", health_data.x)
    health_data.x = 3615
    print("from record after change:", record._healthData.x)
    print("from variable after change:", health_data.x)
