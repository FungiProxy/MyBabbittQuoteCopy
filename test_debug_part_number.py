#!/usr/bin/env python3
"""
Simple debug test for part number generation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_debug_part_number():
    """Debug the part number generation."""
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== DEBUG PART NUMBER GENERATION ===")
        
        # Start configuration
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={"name": "LS2000", "id": 1, "base_length": 10}
        )
        
        # Set basic options
        config_service.set_option("Voltage", "115VAC")
        config_service.set_option("Material", "S")
        config_service.set_option("Probe Length", 10)
        
        print(f"Basic part number: {config_service.generate_model_number()}")
        
        # Add Extra Static Protection
        print("\n--- Adding Extra Static Protection ---")
        config_service.set_option("Extra Static Protection", "Yes")
        print(f"Selected options: {config_service.current_config.selected_options}")
        print(f"Part number with ESP: {config_service.generate_model_number()}")
        
        # Add Bent Probe
        print("\n--- Adding Bent Probe ---")
        config_service.set_option("Bent Probe", "Yes")
        config_service.set_option("Bent Probe Degree", 45)
        print(f"Selected options: {config_service.current_config.selected_options}")
        print(f"Part number with bent probe: {config_service.generate_model_number()}")
        
        # Add 3/4" Diameter Probe
        print("\n--- Adding 3/4\" Diameter Probe ---")
        config_service.set_option('3/4" Diameter Probe', "Yes")
        print(f"Selected options: {config_service.current_config.selected_options}")
        print(f"Part number with 3/4OD: {config_service.generate_model_number()}")
        
        # Add Teflon Insulator
        print("\n--- Adding Teflon Insulator ---")
        config_service.set_option("Insulator Material", "Teflon Upgrade")
        print(f"Selected options: {config_service.current_config.selected_options}")
        print(f"Part number with teflon: {config_service.generate_model_number()}")
        
        print("\n=== END DEBUG ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_debug_part_number() 