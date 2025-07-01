#!/usr/bin/env python3
"""
Simple test to verify the additional options functionality in part number generation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def test_additional_options():
    """Test the additional options functionality."""
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        # Start with basic configuration
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={"name": "LS2000", "id": 1, "base_length": 10}
        )
        config_service.set_option("Voltage", "115VAC")
        config_service.set_option("Material", "S")
        config_service.set_option("Probe Length", 10)
        
        # Test basic part number
        part_number = config_service.generate_model_number()
        print(f"Basic: {part_number}")
        
        # Add process connection
        config_service.set_option("Connection Type", "Flange")
        config_service.set_option("Flange Size", "2")
        config_service.set_option("Flange Rating", "150#")
        
        part_number = config_service.generate_model_number()
        print(f"With flange: {part_number}")
        
        # Add insulator material
        config_service.set_option("Insulator Material", "Teflon Upgrade")
        
        part_number = config_service.generate_model_number()
        print(f"With teflon insulator: {part_number}")
        
        # Add O-rings
        config_service.set_option("O-Rings", "PTFE")
        
        part_number = config_service.generate_model_number()
        print(f"With PTFE O-rings: {part_number}")
        
        # Add exotic metal
        config_service.set_option("Exotic Metal", "Titanium")
        
        part_number = config_service.generate_model_number()
        print(f"With titanium: {part_number}")
        
        # Add accessories
        config_service.set_option("Extra Static Protection", "Yes")
        config_service.set_option("Stainless Steel Tag", "Yes")
        
        part_number = config_service.generate_model_number()
        print(f"With accessories: {part_number}")
        
        print("✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_additional_options() 