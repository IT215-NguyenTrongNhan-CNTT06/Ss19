from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import app.services.healthcare_service as service
from app.schemas.healthcare_schema import (
    ClinicCreate, 
    ClinicDetailResponse, 
    DoctorUpdate, 
    DoctorResponse
)

healthcare_router = APIRouter(
    tags=["Healthcare"]
)

@healthcare_router.post("/clinics", response_model=ClinicDetailResponse, status_code=201)
def create_clinic(clinic: ClinicCreate, db: Session = Depends(get_db)):
    return service.create_clinic(db, clinic)

@healthcare_router.get("/clinics/{clinic_id}", response_model=ClinicDetailResponse)
def get_clinic(clinic_id: int, db: Session = Depends(get_db)):
    return service.get_clinic_by_id(db, clinic_id)

@healthcare_router.patch("/doctors/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, doctor_data: DoctorUpdate, db: Session = Depends(get_db)):
    return service.update_doctor(db, doctor_id, doctor_data)

@healthcare_router.delete("/licenses/{license_id}")
def delete_license(license_id: int, db: Session = Depends(get_db)):
    return service.delete_license(db, license_id)
