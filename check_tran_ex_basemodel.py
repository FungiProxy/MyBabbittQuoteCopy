from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.models.base_model import BaseModel

db = SessionLocal()

# Check Product table
tran_ex_product = db.query(Product).filter(Product.model_number == "LS8000/2-TRAN-EX-S-10").first()
if tran_ex_product:
    print(f"✓ Product found: ID={tran_ex_product.id}, Model={tran_ex_product.model_number}")
else:
    print("✗ Product not found")
    db.close()
    exit(1)

# Check BaseModel table
tran_ex_basemodel = db.query(BaseModel).filter(BaseModel.id == tran_ex_product.id).first()
if tran_ex_basemodel:
    print(f"✓ BaseModel found: ID={tran_ex_basemodel.id}")
else:
    print("✗ BaseModel not found - this is the problem!")
    print("Creating BaseModel for TRAN-EX...")
    
    # Create the BaseModel
    new_basemodel = BaseModel(
        id=tran_ex_product.id,
        model_number=tran_ex_product.model_number,
        description=tran_ex_product.description,
        base_price=tran_ex_product.base_price,
        voltage=tran_ex_product.voltage,
        material=tran_ex_product.material,
        base_length=tran_ex_product.base_length
    )
    db.add(new_basemodel)
    db.commit()
    print(f"✓ Created BaseModel: ID={new_basemodel.id}")

db.close() 