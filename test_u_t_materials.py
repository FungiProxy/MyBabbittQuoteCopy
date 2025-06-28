#!/usr/bin/env python3
"""
Test script to debug U and T materials specifically
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_u_t_materials():
    """Test U and T materials specifically"""
    db = SessionLocal()
    product_service = ProductService(db)
    config_service = ConfigurationService(db, product_service)
    
    try:
        print("=== TESTING U AND T MATERIALS ===")
        
        # Test LS2000 with U material
        print("\n--- Testing LS2000 with U material ---")
        
        # Get base product for LS2000
        base_product = product_service.get_base_product_for_family(db, "LS2000")
        print(f"Base product: {base_product}")
        
        # Start configuration with U material
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info=base_product,
            selected_options={"Material": "U"}
        )
        
        print(f"Initial selected options: {config_service.current_config.selected_options}")
        
        # Set length to 8 inches (should trigger length adder)
        config_service.set_option("Length", "8")
        print(f"After setting length: {config_service.current_config.selected_options}")
        
        # Calculate price
        price = config_service.calculate_price()
        print(f"Final price: ${price:.2f}")
        
        # Test LS2000 with T material
        print("\n--- Testing LS2000 with T material ---")
        
        # Start new configuration with T material
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info=base_product,
            selected_options={"Material": "T"}
        )
        
        print(f"Initial selected options: {config_service.current_config.selected_options}")
        
        # Set length to 10 inches (should trigger length adder)
        config_service.set_option("Length", "10")
        print(f"After setting length: {config_service.current_config.selected_options}")
        
        # Calculate price
        price = config_service.calculate_price()
        print(f"Final price: ${price:.2f}")
        
        # Test manual length adder calculation
        print("\n--- Testing manual length adder calculation ---")
        
        # U material at 8 inches
        u_adder = product_service.calculate_length_price("LS2000", "U", 8.0)
        print(f"U material at 8\": ${u_adder:.2f} (should be $160)")
        
        # T material at 10 inches
        t_adder = product_service.calculate_length_price("LS2000", "T", 10.0)
        print(f"T material at 10\": ${t_adder:.2f} (should be $300)")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_u_t_materials() 