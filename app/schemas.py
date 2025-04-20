from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ShipmentFilters(BaseModel):
    carrier: Optional[str] = None
    status: Optional[str] = None
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(10, ge=1, le=100, description="Items per page")


class ArticleSchema(BaseModel):
    article_name: str
    article_quantity: int
    article_price: float
    SKU: str

    model_config = ConfigDict(from_attributes=True)


class ShipmentSchema(BaseModel):
    tracking_number: str
    carrier: str
    sender_address: str
    receiver_address: str
    status: str
    articles: List[ArticleSchema] = []

    model_config = ConfigDict(from_attributes=True)


class PaginatedShipmentsResponse(BaseModel):
    total: int
    page: int
    limit: int
    shipments: List[ShipmentSchema]
