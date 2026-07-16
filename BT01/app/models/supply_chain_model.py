from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class WarehouseModel(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)

    # Một Nhà kho có thể chứa Nhiều Kiện hàng (packages)
    packages = relationship("PackageModel", back_populates="warehouse", cascade="all, delete-orphan")


class PackageModel(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    package_code = Column(String(100), unique=True, nullable=False, index=True)
    weight = Column(Float, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False)

    # Kiện hàng thuộc về Một Nhà kho duy nhất (warehouse)
    warehouse = relationship("WarehouseModel", back_populates="packages")
    
    # Sở hữu duy nhất Một Vận đơn chi tiết (waybill)
    waybill = relationship("WaybillModel", back_populates="package", uselist=False, cascade="all, delete-orphan")


class WaybillModel(Base):
    __tablename__ = "waybills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tracking_number = Column(String(100), unique=True, nullable=False, index=True)
    shipping_status = Column(String(100), nullable=False)
    package_id = Column(Integer, ForeignKey("packages.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Tương ứng quan hệ 1-1 với thực thể Kiện hàng (package)
    package = relationship("PackageModel", back_populates="waybill")
