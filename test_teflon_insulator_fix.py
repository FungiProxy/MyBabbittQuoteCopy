#!/usr/bin/env python3
"""
Test script to verify TEFINS code is properly added to model numbers.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_teflon_insulator_fix():
    """Test that TEFINS code is properly added when Teflon insulator is selected."""
    
    db = SessionLocal()
    product_service = ProductService(db)
    config_service = ConfigurationService(db, product_service)
    
    try:
        # Test LS2000 with TS material and Teflon insulator
        print("--- Test 1: LS2000 with TS material and Teflon insulator ---")
        config_service.start_configuration(
            product_family_id=1,  # LS2000 family ID
            product_family_name="LS2000",
            base_product_info={"name": "LS2000", "id": 1, "base_length": 10}
        )
        
        # Set basic options
        config_service.set_option("Voltage", "115VAC")
        config_service.set_option("Material", "TS")  # Teflon Sleeve
        config_service.set_option("Probe Length", 36)
        config_service.set_option("Connection Type", "Tri-clamp")
        config_service.set_option("Tri-clamp", "1.5\" Tri-clamp Process Connection")
        config_service.set_option("Extra Static Protection", True)
        config_service.set_option("Stainless Steel Tag", True)
        config_service.set_option("Vibration Resistance", True)
        config_service.set_option("Insulator Material", "TEF")  # Teflon insulator
        
        part_number = config_service.generate_model_number()
        print(f"Generated part number: {part_number}")
        
        # Check if TEFINS is included
        if "TEFINS" in part_number:
            print("✅ TEFINS code correctly added for Teflon insulator")
        else:
            print("❌ TEFINS code missing - this is the bug!")
            return False
        
        # Test LS2000 with H material (should auto-select Teflon)
        print("\n--- Test 2: LS2000 with H material (auto-select Teflon) ---")
        config_service.set_option("Material", "H")  # Halar
        config_service.set_option("Insulator Material", "TEF")  # Teflon insulator
        
        part_number = config_service.generate_model_number()
        print(f"Generated part number: {part_number}")
        
        # Check if TEFINS is included
        if "TEFINS" in part_number:
            print("✅ TEFINS code correctly added for H material with Teflon")
        else:
            print("❌ TEFINS code missing for H material!")
            return False
        
        # Test LS2000 with S material and Teflon insulator (should add TEFINS)
        print("\n--- Test 3: LS2000 with S material and Teflon insulator ---")
        config_service.set_option("Material", "S")  # Stainless Steel
        config_service.set_option("Insulator Material", "TEF")  # Teflon insulator
        
        part_number = config_service.generate_model_number()
        print(f"Generated part number: {part_number}")
        
        # Check if TEFINS is included
        if "TEFINS" in part_number:
            print("✅ TEFINS code correctly added for S material with Teflon")
        else:
            print("❌ TEFINS code missing for S material with Teflon!")
            return False
        
        # Test LS2000 with S material and U insulator (base, should NOT add code)
        print("\n--- Test 4: LS2000 with S material and U insulator (base) ---")
        config_service.set_option("Material", "S")  # Stainless Steel
        config_service.set_option("Insulator Material", "U")  # UHMWPE (base)
        
        part_number = config_service.generate_model_number()
        print(f"Generated part number: {part_number}")
        
        # Check that no insulator code is added
        insulator_codes = ["TEFINS", "PEEKINS", "CERINS", "DELINS"]
        for code in insulator_codes:
            if code in part_number:
                print(f"❌ Unexpected insulator code {code} found for base insulator!")
                return False
        
        print("✅ No insulator codes correctly omitted for base insulator")
        
        print("\n🎉 All tests passed! TEFINS code is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_teflon_insulator_fix()
    sys.exit(0 if success else 1) 