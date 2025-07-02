#!/usr/bin/env python3
"""
Test script to verify the fixes for model number generation and pricing issues.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService
from PySide6.QtWidgets import QApplication
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog

def test_ls2000_base_model():
    """Test LS2000 base model configuration."""
    print("=== Testing LS2000 Base Model ===")
    
    db = SessionLocal()
    product_service = ProductService(db)
    config_service = ConfigurationService(db, product_service)
    
    # Start configuration for LS2000
    config_service.start_configuration(
        product_family_id=1,
        product_family_name="LS2000",
        base_product_info={
            "id": 1,
            "model_number": 'LS2000-115VAC-S-10"',
            "base_price": 425.0,
            "base_length": 10.0,
            "voltage": "115VAC",
            "material": "S"
        }
    )
    
    # Check initial model number (should be base model)
    initial_model = config_service.generate_model_number()
    print(f"Initial model number: {initial_model}")
    
    # Check initial price (should be base price)
    initial_price = config_service.get_final_price()
    print(f"Initial price: ${initial_price:.2f}")
    
    # Verify base model values are set correctly
    selected_options = config_service.current_config.selected_options
    print(f"Selected options: {selected_options}")
    
    # Test that voltage is set to base model value
    voltage = selected_options.get("Voltage")
    print(f"Voltage: {voltage} (expected: 115VAC)")
    
    # Test that material is set to base model value
    material = selected_options.get("Material")
    print(f"Material: {material} (expected: S)")
    
    # Test that probe length is set to base model value
    probe_length = selected_options.get("Probe Length")
    print(f"Probe Length: {probe_length} (expected: 10)")
    
    # Test that model number matches base model
    expected_model = 'LS2000-115VAC-S-10"'
    if initial_model == expected_model:
        print("✓ Model number matches base model")
    else:
        print(f"✗ Model number mismatch: expected {expected_model}, got {initial_model}")
    
    # Test that price matches base price
    expected_price = 425.0
    if abs(initial_price - expected_price) < 0.01:
        print("✓ Price matches base price")
    else:
        print(f"✗ Price mismatch: expected ${expected_price}, got ${initial_price}")
    
    db.close()

def test_accessory_pricing():
    """Test accessory pricing with 'No' values."""
    print("\n=== Testing Accessory Pricing ===")
    
    db = SessionLocal()
    product_service = ProductService(db)
    config_service = ConfigurationService(db, product_service)
    
    # Start configuration for LS2000
    config_service.start_configuration(
        product_family_id=1,
        product_family_name="LS2000",
        base_product_info={
            "id": 1,
            "model_number": 'LS2000-115VAC-S-10"',
            "base_price": 425.0,
            "base_length": 10.0,
            "voltage": "115VAC",
            "material": "S"
        }
    )
    
    # Get base price
    base_price = config_service.get_final_price()
    print(f"Base price: ${base_price:.2f}")
    
    # Set an accessory to "No" (should not add any price)
    config_service.set_option("Extra Static Protection", "No")
    
    # Get price after setting accessory to "No"
    price_with_no = config_service.get_final_price()
    print(f"Price with 'Extra Static Protection' = 'No': ${price_with_no:.2f}")
    
    # Verify price didn't change
    if abs(price_with_no - base_price) < 0.01:
        print("✓ Price unchanged when accessory set to 'No'")
    else:
        print(f"✗ Price changed unexpectedly: ${base_price} -> ${price_with_no}")
    
    # Set the same accessory to "Yes" (should add price)
    config_service.set_option("Extra Static Protection", "Yes")
    
    # Get price after setting accessory to "Yes"
    price_with_yes = config_service.get_final_price()
    print(f"Price with 'Extra Static Protection' = 'Yes': ${price_with_yes:.2f}")
    
    # Verify price increased
    if price_with_yes > base_price:
        print("✓ Price increased when accessory set to 'Yes'")
    else:
        print(f"✗ Price didn't increase: ${base_price} -> ${price_with_yes}")
    
    db.close()

def test_insulator_length_mapping():
    """Test insulator length key mapping."""
    print("\n=== Testing Insulator Length Mapping ===")
    
    db = SessionLocal()
    product_service = ProductService(db)
    config_service = ConfigurationService(db, product_service)
    
    # Start configuration for LS2000
    config_service.start_configuration(
        product_family_id=1,
        product_family_name="LS2000",
        base_product_info={
            "id": 1,
            "model_number": 'LS2000-115VAC-S-10"',
            "base_price": 425.0,
            "base_length": 10.0,
            "voltage": "115VAC",
            "material": "S"
        }
    )
    
    # Get base price
    base_price = config_service.get_final_price()
    print(f"Base price: ${base_price:.2f}")
    
    # Set insulator length to "4" (should map to "Standard")
    config_service.set_option("Insulator Length", "4")
    
    # Get price after setting insulator length
    price_with_insulator = config_service.get_final_price()
    print(f"Price with 'Insulator Length' = '4': ${price_with_insulator:.2f}")
    
    # Verify price didn't change (since "4" should map to "Standard")
    if abs(price_with_insulator - base_price) < 0.01:
        print("✓ Price unchanged when insulator length set to '4' (mapped to 'Standard')")
    else:
        print(f"✗ Price changed unexpectedly: ${base_price} -> ${price_with_insulator}")
    
    db.close()

def test_debug_model_numbers():
    """Test script to debug model number generation."""
    
    app = QApplication(sys.argv)
    
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        
        # Create the dialog
        dialog = ModernProductSelectionDialog(product_service)
        
        print("=== DEBUGGING MODEL NUMBER GENERATION ===")
        print("Please open the dialog and select each product family to see debug output.")
        print("Look for INITIAL_SETUP_DEBUG and DEFAULTS_DEBUG messages.")
        print("=" * 50)
        
        # Show the dialog
        dialog.show()
        
        # Run the application
        app.exec()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_ls2000_base_model()
    test_accessory_pricing()
    test_insulator_length_mapping()
    test_debug_model_numbers()
    print("\n=== Test Complete ===") 