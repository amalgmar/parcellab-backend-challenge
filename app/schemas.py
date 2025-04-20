"""Pydantic schemas for serializing shipment and article data."""

from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class ShipmentFilters(BaseModel):
    """Schema for query filters and pagination."""

    carrier: Optional[str] = None
    status: Optional[str] = None
    page: int = Field(1, ge=1, description='Page number')
    limit: int = Field(10, ge=1, le=100, description='Items per page')


class ArticleSchema(BaseModel):
    """Schema for an article."""

    article_name: str
    article_quantity: int
    article_price: float
    SKU: str

    model_config = ConfigDict(from_attributes=True)


class ShipmentSchema(BaseModel):
    """Schema for a shipment."""

    tracking_number: str
    carrier: str
    sender_address: str
    receiver_address: str
    status: str
    articles: List[ArticleSchema] = []

    model_config = ConfigDict(from_attributes=True)


class PaginatedShipmentsResponse(BaseModel):
    """Schema for query filters and pagination."""

    total: int
    page: int
    limit: int
    shipments: List[ShipmentSchema]


class WeatherSchema(BaseModel):
    """Schema for weather data returned from the weather API."""

    description: Optional[str]
    temperature: Optional[float]
    city: Optional[str]
    warning: Optional[str] = None


class ShipmentWithWeatherResponse(BaseModel):
    """Schema combining shipment details and weather data."""

    shipment: ShipmentSchema
    weather: Union[WeatherSchema, dict, None]
