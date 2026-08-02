import random
import time
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.models import Integration, SyncLog


def run_data_sync(db: Session, integration_id: int, customer_id: int | None, direction: str) -> SyncLog:
    """
    Executes a data-exchange cycle with an external system.

    In production this would call the third-party REST/SOAP API for the
    given integration (e.g. Salesforce, NetSuite, Stripe, Workday),
    transform the payload, and persist the reconciled records. Here the
    network round trip is simulated so the platform can be demoed and
    load-tested without live credentials.
    """
    integration = db.query(Integration).filter(Integration.id == integration_id).first()
    if integration is None:
        raise ValueError("Unknown integration")

    start = time.perf_counter()
    # Simulated third-party API call
    time.sleep(random.uniform(0.05, 0.2))
    success = random.random() > 0.05  # ~95% success rate, mirrors production SLAs
    latency_ms = round((time.perf_counter() - start) * 1000, 2)
    records = random.randint(1, 500)

    log = SyncLog(
        customer_id=customer_id,
        integration_id=integration_id,
        direction=direction,
        status="success" if success else "failed",
        records_synced=records if success else 0,
        latency_ms=latency_ms,
        message="Sync completed" if success else "Upstream timeout — will retry",
    )

    integration.last_synced_at = datetime.utcnow()

    db.add(log)
    db.commit()
    db.refresh(log)
    return log
