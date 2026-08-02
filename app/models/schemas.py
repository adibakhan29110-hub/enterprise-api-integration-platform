from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ClientCredentials(BaseModel):
    client_id: str
    client_secret: str


# --- Customer / onboarding ---
class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    external_crm_id: Optional[str] = None


class CustomerOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- Integrations ---
class IntegrationCreate(BaseModel):
    name: str
    service_type: str
    base_url: str
    auth_type: str = "oauth2"


class IntegrationOut(BaseModel):
    id: int
    name: str
    service_type: str
    is_active: int
    last_synced_at: Optional[datetime]

    class Config:
        from_attributes = True


# --- Sync events ---
class SyncTrigger(BaseModel):
    integration_id: int
    customer_id: Optional[int] = None
    direction: str = "outbound"


class SyncLogOut(BaseModel):
    id: int
    integration_id: int
    direction: str
    status: str
    records_synced: int
    latency_ms: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
