from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.models.base_model import BaseModel
from src.core.models.product_variant import ProductFamily

db = SessionLocal()

# Check Product table
tran_ex_product = db.query(Product).filter(Product.model_number == "LS8000/2-TRAN-EX-S-10").first()
if tran_ex_product:
    print(f"✓ Product found: ID={tran_ex_product.id}, Model={tran_ex_product.model_number}")
else:
    print("✗ Product not found")
    db.close()
    exit(1)

# Check ProductFamily table for TRAN-EX
tran_ex_family = db.query(ProductFamily).filter(ProductFamily.name == "TRAN-EX").first()
if tran_ex_family:
    print(f"✓ ProductFamily found: ID={tran_ex_family.id}, Name={tran_ex_family.name}")
else:
    print("✗ ProductFamily not found - creating TRAN-EX family...")
    tran_ex_family = ProductFamily(
        name="TRAN-EX",
        description="TRAN-EX Probe for LS8000/2 family",
        category="Multi-Point Level Switch"
    )
    db.add(tran_ex_family)
    db.commit()
    print(f"✓ Created ProductFamily: ID={tran_ex_family.id}")

# Check BaseModel table
tran_ex_basemodel = db.query(BaseModel).filter(BaseModel.id == tran_ex_product.id).first()
if tran_ex_basemodel:
    print(f"✓ BaseModel found: ID={tran_ex_basemodel.id}")
else:
    print("✗ BaseModel not found - creating BaseModel for TRAN-EX...")
    
    # Create the BaseModel with proper product_family_id
    new_basemodel = BaseModel(
        id=tran_ex_product.id,
        product_family_id=tran_ex_family.id,
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