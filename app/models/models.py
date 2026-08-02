from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Customer(Base):
    """A customer record synchronized across CRM / ERP / billing systems."""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    external_crm_id = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="onboarding")  # onboarding, active, suspended
    created_at = Column(DateTime, default=datetime.utcnow)

    sync_logs = relationship("SyncLog", back_populates="customer")


class Integration(Base):
    """A configured third-party system connection (CRM, ERP, billing, HRIS, etc.)."""
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)          # e.g. "Salesforce CRM"
    service_type = Column(String, nullable=False)   # crm, erp, billing, hris, support
    base_url = Column(String, nullable=False)
    auth_type = Column(String, default="oauth2")     # oauth2, api_key
    is_active = Column(Integer, default=1)
    last_synced_at = Column(DateTime, nullable=True)


class SyncLog(Base):
    """Audit trail of every data-exchange event between Nexus and an external system."""
    __tablename__ = "sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    integration_id = Column(Integer, ForeignKey("integrations.id"), nullable=False)
    direction = Column(String, nullable=False)      # inbound, outbound
    status = Column(String, nullable=False)         # success, failed, retrying
    records_synced = Column(Integer, default=0)
    latency_ms = Column(Float, nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="sync_logs")


class ServiceAccount(Base):
    """OAuth2 / JWT-authenticated service account used for machine-to-machine calls."""
    __tablename__ = "service_accounts"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True, nullable=False)
    hashed_secret = Column(String, nullable=False)
    scopes = Column(String, default="sync:read sync:write")
    created_at = Column(DateTime, default=datetime.utcnow)
