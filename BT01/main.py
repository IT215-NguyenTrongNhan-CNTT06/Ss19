from fastapi import FastAPI
from database import Base, engine
# Import các model để Base.metadata.create_all nhận biết
from app.models.supply_chain_model import WarehouseModel, PackageModel, WaybillModel
from app.routers.supply_chain_router import supply_chain_router

app = FastAPI(
    title="Supply Chain Management API"
)

Base.metadata.create_all(bind=engine)

app.include_router(supply_chain_router)

@app.get("/")
def get_root():
    return "Supply Chain Server đang khởi động"
