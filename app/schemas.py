"""Pydantic schemas for serializing shipment, article, and weather data."""

from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class ShipmentFilters(BaseModel):
    """Query parameters for filtering and paginating shipments.

    Attributes:
        carrier (Optional[str]): Filter by shipment carrier (e.g., DHL, UPS).
        status (Optional[str]): Filter by shipment status (e.g., in-transit).
        page (int): Page number (minimum 1).
        limit (int): Items per page (1–100).
    """

    carrier: Optional[str] = Field(None, description='Filter by carrier name')
    status: Optional[str] = Field(None, description='Filter by shipment status')
    page: int = Field(1, ge=1, description='Page number')
    limit: int = Field(10, ge=1, le=100, description='Number of results per page')


class ArticleSchema(BaseModel):
    """Represents an individual article included in a shipment.

    Attributes:
        article_name (str): Name of the article.
        article_quantity (int): Quantity of the article.
        article_price (float): Price per unit of the article.
        SKU (str): Stock Keeping Unit identifier.
    """

    article_name: str
    article_quantity: int
    article_price: float
    SKU: str

    model_config = ConfigDict(from_attributes=True)


class ShipmentSchema(BaseModel):
    """Represents a shipment and its associated metadata.

    Attributes:
        tracking_number (str): Unique tracking number for the shipment.
        carrier (str): Name of the carrier service.
        sender_address (str): Address from which the shipment was sent.
        receiver_address (str): Destination address of the shipment.
        status (str): Current status of the shipment.
        articles (List[ArticleSchema]): List of articles in the shipment.
    """

    tracking_number: str
    carrier: str
    sender_address: str
    receiver_address: str
    status: str
    articles: List[ArticleSchema] = []

    model_config = ConfigDict(from_attributes=True)


class PaginatedShipmentsResponse(BaseModel):
    """Paginated response for listing shipments.

    Attributes:
        total (int): Total number of matched shipments.
        page (int): Current page number.
        limit (int): Number of shipments per page.
        shipments (List[ShipmentSchema]): List of shipment entries.
    """

    total: int
    page: int
    limit: int
    shipments: List[ShipmentSchema]


class WeatherSchema(BaseModel):
    """Weather conditions at the receiver's ZIP code.

    Attributes:
        description (Optional[str]): Weather description (e.g., clear sky).
        temperature (Optional[float]): Current temperature in Celsius.
        city (Optional[str]): City name based on ZIP code.
        warning (Optional[str]): Any warning if weather could not be fetched.
    """

    description: Optional[str]
    temperature: Optional[float]
    city: Optional[str]
    warning: Optional[str] = None


class ShipmentWithWeatherResponse(BaseModel):
    """Combined shipment and weather response.

    Attributes:
        shipment (ShipmentSchema): Shipment information.
        weather (Union[WeatherSchema, dict, None]): Weather details or fallback.
    """

    shipment: ShipmentSchema
    weather: Union[WeatherSchema, dict, None]
