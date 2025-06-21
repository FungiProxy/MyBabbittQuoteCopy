#!/usr/bin/env python3
"""
Test script to verify the new option arrangement in ConfigurationWizard.
"""

import sys
import logging
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_new_arrangement():
    """Test the new option arrangement."""
    print("=== Testing New Option Arrangement ===")
    
    db = SessionLocal()
    product_service = ProductService()
    
    try:
        # Test with LS2000
        family_name = "LS2000"
        print(f"\nTesting arrangement for {family_name}")
        
        # Get all options
        additional_options = product_service.get_additional_options(db, family_name)
        print(f"Total options found: {len(additional_options)}")
        
        # Test the new categorization logic
        print("\n1. Core Configuration Options:")
        # Get voltage from additional_options instead of get_available_voltages
        voltage_options = [opt for opt in additional_options if opt.get('name') == 'Voltage']
        voltage_choices = []
        if voltage_options:
            voltage_choices = voltage_options[0].get('choices', [])
        
        materials = product_service.get_available_materials_for_product(db, family_name)
        print(f"  - Voltages: {voltage_choices}")
        print(f"  - Materials: {len(materials)} options")
        print(f"  - Length: Manual input (6-120 inches)")
        
        print("\n2. Connection Options:")
        connection_options = [
            opt for opt in additional_options 
            if opt.get('category') in ['Connections', 'Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator Material', 'Insulator Length']
        ]
        for opt in connection_options:
            print(f"  - {opt.get('name')}: {opt.get('category')}")
        
        print("\n3. Accessories:")
        accessory_options = [
            opt for opt in additional_options 
            if opt.get('category') in ['O-ring Material', 'Accessories']
        ]
        for opt in accessory_options:
            print(f"  - {opt.get('name')}: {opt.get('category')}")
        
        print("\n4. Special Features:")
        special_options = [
            opt for opt in additional_options 
            if opt.get('category') not in ['Material', 'Voltage', 'Connections', 'Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator Material', 'Insulator Length', 'O-ring Material', 'Accessories']
        ]
        for opt in special_options:
            print(f"  - {opt.get('name')}: {opt.get('category')}")
        
        # Verify all options are accounted for
        total_categorized = len(connection_options) + len(accessory_options) + len(special_options)
        print(f"\nVerification:")
        print(f"  - Total options: {len(additional_options)}")
        print(f"  - Categorized options: {total_categorized}")
        print(f"  - Core options (Voltage, Material, Length): 3")
        print(f"  - All accounted for: {total_categorized + 3 == len(additional_options) + 3}")
        
    except Exception as e:
        print(f"Error in arrangement test: {e}")
        logger.exception("Arrangement test failed")
    finally:
        db.close()

def main():
    """Run the arrangement test."""
    print("New Option Arrangement Test")
    print("=" * 50)
    
    test_new_arrangement()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main() 