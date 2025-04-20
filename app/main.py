"""Main FastAPI entry point."""

from typing import Dict

from fastapi import FastAPI

from app.api.routes import shipments

app = FastAPI()


@app.get('/health')
def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {'status': 'ok'}


app.include_router(shipments.router)
