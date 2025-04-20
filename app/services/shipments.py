from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload
from app.models import Shipment
from app.schemas import ShipmentFilters


def get_shipment_by_tracking(db: Session, tracking_number: str, carrier: str):
    return db.query(Shipment).filter(
        Shipment.tracking_number == tracking_number,
        Shipment.carrier == carrier
    ).first()


def fetch_shipments(db: Session, filters: ShipmentFilters):
    query = select(Shipment).options(selectinload(Shipment.articles))

    if filters.carrier:
        query = query.where(Shipment.carrier == filters.carrier)

    if filters.status:
        query = query.where(Shipment.status == filters.status)

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar()

    shipments = db.execute(
        query.offset((filters.page - 1) * filters.limit).limit(filters.limit)
    ).scalars().all()

    return shipments, total
