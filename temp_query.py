from src.core.database import SessionLocal
from src.core.models import ProductFamily

db = SessionLocal()
families = db.query(ProductFamily).all()
print("Product Families in database:")
for f in families:
    print(f" - {f.name}: {f.description} ({f.category})")
db.close() 