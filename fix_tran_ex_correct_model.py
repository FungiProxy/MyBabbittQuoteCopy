from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.models.base_model import BaseModel
from src.core.models.product_variant import ProductFamily

db = SessionLocal()

# Check Product table - look for the correct model number
print("=== Checking TRAN-EX Products ===")
tran_ex_products = db.query(Product).filter(Product.model_number.like("%TRAN-EX%")).all()
for product in tran_ex_products:
    print(f"Product: ID={product.id}, Model='{product.model_number}', Price={product.base_price}")

# Check ProductFamily table for TRAN-EX
tran_ex_family = db.query(ProductFamily).filter(ProductFamily.name == "TRAN-EX").first()
if tran_ex_family:
    print(f"\n✓ ProductFamily found: ID={tran_ex_family.id}, Name={tran_ex_family.name}")
else:
    print("\n✗ ProductFamily not found")
    db.close()
    exit(1)

# Check BaseModel table
tran_ex_basemodel = db.query(BaseModel).filter(BaseModel.model_number.like("%TRAN-EX%")).first()
if tran_ex_basemodel:
    print(f"\n✓ BaseModel found: ID={tran_ex_basemodel.id}, Model='{tran_ex_basemodel.model_number}'")
else:
    print("\n✗ BaseModel not found - creating BaseModel for TRAN-EX...")
    
    # Use the first TRAN-EX product we found
    if tran_ex_products:
        tran_ex_product = tran_ex_products[0]
        print(f"Using product: ID={tran_ex_product.id}, Model='{tran_ex_product.model_number}'")
        
        # Create the BaseModel with the correct model number
        new_basemodel = BaseModel(
            id=tran_ex_product.id,
            product_family_id=tran_ex_family.id,
            model_number=tran_ex_product.model_number,  # Use the actual model number from database
            description=tran_ex_product.description,
            base_price=tran_ex_product.base_price,
            voltage=tran_ex_product.voltage,
            material=tran_ex_product.material,
            base_length=tran_ex_product.base_length
        )
        db.add(new_basemodel)
        db.commit()
        print(f"✓ Created BaseModel: ID={new_basemodel.id}, Model='{new_basemodel.model_number}'")
    else:
        print("✗ No TRAN-EX products found")

db.close() 