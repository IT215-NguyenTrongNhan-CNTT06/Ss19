from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ClinicModel(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    clinic_name = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=False)

    # Một Phòng khám có thể có Nhiều Bác sĩ (doctors) làm việc
    doctors = relationship("DoctorModel", back_populates="clinic", cascade="all, delete-orphan")


class DoctorModel(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_code = Column(String(100), unique=True, nullable=False, index=True)
    salary = Column(Float, nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False)

    # Bác sĩ thuộc về Một Phòng khám duy nhất (clinic)
    clinic = relationship("ClinicModel", back_populates="doctors")
    
    # Sở hữu duy nhất Một Chứng chỉ hành nghề (license)
    license = relationship("LicenseModel", back_populates="doctor", uselist=False, cascade="all, delete-orphan")


class LicenseModel(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    license_number = Column(String(100), unique=True, nullable=False, index=True)
    issue_by = Column(String(255), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Tương ứng quan hệ 1-1 với thực thể Bác sĩ (doctor)
    doctor = relationship("DoctorModel", back_populates="license")
