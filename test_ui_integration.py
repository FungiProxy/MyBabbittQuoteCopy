#!/usr/bin/env python3
"""
Test UI integration with configuration service to verify part number updates.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_ui_integration():
    """Test UI integration with configuration service."""
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== TESTING UI INTEGRATION ===")
        
        # Start configuration
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={
                "name": "LS2000",
                "id": 1,
                "base_price": 425.0,
                "model_number": "LS2000-115VAC-S-10",
                "base_length": 10,
                "voltage": "115VAC",
                "material": "S"
            },
            selected_options={}
        )
        
        print(f"Initial part number: {config_service.generate_model_number()}")
        
        # Test setting Extra Static Protection
        print("\n--- Testing Extra Static Protection ---")
        config_service.set_option("Extra Static Protection", "Yes")
        print(f"After setting Extra Static Protection: {config_service.generate_model_number()}")
        
        # Test setting Bent Probe
        print("\n--- Testing Bent Probe ---")
        config_service.set_option("Bent Probe", "Yes")
        config_service.set_option("Bent Probe Degree", 45)
        print(f"After setting Bent Probe 45 degrees: {config_service.generate_model_number()}")
        
        # Test setting 3/4" Diameter Probe
        print("\n--- Testing 3/4\" Diameter Probe ---")
        config_service.set_option("3/4\" Diameter Probe", "Yes")
        print(f"After setting 3/4\" Diameter Probe: {config_service.generate_model_number()}")
        
        # Test setting Insulator Material
        print("\n--- Testing Insulator Material ---")
        config_service.set_option("Insulator Material", "Teflon Upgrade")
        print(f"After setting Insulator Material: {config_service.generate_model_number()}")
        
        # Test setting Tri-clamp with spud
        print("\n--- Testing Tri-clamp with Spud ---")
        config_service.set_option("Connection Type", "Tri-clamp")
        config_service.set_option("Tri-clamp", "1-1/2\" Spud")
        print(f"After setting Tri-clamp with Spud: {config_service.generate_model_number()}")
        
        # Test all together
        print("\n--- Testing All Options Together ---")
        config_service.set_option("Extra Static Protection", "Yes")
        config_service.set_option("Bent Probe", "Yes")
        config_service.set_option("Bent Probe Degree", 45)
        config_service.set_option("3/4\" Diameter Probe", "Yes")
        config_service.set_option("Insulator Material", "Teflon Upgrade")
        config_service.set_option("Connection Type", "Tri-clamp")
        config_service.set_option("Tri-clamp", "1-1/2\" Spud")
        print(f"Final part number with all options: {config_service.generate_model_number()}")
        
        print("\n=== UI INTEGRATION TEST COMPLETE ===")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_ui_integration() 