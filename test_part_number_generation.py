#!/usr/bin/env python3
"""
Test script to verify the new part number generation logic.
This script tests the updated generate_model_number method that includes
all additional options in the part number format.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_part_number_generation():
    """Test the new part number generation logic."""
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        # Test 1: Basic configuration (LS2000-1115VAC-S-10")
        print("Test 1: Basic configuration")
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={"name": "LS2000", "id": 1, "base_length": 10}
        )
        config_service.set_option("Voltage", "115VAC")
        config_service.set_option("Material", "S")
        config_service.set_option("Probe Length", 10)
        
        part_number = config_service.generate_model_number()
        print(f"Expected: LS2000-115VAC-S-10\"")
        print(f"Actual:   {part_number}")
        print()
        
        # Test 2: With process connection (LS2000-1115VAC-S-10"-2"150#)
        print("Test 2: With process connection")
        config_service.set_option("Connection Type", "Flange")
        config_service.set_option("Flange Size", "2")
        config_service.set_option("Flange Rating", "150#")
        
        part_number = config_service.generate_model_number()
        print(f"Expected: LS2000-115VAC-S-10\"-2\"150#")
        print(f"Actual:   {part_number}")
        print()
        
        # Test 3: With additional options (LS2000-1115VAC-S-10"-2"150#-TEFINS-3/4OD)
        print("Test 3: With additional options")
        config_service.set_option("Insulator Material", "Teflon Upgrade")
        config_service.set_option("O-Rings", "PTFE")
        
        part_number = config_service.generate_model_number()
        print(f"Expected: LS2000-115VAC-S-10\"-2\"150#-TEFINS-PTFEOR")
        print(f"Actual:   {part_number}")
        print()
        
        # Test 4: With exotic metal
        print("Test 4: With exotic metal")
        config_service.set_option("Exotic Metal", "Titanium")
        
        part_number = config_service.generate_model_number()
        print(f"Expected: LS2000-115VAC-S-10\"-2\"150#-TEFINS-PTFEOR-TI")
        print(f"Actual:   {part_number}")
        print()
        
        # Test 5: With accessories
        print("Test 5: With accessories")
        config_service.set_option("Extra Static Protection", "Yes")
        config_service.set_option("Stainless Steel Tag", "Yes")
        
        part_number = config_service.generate_model_number()
        print(f"Expected: LS2000-115VAC-S-10\"-2\"150#-TEFINS-PTFEOR-TI-ESP-SSTAG")
        print(f"Actual:   {part_number}")
        print()
        
        # Test 6: Tri-clamp connection
        print("Test 6: Tri-clamp connection")
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={"name": "LS2000", "id": 1, "base_length": 10}
        )
        config_service.set_option("Voltage", "115VAC")
        config_service.set_option("Material", "S")
        config_service.set_option("Probe Length", 10)
        config_service.set_option("Connection Type", "Tri-clamp")
        config_service.set_option("Tri-clamp", "2\" Tri-clamp Process Connection")
        
        part_number = config_service.generate_model_number()
        print(f"Expected: LS2000-115VAC-S-10\"-2TC")
        print(f"Actual:   {part_number}")
        print()
        
        # Test 7: NPT connection
        print("Test 7: NPT connection")
        config_service.set_option("Connection Type", "NPT")
        config_service.set_option("NPT Size", "3/4")
        
        part_number = config_service.generate_model_number()
        print(f"Expected: LS2000-115VAC-S-10\"-3/4\"NPT")
        print(f"Actual:   {part_number}")
        print()
        
        print("✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_part_number_generation() 