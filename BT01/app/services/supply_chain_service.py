from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.supply_chain_model import WarehouseModel, PackageModel, WaybillModel
from app.schemas.supply_chain_schema import WarehouseCreate, PackageUpdate

def create_warehouse(db: Session, warehouse: WarehouseCreate):
    try:
        new_warehouse = WarehouseModel(**warehouse.model_dump())
        db.add(new_warehouse)
        db.commit()
        db.refresh(new_warehouse)
        return new_warehouse
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

def get_warehouse_by_id(db: Session, warehouse_id: int):
    warehouse = (
        db.query(WarehouseModel)
        .options(joinedload(WarehouseModel.packages))
        .filter(WarehouseModel.id == warehouse_id)
        .first()
    )
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

def update_package(db: Session, package_id: int, package_data: PackageUpdate):
    package = db.query(PackageModel).filter(PackageModel.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    
    update_data = package_data.model_dump(exclude_unset=True)
    try:
        for key, value in update_data.items():
            setattr(package, key, value)
        db.commit()
        db.refresh(package)
        return package
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

def delete_waybill(db: Session, waybill_id: int):
    waybill = db.query(WaybillModel).filter(WaybillModel.id == waybill_id).first()
    if not waybill:
        raise HTTPException(status_code=404, detail="Waybill not found")
    
    try:
        db.delete(waybill)
        db.commit()
        return {"message": "Xóa vận đơn thành công"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
