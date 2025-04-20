"""SQLAlchemy models for Shipment and Article."""

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


# pylint: disable=too-few-public-methods
class Shipment(Base):
    """Represents a shipment."""

    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, index=True)
    carrier = Column(String, index=True)
    sender_address = Column(String)
    receiver_address = Column(String)
    status = Column(String, index=True)

    articles = relationship('Article', back_populates='shipment', lazy='selectin')


# pylint: disable=too-few-public-methods
class Article(Base):
    """Represents an article inside a shipment."""

    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey('shipments.id'))
    article_name = Column(String)
    article_quantity = Column(Integer)
    article_price = Column(Float)
    SKU = Column(String)

    shipment = relationship('Shipment', back_populates='articles', lazy='selectin')
