from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_db, LocalSession
from sqlalchemy.orm import Session
from app.models.healthcare_model import ClinicModel, DoctorModel, LicenseModel

client = TestClient(app)

# Clean and recreate tables to ensure fresh test state
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def test_flow():
    # 1. Create a Clinic
    clinic_data = {"clinic_name": "General Clinic", "specialty": "Internal Medicine"}
    response = client.post("/clinics", json=clinic_data)
    assert response.status_code == 201
    clinic = response.json()
    print("Created Clinic:", clinic)
    clinic_id = clinic["id"]

    # 2. Add some doctors and a license via db session
    db: Session = LocalSession()
    try:
        doc1 = DoctorModel(doctor_code="DOC001", salary=2500.0, clinic_id=clinic_id)
        doc2 = DoctorModel(doctor_code="DOC002", salary=3000.0, clinic_id=clinic_id)
        db.add(doc1)
        db.add(doc2)
        db.commit()
        db.refresh(doc1)
        db.refresh(doc2)
        
        lic1 = LicenseModel(license_number="LIC001", issue_by="Ministry of Health", doctor_id=doc1.id)
        db.add(lic1)
        db.commit()
        db.refresh(lic1)
        print(f"Added Doctor 1 (ID: {doc1.id}), Doctor 2 (ID: {doc2.id}), and License 1 (ID: {lic1.id})")
        lic_id = lic1.id
        doc1_id = doc1.id
    finally:
        db.close()

    # 3. Get Clinic Detail (1-N relationship test)
    response = client.get(f"/clinics/{clinic_id}")
    assert response.status_code == 200
    clinic_detail = response.json()
    print("Clinic Detail (doctors included):", clinic_detail)
    assert len(clinic_detail["doctors"]) == 2

    # 4. Patch Doctor (dynamic update test)
    patch_data = {"salary": 2800.0} # only update salary
    response = client.patch(f"/doctors/{doc1_id}", json=patch_data)
    assert response.status_code == 200
    doc_updated = response.json()
    print("Updated Doctor 1:", doc_updated)
    assert doc_updated["salary"] == 2800.0
    assert doc_updated["doctor_code"] == "DOC001" # unchanged

    # 5. Delete License (hard delete test)
    response = client.delete(f"/licenses/{lic_id}")
    assert response.status_code == 200
    print("Delete License response:", response.json())

    # Verify License is gone
    db = LocalSession()
    try:
        lic_check = db.query(LicenseModel).filter(LicenseModel.id == lic_id).first()
        assert lic_check is None
        print("Confirmed: License has been hard deleted from the DB.")
    finally:
        db.close()

if __name__ == "__main__":
    test_flow()
    print("Exercise 2 Verification Flow PASSED!")
