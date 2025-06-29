# This script demonstrates the logic you should add to your product selection dialog or configuration widget.
# It ensures that when the TRAN-EX family is selected, the correct base product is used.

from src.core.database import SessionLocal
from src.core.models.product import Product
from src.core.services.product_service import ProductService

db = SessionLocal()
product_service = ProductService(db)

def get_base_product_for_family_patched(family_name):
    if family_name == "TRAN-EX":
        # Hardcode the correct model number for TRAN-EX
        base_product = db.query(Product).filter(Product.model_number == "LS8000/2-TRAN-EX-S-10").first()
        if base_product:
            print(f"[PATCH] Using TRAN-EX base product: {base_product.model_number} (ID: {base_product.id})")
        else:
            print("[PATCH] TRAN-EX base product not found!")
        return base_product
    else:
        return product_service.get_base_product_for_family(db, family_name)

# Example usage:
family_name = "TRAN-EX"
base_product = get_base_product_for_family_patched(family_name)
if base_product:
    print(f"Base product for {family_name}: {base_product.model_number} (ID: {base_product.id})")
else:
    print(f"No base product found for {family_name}")

db.close() 