#!/usr/bin/env python3
"""
Test script to verify that flange and tri-clamp connection codes are properly added to the part number.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_connection_codes():
    """Test that connection codes are properly added to part numbers."""
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== TESTING CONNECTION CODES ===")
        
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
        
        # Test 1: NPT Connection
        print("\n--- Test 1: NPT Connection ---")
        config_service.set_option("Connection Type", "NPT")
        config_service.set_option("NPT Size", "3/4")
        part_number = config_service.generate_model_number()
        print(f"With NPT connection: {part_number}")
        assert '3/4"NPT' in part_number, f"Expected 3/4\"NPT in part number, got: {part_number}"
        print("✅ NPT connection code correctly added")
        
        # Test 2: Flange Connection
        print("\n--- Test 2: Flange Connection ---")
        config_service.set_option("Connection Type", "Flange")
        config_service.set_option("Flange Size", "2")
        config_service.set_option("Flange Rating", "150#")
        part_number = config_service.generate_model_number()
        print(f"With Flange connection: {part_number}")
        assert '2"150#' in part_number, f"Expected 2\"150# in part number, got: {part_number}"
        print("✅ Flange connection code correctly added")
        
        # Test 3: Tri-clamp Connection (2")
        print("\n--- Test 3: Tri-clamp Connection (2\") ---")
        config_service.set_option("Connection Type", "Tri-clamp")
        config_service.set_option("Tri-clamp", "2\" Tri-clamp Process Connection")
        part_number = config_service.generate_model_number()
        print(f"With Tri-clamp connection: {part_number}")
        assert 'TC2"' in part_number, f"Expected TC2\" in part number, got: {part_number}"
        print("✅ Tri-clamp connection code correctly added")
        
        # Test 4: Tri-clamp Connection (1-1/2")
        print("\n--- Test 4: Tri-clamp Connection (1-1/2\") ---")
        config_service.set_option("Tri-clamp", "1-1/2\" Tri-clamp Process Connection")
        part_number = config_service.generate_model_number()
        print(f"With Tri-clamp connection: {part_number}")
        assert 'TC1-1/2"' in part_number, f"Expected TC1-1/2\" in part number, got: {part_number}"
        print("✅ Tri-clamp connection code correctly added")
        
        # Test 5: Tri-clamp with Spud
        print("\n--- Test 5: Tri-clamp with Spud ---")
        config_service.set_option("Tri-clamp", "2\" Tri-clamp Spud Process Connection")
        part_number = config_service.generate_model_number()
        print(f"With Tri-clamp Spud connection: {part_number}")
        assert 'TC2"SPD' in part_number, f"Expected TC2\"SPD in part number, got: {part_number}"
        print("✅ Tri-clamp Spud connection code correctly added")
        
        # Test 6: No connection type
        print("\n--- Test 6: No connection type ---")
        config_service.set_option("Connection Type", "")
        part_number = config_service.generate_model_number()
        print(f"With no connection type: {part_number}")
        # Should not contain any connection codes
        connection_codes = ['NPT', '150#', 'TC']
        for code in connection_codes:
            assert code not in part_number, f"Unexpected connection code {code} in part number: {part_number}"
        print("✅ No connection codes when no connection type selected")
        
        print("\n=== ALL TESTS PASSED ===")
        print("✅ Connection codes working correctly!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_connection_codes() 