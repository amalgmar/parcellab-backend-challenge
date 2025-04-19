from sqlalchemy.exc import SQLAlchemyError
from app.models import Shipment, Article
from app.db import SessionLocal


def seed_data():
    db = SessionLocal()
    print("🔍 Starting DB seeding...")

    try:
        if db.query(Shipment).filter(Shipment.tracking_number == "TN12345678").first():
            print("⚠️  Sample data already exists. Skipping seeding.")
            return

        s1 = Shipment(
            tracking_number="TN12345678",
            carrier="DHL",
            sender_address="Street 1, 10115 Berlin, Germany",
            receiver_address="Street 10, 75001 Paris, France",
            status="in-transit",
        )
        s1.articles = [
            Article(article_name="Laptop", article_quantity=1, article_price=800, SKU="LP123"),
            Article(article_name="Mouse", article_quantity=1, article_price=25, SKU="MO456"),
        ]

        s2 = Shipment(
            tracking_number="TN12345680",
            carrier="DPD",
            sender_address="Street 3, 80331 Munich, Germany",
            receiver_address="Street 5, 28013 Madrid, Spain",
            status="delivery",
        )
        s2.articles = [
            Article(article_name="Keyboard", article_quantity=1, article_price=50, SKU="KB012"),
            Article(article_name="Mouse", article_quantity=1, article_price=25, SKU="MO456"),
        ]

        # ✅ Use default transactional behavior
        db.add_all([s1, s2])
        db.commit()
        print("✅ Seeded sample shipments and articles.")

    except SQLAlchemyError as e:
        db.rollback()
        print("❌ Seed failed. Rolled back.")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    try:
        seed_data()
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        import traceback

        traceback.print_exc()
