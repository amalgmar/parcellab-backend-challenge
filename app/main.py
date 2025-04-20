"""Main FastAPI entry point."""

from typing import Dict

from fastapi import FastAPI

from app.api.routes import shipments


app = FastAPI(
    title='📦 Track & Trace API',
    version='1.0.0',
    description="""
This API allows end users to track shipments and
 view current weather conditions at the destination.

**Features:**
- Lookup shipments by tracking number and carrier
- Fetch current weather at the destination ZIP
- Pagination and filtering by status or carrier

*Powered by FastAPI + PostgreSQL + OpenWeatherMap*
    """,
    contact={
        'name': 'Amal Gmar',
        'email': 'amalgmar7@gmail.com',
    },
    license_info={
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT',
    },
    docs_url='/docs',  # Swagger UI
    redoc_url='/redoc',  # ReDoc
)


@app.get('/health')
def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {'status': 'ok'}


app.include_router(shipments.router)
