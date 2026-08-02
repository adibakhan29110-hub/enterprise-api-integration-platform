# Enterprise API Integration Platform

A scalable backend platform that integrates multiple third-party APIs for cross-system
data exchange — built with **FastAPI**, **PostgreSQL**, **Docker**, and **JWT / OAuth 2.0**.

## Highlights

- Developed a scalable backend platform integrating multiple third-party APIs for
  cross-system data exchange.
- Implemented OAuth 2.0 authentication and secure API communication across services.
- Designed modular microservices for customer onboarding and data synchronization.
- Automated data exchange between external platforms, reducing manual processing effort.

## Tech Stack

| Layer          | Technology                          |
|----------------|--------------------------------------|
| API Framework  | FastAPI (Python)                     |
| Database       | PostgreSQL + SQLAlchemy ORM          |
| Auth           | OAuth 2.0 client-credentials + JWT   |
| Containerization | Docker / docker-compose            |
| Frontend       | Static HTML/CSS/JS ops dashboard     |

## Project Structure

```
enterprise-api-integration-platform/
├── app/
│   ├── main.py                # FastAPI app entrypoint
│   ├── core/
│   │   ├── config.py           # Settings (env-driven)
│   │   ├── database.py         # SQLAlchemy engine/session
│   │   └── security.py         # JWT issuing/validation, password hashing
│   ├── models/
│   │   ├── models.py           # SQLAlchemy ORM models
│   │   └── schemas.py          # Pydantic request/response schemas
│   ├── routers/
│   │   ├── auth.py             # OAuth2 token issuance, service account registration
│   │   ├── customers.py        # Customer onboarding microservice
│   │   ├── integrations.py     # Third-party system registration
│   │   └── sync.py             # Data synchronization microservice
│   └── services/
│       └── sync_service.py     # Core sync/integration logic
├── frontend/
│   └── dashboard.html          # Live operations dashboard (open directly in browser)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Running Locally

### Option 1 — Docker (recommended)

```bash
cp .env.example .env
docker-compose up --build
```

API will be available at `http://localhost:8000`
Interactive API docs (Swagger UI): `http://localhost:8000/docs`

### Option 2 — Local Python environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # update DATABASE_URL to point at a local Postgres instance
uvicorn app.main:app --reload
```

### Dashboard

Open `frontend/dashboard.html` directly in a browser to view the operations dashboard
(integration status, sync volume, live event log, microservice health).

## API Overview

| Method | Endpoint              | Description                                   |
|--------|------------------------|-----------------------------------------------|
| POST   | `/auth/register`       | Register a new OAuth2 service account          |
| POST   | `/auth/token`          | Exchange credentials for a JWT access token     |
| POST   | `/customers/`          | Onboard a new customer                          |
| GET    | `/customers/`          | List onboarded customers                        |
| POST   | `/integrations/`       | Register a third-party system (CRM, ERP, etc.)  |
| GET    | `/integrations/`       | List connected integrations                     |
| POST   | `/sync/trigger`        | Trigger a data-synchronization cycle            |
| GET    | `/sync/logs`           | View recent synchronization audit logs          |

All endpoints except `/auth/*` require a valid `Bearer` JWT obtained from `/auth/token`.

## Notes

This is a portfolio-scale reference implementation: the third-party API calls in
`sync_service.py` are simulated so the project can be run and demoed without live
credentials for Salesforce, NetSuite, Stripe, or Workday. Swap in real `httpx` calls
to each provider's REST API to make it production-ready.
