from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.models.base_model import BaseModel

db = SessionLocal()

# Check Product table
tran_ex_product = db.query(Product).filter(Product.model_number.like("%TRAN-EX%")).first()
if tran_ex_product:
    print(f"Product model number: '{tran_ex_product.model_number}'")
    print(f"Product model number length: {len(tran_ex_product.model_number)}")
    print(f"Product model number bytes: {tran_ex_product.model_number.encode()}")
else:
    print("No TRAN-EX product found")

# Check BaseModel table
tran_ex_basemodel = db.query(BaseModel).filter(BaseModel.model_number.like("%TRAN-EX%")).first()
if tran_ex_basemodel:
    print(f"\nBaseModel model number: '{tran_ex_basemodel.model_number}'")
    print(f"BaseModel model number length: {len(tran_ex_basemodel.model_number)}")
    print(f"BaseModel model number bytes: {tran_ex_basemodel.model_number.encode()}")
else:
    print("\nNo TRAN-EX BaseModel found")

# Test the exact match
test_model = "LS8000/2-TRAN-EX-S-10"
if tran_ex_product:
    print(f"\nTesting exact match with: '{test_model}'")
    print(f"Match result: {tran_ex_product.model_number == test_model}")
    print(f"Contains result: {test_model in tran_ex_product.model_number}")

db.close() 