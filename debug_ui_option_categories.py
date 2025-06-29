from src.core.services.product_service import ProductService
from src.core.database import SessionLocal

db = SessionLocal()
service = ProductService(db)

family_name = "TRAN-EX"
options = service.get_additional_options(db, family_name)
print(f"[UI DEBUG] All option categories for TRAN-EX:")
for opt in options:
    print(f"NAME: {opt.get('name')} | CATEGORY: {opt.get('category')} | CHOICES: {opt.get('choices')}")
db.close() 