#!/usr/bin/env python3
"""
Test all the new part number codes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_all_codes():
    """Test all the new part number codes."""
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== TESTING ALL NEW CODES ===")
        
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
        
        print(f"Basic: {config_service.generate_model_number()}")
        
        # Test Extra Static Protection
        config_service.set_option("Extra Static Protection", "Yes")
        print(f"With ESP: {config_service.generate_model_number()}")
        
        # Test Bent Probe
        config_service.set_option("Bent Probe", "Yes")
        config_service.set_option("Bent Probe Degree", 45)
        print(f"With Bent Probe: {config_service.generate_model_number()}")
        
        # Test Teflon Insulator
        config_service.set_option("Insulator Material", "Teflon Upgrade")
        print(f"With Teflon: {config_service.generate_model_number()}")
        
        # Test non-standard length with insulator
        config_service.set_option("Probe Length", 15)
        print(f"With non-standard length: {config_service.generate_model_number()}")
        
        # Test Tri-clamp with spud
        config_service.set_option("Connection Type", "Tri-clamp")
        config_service.set_option("Tri-clamp", "1-1/2\" Tri-clamp Spud")
        print(f"With Tri-clamp spud: {config_service.generate_model_number()}")
        
        print("\n=== ALL TESTS COMPLETED ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_all_codes() 