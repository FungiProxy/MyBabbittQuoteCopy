from src.core.models.product import Product

print("Product model fields:")
for col in Product.__table__.columns:
    print(f"- {col.name}") 