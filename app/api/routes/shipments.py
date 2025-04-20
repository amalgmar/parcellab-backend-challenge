"""API routes for accessing and querying shipment and weather data."""

import logging
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas import (
    PaginatedShipmentsResponse,
    ShipmentFilters,
    ShipmentSchema,
    ShipmentWithWeatherResponse,
)
from app.services.shipments import fetch_shipments, get_shipment_by_tracking
from app.services.weather import get_weather_by_zip
from app.utils.extract_zip import extract_zip

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    '/shipments/{tracking_number}',
    response_model=ShipmentWithWeatherResponse,
    tags=['Shipments'],
    summary='Retrieve shipment and weather data by tracking number',
    response_description='Shipment details including weather at the destination'
)
def shipment_lookup(
    tracking_number: str,
    carrier: str = Query(..., description='The carrier name (e.g., DHL, UPS)'),
    db: Session = Depends(get_db),
) -> ShipmentWithWeatherResponse:
    """Retrieve shipment details with weather based on tracking number and carrier.

    Args:
        tracking_number (str): Shipment tracking number.
        carrier (str): Carrier name to validate against (e.g., DHL, UPS).
        db (Session): SQLAlchemy database session dependency.

    Returns:
        ShipmentWithWeatherResponse: Shipment data and weather info at destination ZIP.

    Raises:
        HTTPException: 404 if shipment not found, 500 for unexpected errors.
    """
    try:
        shipment = get_shipment_by_tracking(db, tracking_number, carrier)
        if not shipment:
            raise HTTPException(status_code=404, detail='Shipment not found')

        zip_code = extract_zip(shipment.receiver_address)
        weather = get_weather_by_zip(zip_code) if zip_code else None

        return ShipmentWithWeatherResponse(
            shipment=ShipmentSchema.model_validate(shipment),
            weather=weather,
        )

    except HTTPException:
        raise  # Let FastAPI handle known HTTP exceptions

    except Exception as exc:
        logger.exception('Unhandled exception in shipment_lookup')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error',
        ) from exc


@router.get(
    '/shipments',
    response_model=PaginatedShipmentsResponse,
    tags=['Shipments'],
    summary='List all shipments with optional filters and pagination',
    response_description='Paginated list of shipments'
)
def list_shipments(
    filters: ShipmentFilters = Depends(),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Retrieve a paginated list of shipments with optional filtering.

    Args:
        filters (ShipmentFilters): Query parameters for filtering and pagination.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        dict: Contains `total`, `page`, `limit`, and list of `shipments`.
    """
    shipments, total = fetch_shipments(db, filters)
    return {
        'total': total,
        'page': filters.page,
        'limit': filters.limit,
        'shipments': shipments,
    }
