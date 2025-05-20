"""
Test the pricing module.

This script tests the pricing calculations for various product configurations.
"""
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.core.models import Product, Material
from src.core.pricing import calculate_product_price, calculate_option_price


def test_product_pricing(db: Session):
    """Test product price calculations for various configurations."""
    print("\n=== Product Pricing Tests ===\n")
    
    # Test base prices for each model
    test_models = [
        ("LS2000", "General Purpose Level Switch"),
        ("LS2100", "Loop Powered Level Switch"),
        ("LS6000", "Heavy Duty Level Switch"),
        ("LS7000", "Advanced Features Level Switch"),
        ("LS7000/2", "Dual Point Level Switch"),
        ("LS8000", "Remote Mounted Level Switch"),
        ("LS8000/2", "Remote Mounted Dual Point Level Switch"),
        ("LT9000", "Level Transmitter"),
        ("FS10000", "Flow Switch")
    ]
    
    for model_number, description in test_models:
        # Get product with standard configuration (S material)
        product = db.query(Product).filter(
            Product.model_number.startswith(model_number),
            Product.material == "S"
        ).first()
        
        if product:
            print(f"\nTesting {model_number} - {description}")
            print(f"Base configuration (S material, {product.base_length}\"): ${product.base_price:.2f}")
            
            # Test with longer length
            longer_length = product.base_length + 10
            price = calculate_product_price(db, product.id, longer_length)
            print(f"Extended length ({longer_length}\"): ${price:.2f}")
            
            # Test with different materials
            materials = [
                ("H", "Hastelloy"),
                ("A", "Aluminum"),
                ("T", "Titanium"),
                ("U", "Monel")
            ]
            
            for material_code, material_name in materials:
                try:
                    price = calculate_product_price(
                        db, product.id, material_override=material_code
                    )
                    print(f"{material_name} material: ${price:.2f}")
                except ValueError as e:
                    print(f"{material_name} material: Not available")
        else:
            print(f"\nWarning: {model_number} not found in database")


def test_option_pricing():
    """Test option price calculations."""
    print("\n=== Option Pricing Tests ===\n")
    
    # Test fixed price options
    print("Fixed Price Options:")
    options = [
        ("High Temperature Version", 150.0),
        ("Remote Display", 250.0),
        ("HART Protocol", 300.0),
        ("Modbus RTU", 250.0)
    ]
    
    for name, price in options:
        result = calculate_option_price(price, "fixed")
        print(f"{name} (${price:.2f}): ${result:.2f}")
    
    # Test per-inch options
    print("\nPer-Inch Options (testing with 20\"):")
    per_inch_options = [
        ("Extended Probe", 8.0),  # Standard models
        ("Extended Probe Premium", 12.0)  # Premium models
    ]
    
    for name, price in per_inch_options:
        result = calculate_option_price(price, "per_inch", 20.0)
        print(f"{name} (${price:.2f}/inch × 20\"): ${result:.2f}")
    
    # Test per-foot options
    print("\nPer-Foot Options (testing with 24\" = 2ft):")
    per_foot_options = [
        ("Extended Cable", 5.0),
    ]
    
    for name, price in per_foot_options:
        result = calculate_option_price(price, "per_foot", 24.0)
        print(f"{name} (${price:.2f}/foot × 2ft): ${result:.2f}")


def main():
    """Run pricing module tests."""
    db = SessionLocal()
    
    try:
        test_product_pricing(db)
        test_option_pricing()
        
        print("\nPricing tests complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main() 