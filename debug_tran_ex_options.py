from src.core.services.product_service import ProductService
from src.core.database import SessionLocal

db = SessionLocal()
service = ProductService(db)

family_name = "TRAN-EX"
print(f"[DEBUG] Loading options for family: {family_name}")
options = service.get_additional_options(db, family_name)
print(f"[DEBUG] Options loaded: {[opt.get('name') for opt in options]}")
db.close() 