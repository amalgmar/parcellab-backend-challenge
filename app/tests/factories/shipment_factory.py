"""Factory module for generating Shipment and Article test data."""

from typing import Any

import factory

from app.models import Article, Shipment


class ArticleFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Article objects for tests."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for the SQLAlchemyModelFactory.

        - `model`: Specifies the SQLAlchemy model to use (Article or Shipment).
        - `sqlalchemy_session`: Allows injecting a session dynamically at runtime.
        - `sqlalchemy_session_persistence`:
        Determines how session changes are flushed (e.g., 'flush', 'commit').
        """

        model = Article
        sqlalchemy_session = None  # 🔑 Allow dynamic session injection
        sqlalchemy_session_persistence = 'flush'

    article_name = factory.Sequence(lambda n: f'Article {n}')
    article_quantity = 1
    article_price = 10.0
    SKU = factory.Sequence(lambda n: f'SKU{n:03}')


class ShipmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Shipment objects for tests."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for the SQLAlchemyModelFactory.

        - `model`: Specifies the SQLAlchemy model to use (Article or Shipment).
        - `sqlalchemy_session`: Allows injecting a session dynamically at runtime.
        - `sqlalchemy_session_persistence`:
        Determines how session changes are flushed (e.g., 'flush', 'commit').
        """

        model = Shipment
        sqlalchemy_session = None  # 🔑 Allow dynamic session injection
        sqlalchemy_session_persistence = 'flush'

    tracking_number = factory.Sequence(lambda n: f'TN00000{n}')
    carrier = 'DHL'
    sender_address = 'Test Sender'
    receiver_address = '75001 Paris, France'
    status = 'in-transit'

    # pylint: disable=unused-argument
    @factory.post_generation
    def articles(
        self, create: bool, extracted: list[Any] | None, **kwargs: Any
    ) -> None:
        """Post-generation hook to attach Article instances to a Shipment."""
        if not create or not extracted:
            return
        for article in extracted:
            self.articles.append(article)
