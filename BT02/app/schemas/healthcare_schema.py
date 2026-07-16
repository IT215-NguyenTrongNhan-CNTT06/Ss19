from pydantic import BaseModel
from typing import List, Optional

class ClinicBase(BaseModel):
    clinic_name: str
    specialty: str

class ClinicCreate(ClinicBase):
    pass

class DoctorResponse(BaseModel):
    id: int
    doctor_code: str
    salary: float
    clinic_id: int

    class Config:
        from_attributes = True

class ClinicDetailResponse(ClinicBase):
    id: int
    doctors: List[DoctorResponse] = []

    class Config:
        from_attributes = True

class DoctorUpdate(BaseModel):
    doctor_code: Optional[str] = None
    salary: Optional[float] = None
    clinic_id: Optional[int] = None

class LicenseResponse(BaseModel):
    id: int
    license_number: str
    issue_by: str
    doctor_id: int

    class Config:
        from_attributes = True
