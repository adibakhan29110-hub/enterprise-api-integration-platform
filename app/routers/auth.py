from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.models import ServiceAccount
from app.models.schemas import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201)
def register_service_account(client_id: str, client_secret: str, db: Session = Depends(get_db)):
    """Registers a new machine service account for secure inter-service API access."""
    existing = db.query(ServiceAccount).filter(ServiceAccount.client_id == client_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="client_id already registered")

    account = ServiceAccount(client_id=client_id, hashed_secret=hash_password(client_secret))
    db.add(account)
    db.commit()
    return {"message": "Service account registered", "client_id": client_id}


@router.post("/token", response_model=Token)
def issue_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth 2.0 client-credentials-style token endpoint.
    Exchanges valid service-account credentials for a signed JWT
    used to authenticate all subsequent integration/sync calls.
    """
    account = db.query(ServiceAccount).filter(ServiceAccount.client_id == form_data.username).first()
    if not account or not verify_password(form_data.password, account.hashed_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect client_id or client_secret",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": account.client_id, "scopes": account.scopes})
    return Token(access_token=token)
