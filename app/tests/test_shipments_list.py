from app.tests.factories.shipment_factory import ShipmentFactory
from sqlalchemy.orm import Session


def test_list_shipments_with_pagination(client, db: Session):
    ShipmentFactory._meta.sqlalchemy_session = db

    # Create 5 unique test shipments with identifiable carrier
    for _ in range(5):
        ShipmentFactory.create(status="in-transit", carrier="PaginationCarrier")

    db.commit()

    # Request with limit=2 (should return only 2 items)
    response = client.get("/shipments?page=1&limit=2&carrier=PaginationCarrier")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total"] == 5
    assert len(data["shipments"]) == 2
    assert all(s["carrier"] == "PaginationCarrier" for s in data["shipments"])


def test_list_shipments_with_filters(client, db: Session):
    ShipmentFactory._meta.sqlalchemy_session = db

    # Use a unique test carrier to avoid collision with other tests or seed data
    ShipmentFactory.create(carrier="TestFilterCarrier", status="delivery")
    ShipmentFactory.create(carrier="TestFilterCarrier", status="in-transit")
    db.commit()

    response = client.get("/shipments?carrier=TestFilterCarrier&status=in-transit")
    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 1
    assert len(data["shipments"]) == 1
    assert data["shipments"][0]["carrier"] == "TestFilterCarrier"
    assert data["shipments"][0]["status"] == "in-transit"
