"""
Script to remove ultrasonic and radar products from the database.
"""
import sys
import logging
from pathlib import Path

# Add the project root to the Python path so we can import from src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.database import SessionLocal
from src.core.models import ProductFamily, ProductVariant
from src.core.services.database_init import initialize_database_if_needed
from src.core.services.database_populate import remove_obsolete_products

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    """Remove ultrasonic and radar products."""
    # Make sure database exists
    initialize_database_if_needed()
    
    # Create database session
    db = SessionLocal()
    try:
        # First, check for any ultrasonic or radar products
        print("\n=== Before Removal: Checking for Ultrasonic or Radar Products ===")
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
                
            # Now remove the obsolete products
            print("\n=== Removing Obsolete Products ===")
            remove_obsolete_products(db)
            
            # Check again after removal
            print("\n=== After Removal: Checking for Ultrasonic or Radar Products ===")
            remaining = db.query(ProductFamily).filter(
                (ProductFamily.name.ilike("%ultrasonic%")) |
                (ProductFamily.description.ilike("%ultrasonic%")) |
                (ProductFamily.name.ilike("%radar%")) |
                (ProductFamily.description.ilike("%radar%")) |
                (ProductFamily.category.ilike("%ultrasonic%")) |
                (ProductFamily.category.ilike("%radar%"))
            ).all()
            
            if remaining:
                print("Still found ultrasonic or radar products after removal:")
                for prod in remaining:
                    print(f"  - {prod.name}: {prod.description}")
            else:
                print("All ultrasonic and radar products have been successfully removed.")
        else:
            print("No ultrasonic or radar products found in the database. Nothing to remove.")
    finally:
        db.close()

if __name__ == "__main__":
    main() 