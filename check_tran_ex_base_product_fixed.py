from src.core.database import SessionLocal
from src.core.models.product import Product

db = SessionLocal()
# Try using model_number or another identifying field if 'name' does not exist
tran_ex_product = db.query(Product).filter(Product.model_number.like("%TRAN-EX%")).first()
if tran_ex_product:
    print(f"TRAN-EX base product found: ID={tran_ex_product.id}, Model Number={tran_ex_product.model_number}, Base Price={tran_ex_product.base_price}")
else:
    print("TRAN-EX base product NOT found. You need to create it for the UI to work.")
db.close() 