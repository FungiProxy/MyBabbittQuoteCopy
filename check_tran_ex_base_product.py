from src.core.database import SessionLocal
from src.core.models.product import Product

db = SessionLocal()
tran_ex_product = db.query(Product).filter(Product.name == "TRAN-EX").first()
if tran_ex_product:
    print(f"TRAN-EX base product found: ID={tran_ex_product.id}, Name={tran_ex_product.name}, Base Price={tran_ex_product.base_price}")
else:
    print("TRAN-EX base product NOT found. You need to create it for the UI to work.")
db.close() 