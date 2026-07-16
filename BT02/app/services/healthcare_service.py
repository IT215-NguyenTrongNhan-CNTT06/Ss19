from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.healthcare_model import ClinicModel, DoctorModel, LicenseModel
from app.schemas.healthcare_schema import ClinicCreate, DoctorUpdate

def create_clinic(db: Session, clinic: ClinicCreate):
    try:
        new_clinic = ClinicModel(**clinic.model_dump())
        db.add(new_clinic)
        db.commit()
        db.refresh(new_clinic)
        return new_clinic
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

def get_clinic_by_id(db: Session, clinic_id: int):
    clinic = (
        db.query(ClinicModel)
        .options(joinedload(ClinicModel.doctors))
        .filter(ClinicModel.id == clinic_id)
        .first()
    )
    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")
    return clinic

def update_doctor(db: Session, doctor_id: int, doctor_data: DoctorUpdate):
    doctor = db.query(DoctorModel).filter(DoctorModel.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    update_data = doctor_data.model_dump(exclude_unset=True)
    try:
        for key, value in update_data.items():
            setattr(doctor, key, value)
        db.commit()
        db.refresh(doctor)
        return doctor
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

def delete_license(db: Session, license_id: int):
    license_obj = db.query(LicenseModel).filter(LicenseModel.id == license_id).first()
    if not license_obj:
        raise HTTPException(status_code=404, detail="License not found")
    
    try:
        db.delete(license_obj)
        db.commit()
        return {"message": "Xóa chứng chỉ hành nghề thành công"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
