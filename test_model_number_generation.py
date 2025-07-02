#!/usr/bin/env python3
"""
Test script to verify model number generation logic.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService
from src.core.config.base_models import get_base_model

def test_model_number_generation():
    """Test the model number generation logic."""
    
    db = SessionLocal()
    try:
        product_service = ProductService(db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== TESTING MODEL NUMBER GENERATION ===\n")
        
        # Test cases for different product families
        test_cases = [
            "LS2000",
            "LS2100", 
            "LS6000",
            "LS7000",
            "LS8000",
            "LT9000",
            "FS10000"
        ]
        
        for family in test_cases:
            print(f"Testing {family}:")
            
            # Get base model info
            base_model = get_base_model(family)
            base_model_number = base_model.get("model_number", "")
            print(f"  Base model number: {base_model_number}")
            
            # Start configuration with base defaults
            config_service.start_configuration(
                product_family_id=1,  # Dummy ID
                product_family_name=family,
                base_product_info={
                    'id': 1,
                    'name': family,
                    'base_length': base_model.get('base_length', 10),
                    'voltage': base_model.get('voltage', '115VAC'),
                    'material': base_model.get('material', 'S'),
                },
                selected_options={
                    'Voltage': base_model.get('voltage', '115VAC'),
                    'Material': base_model.get('material', 'S'),
                    'Probe Length': base_model.get('base_length', 10),
                }
            )
            
            # Generate model number
            generated_number = config_service.generate_model_number()
            print(f"  Generated number: {generated_number}")
            
            # Check if they match
            if generated_number == base_model_number:
                print(f"  ✓ PASS: Generated number matches base model")
            else:
                print(f"  ✗ FAIL: Generated number does not match base model")
            
            print()
        
        # Test with non-base options
        print("=== TESTING WITH NON-BASE OPTIONS ===\n")
        
        # Test LS2000 with different material
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={
                'id': 1,
                'name': 'LS2000',
                'base_length': 10,
                'voltage': '115VAC',
                'material': 'S',
            },
            selected_options={
                'Voltage': '115VAC',
                'Material': 'H',  # Changed from base 'S' to 'H'
                'Probe Length': 10,
            }
        )
        
        generated_with_changes = config_service.generate_model_number()
        print(f"LS2000 with Material=H: {generated_with_changes}")
        print(f"Expected: LS2000-115VAC-H-10\"")
        print(f"✓ PASS: {generated_with_changes == 'LS2000-115VAC-H-10\"'}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_model_number_generation() 