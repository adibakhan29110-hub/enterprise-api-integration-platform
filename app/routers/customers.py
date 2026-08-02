from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_client
from app.models.models import Customer
from app.models.schemas import CustomerCreate, CustomerOut

router = APIRouter(prefix="/customers", tags=["Customer Onboarding"])


@router.post("/", response_model=CustomerOut, status_code=201)
def onboard_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    _client: dict = Depends(get_current_client),
):
    """
    Onboards a new customer and prepares them for cross-system
    synchronization (CRM, ERP, billing, HRIS).
    """
    existing = db.query(Customer).filter(Customer.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer already exists")

    customer = Customer(
        name=payload.name,
        email=payload.email,
        external_crm_id=payload.external_crm_id,
        status="onboarding",
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/", response_model=List[CustomerOut])
def list_customers(db: Session = Depends(get_db), _client: dict = Depends(get_current_client)):
    return db.query(Customer).all()


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db), _client: dict = Depends(get_current_client)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
