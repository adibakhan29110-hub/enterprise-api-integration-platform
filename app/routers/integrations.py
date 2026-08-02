from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_client
from app.models.models import Integration
from app.models.schemas import IntegrationCreate, IntegrationOut

router = APIRouter(prefix="/integrations", tags=["Third-Party Integrations"])


@router.post("/", response_model=IntegrationOut, status_code=201)
def register_integration(
    payload: IntegrationCreate,
    db: Session = Depends(get_db),
    _client: dict = Depends(get_current_client),
):
    """Registers a new third-party system (CRM, ERP, billing, HRIS, support desk...)."""
    integration = Integration(**payload.model_dump())
    db.add(integration)
    db.commit()
    db.refresh(integration)
    return integration


@router.get("/", response_model=List[IntegrationOut])
def list_integrations(db: Session = Depends(get_db), _client: dict = Depends(get_current_client)):
    return db.query(Integration).all()
