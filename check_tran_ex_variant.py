from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.models.product_variant import ProductVariant

db = SessionLocal()

# Check Product table
tran_ex_product = db.query(Product).filter(Product.model_number == "LS8000/2-TRAN-EX-S-10").first()
if tran_ex_product:
    print(f"✓ Product found: ID={tran_ex_product.id}, Model={tran_ex_product.model_number}")
else:
    print("✗ Product not found")
    db.close()
    exit(1)

# Check ProductVariant table
tran_ex_variant = db.query(ProductVariant).filter(ProductVariant.product_id == tran_ex_product.id).first()
if tran_ex_variant:
    print(f"✓ ProductVariant found: ID={tran_ex_variant.id}, Product ID={tran_ex_variant.product_id}")
else:
    print("✗ ProductVariant not found - this is the problem!")
    print("Creating ProductVariant for TRAN-EX...")
    
    # Create the ProductVariant
    new_variant = ProductVariant(
        product_id=tran_ex_product.id,
        model_number=tran_ex_product.model_number,
        description=tran_ex_product.description,
        base_price=tran_ex_product.base_price,
        voltage=tran_ex_product.voltage,
        material=tran_ex_product.material,
        base_length=tran_ex_product.base_length
    )
    db.add(new_variant)
    db.commit()
    print(f"✓ Created ProductVariant: ID={new_variant.id}")

db.close() 