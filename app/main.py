from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, customers, integrations, sync

# Creates tables on startup if they don't already exist (use Alembic migrations in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description=(
        "A scalable backend platform integrating multiple third-party APIs "
        "for cross-system data exchange, with OAuth 2.0 / JWT-secured "
        "service-to-service communication and modular microservices for "
        "customer onboarding and data synchronization."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(integrations.router)
app.include_router(sync.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": settings.app_name}
