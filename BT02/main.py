from fastapi import FastAPI
from database import Base, engine
# Import các model để Base.metadata.create_all nhận biết
from app.models.healthcare_model import ClinicModel, DoctorModel, LicenseModel
from app.routers.healthcare_router import healthcare_router

app = FastAPI(
    title="Healthcare Management API"
)

Base.metadata.create_all(bind=engine)

app.include_router(healthcare_router)

@app.get("/")
def get_root():
    return "Healthcare Server đang khởi động"
