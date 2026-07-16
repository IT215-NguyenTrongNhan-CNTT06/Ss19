from pydantic import BaseModel
from typing import List, Optional

class WarehouseBase(BaseModel):
    warehouse_name: str
    location: str

class WarehouseCreate(WarehouseBase):
    pass

class PackageResponse(BaseModel):
    id: int
    package_code: str
    weight: float
    warehouse_id: int

    class Config:
        from_attributes = True

class WarehouseDetailResponse(WarehouseBase):
    id: int
    packages: List[PackageResponse] = []

    class Config:
        from_attributes = True

class PackageUpdate(BaseModel):
    package_code: Optional[str] = None
    weight: Optional[float] = None
    warehouse_id: Optional[int] = None

class WaybillResponse(BaseModel):
    id: int
    tracking_number: str
    shipping_status: str
    package_id: int

    class Config:
        from_attributes = True
