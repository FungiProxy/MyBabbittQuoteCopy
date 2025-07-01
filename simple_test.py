#!/usr/bin/env python3
"""
Very simple test to debug option setting.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def simple_test():
    """Simple test to see what's happening."""
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== SIMPLE TEST ===")
        
        # Start configuration
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={"name": "LS2000", "id": 1, "base_length": 10}
        )
        
        print(f"Initial selected options: {config_service.current_config.selected_options}")
        
        # Try to set Extra Static Protection
        print("\nSetting Extra Static Protection to Yes...")
        config_service.set_option("Extra Static Protection", "Yes")
        print(f"After setting ESP: {config_service.current_config.selected_options}")
        
        # Generate part number
        part_number = config_service.generate_model_number()
        print(f"Part number: {part_number}")
        
        # Check what options are available for LS2000
        print("\nAvailable options for LS2000:")
        options = config_service.get_available_options("LS2000")
        for option in options:
            print(f"  - {option['name']}: {option['choices']}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    simple_test() 