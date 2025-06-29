from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.services.product_service import ProductService

db = SessionLocal()
product_service = ProductService(db)

# Test TRAN-EX selection
print("=== Testing TRAN-EX Selection ===")

# Check if TRAN-EX product exists
tran_ex_product = db.query(Product).filter(Product.model_number == "LS8000/2-TRAN-EX-S-10").first()
if tran_ex_product:
    print(f"✓ TRAN-EX product found: ID={tran_ex_product.id}, Model={tran_ex_product.model_number}")
else:
    print("✗ TRAN-EX product not found")
    db.close()
    exit(1)

# Test getting base product for TRAN-EX family
base_product = product_service.get_base_product_for_family(db, "TRAN-EX")
if base_product:
    print(f"✓ Base product for TRAN-EX: {base_product}")
else:
    print("✗ No base product found for TRAN-EX")

# Test getting materials for TRAN-EX
materials = product_service.get_available_materials_for_product(db, "TRAN-EX")
if materials:
    print(f"✓ Materials for TRAN-EX: {len(materials)} options")
    for mat in materials:
        print(f"  - {mat.get('name', 'Unknown')}: {mat.get('choices', [])}")
else:
    print("✗ No materials found for TRAN-EX")

# Test getting voltages for TRAN-EX
voltages = product_service.get_available_voltages(db, "TRAN-EX")
if voltages:
    print(f"✓ Voltages for TRAN-EX: {voltages}")
else:
    print("✗ No voltages found for TRAN-EX")

# Test getting additional options for TRAN-EX
additional_options = product_service.get_additional_options(db, "TRAN-EX")
if additional_options:
    print(f"✓ Additional options for TRAN-EX: {len(additional_options)} options")
    for opt in additional_options:
        print(f"  - {opt.get('name', 'Unknown')}: {opt.get('category', 'Unknown')}")
else:
    print("✗ No additional options found for TRAN-EX")

db.close() 