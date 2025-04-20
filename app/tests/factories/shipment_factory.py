import factory
from app.models import Shipment, Article


class ArticleFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Article objects for tests."""

    class Meta:
        model = Article
        sqlalchemy_session = None  # 🔑 Allow dynamic session injection
        sqlalchemy_session_persistence = "flush"

    article_name = factory.Sequence(lambda n: f"Article {n}")
    article_quantity = 1
    article_price = 10.0
    SKU = factory.Sequence(lambda n: f"SKU{n:03}")


class ShipmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Shipment objects for tests."""

    class Meta:
        model = Shipment
        sqlalchemy_session = None  # 🔑 Allow dynamic session injection
        sqlalchemy_session_persistence = "flush"

    tracking_number = factory.Sequence(lambda n: f"TN00000{n}")
    carrier = "DHL"
    sender_address = "Test Sender"
    receiver_address = "75001 Paris, France"
    status = "in-transit"

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for article in extracted:
            self.articles.append(article)
