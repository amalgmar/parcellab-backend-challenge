from sqlalchemy.orm import Session
from app.models import Shipment


def get_shipment_by_tracking(db: Session, tracking_number: str, carrier: str):
    return db.query(Shipment).filter(
        Shipment.tracking_number == tracking_number,
        Shipment.carrier == carrier
    ).first()
