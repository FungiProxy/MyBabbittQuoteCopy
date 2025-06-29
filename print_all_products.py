from src.core.database import SessionLocal
from src.core.models.product import Product

db = SessionLocal()
products = db.query(Product).all()
for p in products:
    print(f"ID: {p.id} | Model Number: {p.model_number} | Description: {p.description}")
db.close() 