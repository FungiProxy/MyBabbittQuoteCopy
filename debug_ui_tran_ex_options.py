from src.core.services.product_service import ProductService
from src.core.database import SessionLocal

db = SessionLocal()
service = ProductService(db)

family_name = "TRAN-EX"
options = service.get_additional_options(db, family_name)
print(f"[UI DEBUG] Options received for TRAN-EX: {[opt.get('name') for opt in options]}")
for opt in options:
    print(f"[UI DEBUG] Option: {opt.get('name')} | Category: {opt.get('category')} | Choices: {opt.get('choices')}")
db.close() 