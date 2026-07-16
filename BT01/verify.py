from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_db, LocalSession
from sqlalchemy.orm import Session
from app.models.supply_chain_model import WarehouseModel, PackageModel, WaybillModel

client = TestClient(app)

# Clean and recreate tables to ensure fresh test state
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def test_flow():
    # 1. Create a Warehouse
    wh_data = {"warehouse_name": "Warehouse A", "location": "District 1, HCM City"}
    response = client.post("/warehouses", json=wh_data)
    assert response.status_code == 201
    wh = response.json()
    print("Created Warehouse:", wh)
    wh_id = wh["id"]

    # 2. Add some packages and a waybill via db session
    db: Session = LocalSession()
    try:
        pkg1 = PackageModel(package_code="PKG001", weight=10.5, warehouse_id=wh_id)
        pkg2 = PackageModel(package_code="PKG002", weight=15.2, warehouse_id=wh_id)
        db.add(pkg1)
        db.add(pkg2)
        db.commit()
        db.refresh(pkg1)
        db.refresh(pkg2)
        
        waybill1 = WaybillModel(tracking_number="WB001", shipping_status="SHIPPED", package_id=pkg1.id)
        db.add(waybill1)
        db.commit()
        db.refresh(waybill1)
        print(f"Added Package 1 (ID: {pkg1.id}), Package 2 (ID: {pkg2.id}), and Waybill 1 (ID: {waybill1.id})")
        wb_id = waybill1.id
        pkg1_id = pkg1.id
    finally:
        db.close()

    # 3. Get Warehouse Detail (1-N relationship test)
    response = client.get(f"/warehouses/{wh_id}")
    assert response.status_code == 200
    wh_detail = response.json()
    print("Warehouse Detail (packages included):", wh_detail)
    assert len(wh_detail["packages"]) == 2

    # 4. Patch Package (dynamic update test)
    patch_data = {"weight": 12.8} # only update weight
    response = client.patch(f"/packages/{pkg1_id}", json=patch_data)
    assert response.status_code == 200
    pkg_updated = response.json()
    print("Updated Package 1:", pkg_updated)
    assert pkg_updated["weight"] == 12.8
    assert pkg_updated["package_code"] == "PKG001" # unchanged

    # 5. Delete Waybill (hard delete test)
    response = client.delete(f"/waybills/{wb_id}")
    assert response.status_code == 200
    print("Delete Waybill response:", response.json())

    # Verify Waybill is gone
    db = LocalSession()
    try:
        wb_check = db.query(WaybillModel).filter(WaybillModel.id == wb_id).first()
        assert wb_check is None
        print("Confirmed: Waybill has been hard deleted from the DB.")
    finally:
        db.close()

if __name__ == "__main__":
    test_flow()
    print("Exercise 1 Verification Flow PASSED!")
