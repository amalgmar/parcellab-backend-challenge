from pydantic import BaseModel
from typing import List


class ArticleSchema(BaseModel):
    article_name: str
    article_quantity: int
    article_price: float
    SKU: str

    class Config:
        orm_mode = True


class ShipmentSchema(BaseModel):
    tracking_number: str
    carrier: str
    sender_address: str
    receiver_address: str
    status: str
    articles: List[ArticleSchema] = []

    class Config:
        orm_mode = True
