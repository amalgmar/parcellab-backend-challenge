from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, index=True)
    carrier = Column(String, index=True)
    sender_address = Column(String)
    receiver_address = Column(String)
    status = Column(String, index=True)

    articles = relationship("Article", back_populates="shipment", lazy="selectin")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    article_name = Column(String)
    article_quantity = Column(Integer)
    article_price = Column(Float)
    SKU = Column(String)

    shipment = relationship("Shipment", back_populates="articles", lazy="selectin")
