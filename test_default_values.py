#!/usr/bin/env python3
"""
Test script to verify that default values are set for all options.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_default_values():
    """Test that default values are set for all options."""
    
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== TESTING DEFAULT VALUES ===")
        
        # Start configuration for LS2000
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={
                "name": "LS2000", 
                "id": 1, 
                "base_length": 10,
                "material": "S",
                "voltage": "115VAC"
            }
        )
        
        print(f"\n📋 All selected options after configuration:")
        for option_name, value in config_service.current_config.selected_options.items():
            print(f"  {option_name}: {value}")
        
        # Test that we can change just the voltage
        print(f"\n🔄 Changing only voltage to 24VDC...")
        config_service.set_option("Voltage", "24VDC")
        
        print(f"\n📋 Selected options after voltage change:")
        for option_name, value in config_service.current_config.selected_options.items():
            print(f"  {option_name}: {value}")
        
        # Generate model number
        model_number = config_service.generate_model_number()
        print(f"\n🔢 Generated model number: {model_number}")
        
        # Test export data structure
        config_data = {
            'product': 'LS2000',
            'product_id': 1,
            'description': 'LS2000 Level Sensor',
            'unit_price': 785.0,
            'quantity': 1,
            'total_price': 785.0,
            'configuration': config_service.current_config.selected_options,
            'model_number': model_number,
            'config_data': config_service.current_config.selected_options.copy(),
            'options': []
        }
        
        print(f"\n📦 Configuration data for export:")
        print(f"  model_number: {config_data['model_number']}")
        print(f"  config_data keys: {list(config_data['config_data'].keys())}")
        
        # Check specific fields that export needs
        config = config_data['config_data']
        print(f"\n🎯 Export-critical fields:")
        print(f"  Connection Type: {config.get('Connection Type', 'MISSING')}")
        print(f"  Connection Material: {config.get('Connection Material', 'MISSING')}")
        print(f"  Voltage: {config.get('Voltage', 'MISSING')}")
        print(f"  Material: {config.get('Material', 'MISSING')}")
        print(f"  Probe Length: {config.get('Probe Length', 'MISSING')}")
        print(f"  Insulator Material: {config.get('Insulator Material', 'MISSING')}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_default_values() 