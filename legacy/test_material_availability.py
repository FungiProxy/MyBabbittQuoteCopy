"""
Test script for material availability functionality.
"""
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.core.models import Product, Material, MaterialAvailability
from src.core.services.product_service import ProductService
from src.core.pricing import calculate_product_price


def test_material_availability():
    """Test material availability for different product types."""
    db = SessionLocal()
    
    try:
        # Get all product types available
        product_types = db.query(MaterialAvailability.product_type).distinct().all()
        product_types = [pt[0] for pt in product_types]
        
        print(f"Found {len(product_types)} product types in the database:")
        for pt in product_types:
            print(f"  - {pt}")
        
        # Test material availability for each product type
        for product_type in product_types:
            print(f"\nMaterial availability for {product_type}:")
            
            # Get available materials
            available_materials = ProductService.get_available_materials_for_product(db, product_type)
            print(f"  Available materials ({len(available_materials)}):")
            for material in available_materials:
                print(f"    - {material.code}: {material.name}")
            
            # Check specific materials
            all_materials = ["S", "H", "U", "T", "TS", "CPVC"]
            for material_code in all_materials:
                is_available = ProductService.is_material_available_for_product(db, material_code, product_type)
                print(f"  Material {material_code} available: {is_available}")
    finally:
        db.close()


def test_pricing_with_material_availability():
    """Test pricing with material availability checks."""
    db = SessionLocal()
    
    try:
        # Define test products - one for each product type we want to test
        test_products = [
            {
                "model_number": "LS2000-115VAC-S-10",
                "description": "Test LS2000 Level Switch",
                "category": "Level Switch",
                "base_price": 425.0,
                "base_length": 10.0,
                "voltage": "115VAC",
                "material": "S"
            },
            {
                "model_number": "LS7000/2-115VAC-H-10",
                "description": "Test LS7000/2 Dual Point Level Switch",
                "category": "Level Switch",
                "base_price": 770.0,
                "base_length": 10.0,
                "voltage": "115VAC",
                "material": "H"
            },
            {
                "model_number": "FS10000-115VAC-S-6",
                "description": "Test FS10000 Flow Switch",
                "category": "Flow Switch",
                "base_price": 1885.0,
                "base_length": 6.0,
                "voltage": "115VAC",
                "material": "S"
            }
        ]
        
        # Create test products if they don't exist
        for product_data in test_products:
            existing_product = db.query(Product).filter(
                Product.model_number == product_data["model_number"]
            ).first()
            
            if not existing_product:
                new_product = Product(**product_data)
                db.add(new_product)
                db.commit()
                print(f"Created test product: {product_data['model_number']}")
        
        # Test pricing for each product type
        for product_type in ["LS2000", "LS7000/2", "FS10000"]:
            # Find a product of this type
            product = db.query(Product).filter(
                Product.model_number.startswith(product_type)
            ).first()
            
            if not product:
                print(f"No product found for type {product_type}")
                continue
            
            print(f"\nTesting {product.model_number} - ${product.base_price:.2f}")
            
            # Test with different materials
            test_materials = ["S", "H", "U", "T"]
            for material_code in test_materials:
                try:
                    # Calculate price with this material
                    price = calculate_product_price(
                        db, product.id, material_override=material_code
                    )
                    print(f"  With {material_code} material: ${price:.2f}")
                except ValueError as e:
                    print(f"  With {material_code} material: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    print("Testing Material Availability")
    print("============================")
    test_material_availability()
    
    print("\nTesting Pricing with Material Availability")
    print("==========================================")
    test_pricing_with_material_availability() 