"""
Script to check the products in the database.
"""
import sys
import logging
from pathlib import Path

# Add the project root to the Python path so we can import from src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.database import SessionLocal
from src.core.models import ProductFamily, ProductVariant

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def check_products():
    """Check products in the database."""
    db = SessionLocal()
    try:
        print("=== Product Families ===")
        families = db.query(ProductFamily).all()
        for family in families:
            print(f"ID: {family.id}, Name: {family.name}, Category: {family.category}")
            print(f"  Description: {family.description}")
            
            variants = db.query(ProductVariant).filter(
                ProductVariant.product_family_id == family.id
            ).all()
            
            print(f"  Variants: {len(variants)}")
            for variant in variants:
                print(f"    - {variant.model_number} (${variant.base_price})")
            
            print()
        
        # Check for any products with "ultrasonic" or "radar" in the name or description
        print("\n=== Checking for Ultrasonic or Radar Products ===")
        ultrasonic_radar = db.query(ProductFamily).filter(
            (ProductFamily.name.ilike("%ultrasonic%")) |
            (ProductFamily.description.ilike("%ultrasonic%")) |
            (ProductFamily.name.ilike("%radar%")) |
            (ProductFamily.description.ilike("%radar%")) |
            (ProductFamily.category.ilike("%ultrasonic%")) |
            (ProductFamily.category.ilike("%radar%"))
        ).all()
        
        if ultrasonic_radar:
            print("Found ultrasonic or radar products:")
            for prod in ultrasonic_radar:
                print(f"  - {prod.name}: {prod.description}")
        else:
            print("No ultrasonic or radar products found in the database.")
    finally:
        db.close()

if __name__ == "__main__":
    check_products() 