import os
import sys

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from src.core.database import get_db
from src.core.models.product_variant import ProductVariant

def update_ls8000_2_price():
    """Update the base price of all LS8000/2 variants to $740."""
    db = next(get_db())
    
    # Get all LS8000/2 variants
    variants = db.query(ProductVariant).filter(
        ProductVariant.model_number.like('LS8000/2%')
    ).all()
    
    # Update base price for each variant
    for variant in variants:
        variant.base_price = 740.0
    
    # Commit changes
    db.commit()
    print(f"Updated base price to $740 for {len(variants)} LS8000/2 variants")

if __name__ == "__main__":
    update_ls8000_2_price() 