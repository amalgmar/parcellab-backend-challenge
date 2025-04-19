from typing import List
from pydantic import BaseModel, ConfigDict


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
