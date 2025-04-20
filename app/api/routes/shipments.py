from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import ShipmentSchema, PaginatedShipmentsResponse, ShipmentFilters
from app.services.shipments import get_shipment_by_tracking, fetch_shipments
from app.services.weather import get_weather_by_zip
from app.utils.extract_zip import extract_zip
from fastapi import status
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/shipments/{tracking_number}")
def shipment_lookup(
        tracking_number: str,
        carrier: str = Query(...),
        db: Session = Depends(get_db)
):
    try:
        shipment = get_shipment_by_tracking(db, tracking_number, carrier)
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")

        zip_code = extract_zip(shipment.receiver_address)
        weather = get_weather_by_zip(zip_code) if zip_code else None

        return {
            "shipment": ShipmentSchema.model_validate(shipment),
            "weather": weather
        }
    except HTTPException:
        raise  # Let FastAPI handle known errors
    except Exception as e:
        logger.exception("Unhandled exception in shipment_lookup")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/shipments", response_model=PaginatedShipmentsResponse)
def list_shipments(filters: ShipmentFilters = Depends(), db: Session = Depends(get_db)):
    shipments, total = fetch_shipments(db, filters)
    return {
        "total": total,
        "page": filters.page,
        "limit": filters.limit,
        "shipments": shipments
    }
