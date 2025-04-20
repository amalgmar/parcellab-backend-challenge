"""Tests for shipment detail endpoint including weather integration."""

import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.tests.factories.shipment_factory import ArticleFactory, ShipmentFactory


def test_shipment_lookup_success(client: TestClient, db: Session) -> None:
    """Tests successful lookup of a shipment with weather info."""
    # pylint: disable=protected-access
    ShipmentFactory._meta.sqlalchemy_session = db
    # pylint: disable=protected-access
    ArticleFactory._meta.sqlalchemy_session = db

    shipment = ShipmentFactory.create(
        articles=[ArticleFactory.create(), ArticleFactory.create()]
    )
    db.commit()

    response = client.get(
        f'/shipments/{shipment.tracking_number}?carrier={shipment.carrier}'
    )
    assert response.status_code == 200
    assert len(response.json()['shipment']['articles']) == 2


def test_shipment_not_found(client: TestClient) -> None:
    """Tests 404 response for invalid tracking number."""
    response = client.get('/shipments/INVALID123?carrier=DHL')
    assert response.status_code == 404


def test_shipment_wrong_carrier(client: TestClient, db: Session) -> None:
    """Tests 404 response when wrong carrier is used."""
    # pylint: disable=protected-access
    ShipmentFactory._meta.sqlalchemy_session = db

    shipment = ShipmentFactory.create()
    db.commit()

    response = client.get(f'/shipments/{shipment.tracking_number}?carrier=UPS')
    assert response.status_code == 404


def test_weather_structure(client: TestClient, db: Session) -> None:
    """Validates weather structure returned in shipment detail."""
    # pylint: disable=protected-access
    ShipmentFactory._meta.sqlalchemy_session = db

    shipment = ShipmentFactory.create(
        receiver_address='Street 15, 1050 Copenhagen, Denmark'
    )
    db.commit()

    response = client.get(
        f'/shipments/{shipment.tracking_number}?carrier={shipment.carrier}'
    )
    assert response.status_code == 200
    weather = response.json()['weather']

    if 'warning' in weather:
        # Skipping assertion if weather service failed
        pytest.skip('Weather API unavailable during test run.')
    else:
        assert 'description' in weather
        assert 'temperature' in weather
        assert 'city' in weather
