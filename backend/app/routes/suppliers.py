from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Supplier
from app.schemas import SupplierCreate
from app.deps import get_db

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.post("/")
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(name=data.name)
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier