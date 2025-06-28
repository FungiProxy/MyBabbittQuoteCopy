#!/usr/bin/env python3
"""
Test script to verify O-ring pricing functionality
"""

import sys
import logging
from PySide6.QtWidgets import QApplication

# Set up logging to see debug output
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Test O-ring pricing
from src.core.database import SessionLocal
from src.core.models import Option
from src.core.pricing import PricingContext, calculate_product_price
from src.core.models import BaseModel, Material

def test_oring_pricing():
    """Test O-ring material pricing"""
    print("=== TESTING O-RING PRICING ===")
    
    with SessionLocal() as db:
        # Get O-ring options from database
        o_ring_options = db.query(Option).filter(
            Option.name == "O-Rings",
            Option.category == "O-ring Material"
        ).all()
        
        print(f"Found {len(o_ring_options)} O-ring options:")
        for option in o_ring_options:
            print(f"  - {option.name} ({option.category})")
            print(f"    Product families: {option.product_families}")
            print(f"    Choices: {option.choices}")
            print(f"    Adders: {option.adders}")
            print()
        
        # Test with a specific product (LS2000)
        base_model = db.query(BaseModel).filter(
            BaseModel.model_number.like("LS2000%")
        ).first()
        
        if not base_model:
            print("No LS2000 base model found for testing")
            return
        
        print(f"Testing with base model: {base_model.model_number}")
        print(f"Base price: ${base_model.base_price}")
        
        # Test pricing with different O-ring materials
        test_materials = ["Viton", "Kalrez"]
        
        for o_ring_material in test_materials:
            print(f"\n--- Testing {o_ring_material} O-ring ---")
            
            # Create pricing context
            context = PricingContext(
                db=db,
                product_id=base_model.id,
                length_in=10.0,
                material_override_code="S",
                specs={
                    "O-Rings": o_ring_material
                }
            )
            
            try:
                # Calculate price
                final_price = calculate_product_price(context)
                print(f"Final price with {o_ring_material}: ${final_price:.2f}")
                
                # Calculate expected adder
                expected_adder = 0
                for option in o_ring_options:
                    if option.product_families and "LS2000" in option.product_families:
                        if option.adders and o_ring_material in option.adders:
                            expected_adder = option.adders[o_ring_material]
                            break
                
                print(f"Expected {o_ring_material} adder: ${expected_adder}")
                print(f"Price difference: ${final_price - base_model.base_price:.2f}")
                
            except Exception as e:
                print(f"Error calculating price for {o_ring_material}: {e}")

if __name__ == "__main__":
    test_oring_pricing() 