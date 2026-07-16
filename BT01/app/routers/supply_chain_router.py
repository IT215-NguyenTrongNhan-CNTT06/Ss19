from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import app.services.supply_chain_service as service
from app.schemas.supply_chain_schema import (
    WarehouseCreate, 
    WarehouseDetailResponse, 
    PackageUpdate, 
    PackageResponse
)

supply_chain_router = APIRouter(
    tags=["Supply Chain"]
)

@supply_chain_router.post("/warehouses", response_model=WarehouseDetailResponse, status_code=201)
def create_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    return service.create_warehouse(db, warehouse)

@supply_chain_router.get("/warehouses/{warehouse_id}", response_model=WarehouseDetailResponse)
def get_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    return service.get_warehouse_by_id(db, warehouse_id)

@supply_chain_router.patch("/packages/{package_id}", response_model=PackageResponse)
def update_package(package_id: int, package_data: PackageUpdate, db: Session = Depends(get_db)):
    return service.update_package(db, package_id, package_data)

@supply_chain_router.delete("/waybills/{waybill_id}")
def delete_waybill(waybill_id: int, db: Session = Depends(get_db)):
    return service.delete_waybill(db, waybill_id)
