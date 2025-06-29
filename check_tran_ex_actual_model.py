from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.models.base_model import BaseModel
from src.core.models.product_variant import ProductFamily

db = SessionLocal()

# Check all TRAN-EX related products
print("=== TRAN-EX Products ===")
tran_ex_products = db.query(Product).filter(Product.model_number.like("%TRAN-EX%")).all()
for product in tran_ex_products:
    print(f"Product: ID={product.id}, Model={product.model_number}, Price={product.base_price}")

print("\n=== TRAN-EX ProductFamily ===")
tran_ex_family = db.query(ProductFamily).filter(ProductFamily.name == "TRAN-EX").first()
if tran_ex_family:
    print(f"ProductFamily: ID={tran_ex_family.id}, Name={tran_ex_family.name}")

print("\n=== TRAN-EX BaseModel ===")
tran_ex_basemodel = db.query(BaseModel).filter(BaseModel.model_number.like("%TRAN-EX%")).first()
if tran_ex_basemodel:
    print(f"BaseModel: ID={tran_ex_basemodel.id}, Model={tran_ex_basemodel.model_number}")

print("\n=== All TRAN-EX related records ===")
# Check if there are any other TRAN-EX records
all_tran_ex = db.query(Product).filter(Product.description.like("%TRAN-EX%")).all()
for product in all_tran_ex:
    print(f"Product: ID={product.id}, Model={product.model_number}, Description={product.description}")

db.close() 