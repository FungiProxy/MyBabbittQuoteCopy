"""
Script to test removing ultrasonic and radar products from the database.
First adds a sample ultrasonic product, then removes it.
"""
import sys
import logging
from pathlib import Path

# Add the project root to the Python path so we can import from src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.database import SessionLocal, init_db
from src.core.models import ProductFamily, ProductVariant
from src.core.services.database_populate import remove_obsolete_products

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def add_sample_ultrasonic_product(db):
    """Add a sample ultrasonic product for testing."""
    # First check if it already exists
    existing = db.query(ProductFamily).filter(
        ProductFamily.name == "LRU2000"
    ).first()
    
    if existing:
        print(f"Ultrasonic product family {existing.name} already exists")
        return existing
    
    # Create a new ultrasonic product family
    ultrasonic = ProductFamily(
        name="LRU2000",
        description="ULTRASONIC LEVEL SENSOR",
        category="Ultrasonic Level Sensor"
    )
    
    db.add(ultrasonic)
    db.commit()
    db.refresh(ultrasonic)
    
    # Add a variant
    variant = ProductVariant(
        product_family_id=ultrasonic.id,
        model_number="LRU2000-115VAC",
        description="Ultrasonic level sensor with 115VAC power",
        base_price=1200.0,
        voltage="115VAC"
    )
    
    db.add(variant)
    db.commit()
    
    print(f"Added ultrasonic product family: {ultrasonic.name} - {ultrasonic.description}")
    print(f"Added variant: {variant.model_number}")
    
    return ultrasonic

def list_products(db):
    """List all product families in the database."""
    print("\n=== Product Families ===")
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

def main():
    """Test adding and removing ultrasonic products."""
    # Create database session
    db = SessionLocal()
    
    try:
        # List current products
        print("Before adding ultrasonic product:")
        list_products(db)
        
        # Add a sample ultrasonic product
        add_sample_ultrasonic_product(db)
        
        # List products after adding
        print("\nAfter adding ultrasonic product:")
        list_products(db)
        
        # Remove ultrasonic and radar products
        print("\nRemoving ultrasonic and radar products...")
        remove_obsolete_products(db)
        
        # List products after removal
        print("\nAfter removing ultrasonic products:")
        list_products(db)
        
    finally:
        db.close()

if __name__ == "__main__":
    main() 