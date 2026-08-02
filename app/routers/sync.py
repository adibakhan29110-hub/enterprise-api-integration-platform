from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_client
from app.models.models import SyncLog
from app.models.schemas import SyncLogOut, SyncTrigger
from app.services.sync_service import run_data_sync

router = APIRouter(prefix="/sync", tags=["Data Synchronization"])


@router.post("/trigger", response_model=SyncLogOut)
def trigger_sync(
    payload: SyncTrigger,
    db: Session = Depends(get_db),
    _client: dict = Depends(get_current_client),
):
    """
    Triggers an automated data-exchange cycle with a connected third-party
    system, replacing what would otherwise be manual data entry/reconciliation.
    """
    log = run_data_sync(db, payload.integration_id, payload.customer_id, payload.direction)
    return log


@router.get("/logs", response_model=List[SyncLogOut])
def get_sync_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    _client: dict = Depends(get_current_client),
):
    return db.query(SyncLog).order_by(SyncLog.created_at.desc()).limit(limit).all()
