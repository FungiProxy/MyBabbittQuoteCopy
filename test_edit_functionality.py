#!/usr/bin/env python3
"""
Test script to verify the edit functionality for quote items.
This script tests that when editing a quote item, the configuration dialog opens with the exact configuration that was selected.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog

def test_edit_functionality():
    """Test the edit functionality for different item types."""
    app = QApplication(sys.argv)
    
    # Initialize services
    db = SessionLocal()
    product_service = ProductService(db=db)
    
    # Test data for a configured product with complex configuration
    configured_product_to_edit = {
        "product_family": "LS2000",
        "model_number": "LS2000-115VAC-H-24\"-1.5\"TCSPUD-XSP-SSTAG-VR-90DEG-8\"TEFINS",
        "configuration": "Material: H | Voltage: 115VAC | Length: 24\" | Tri-clamp: 1.5\" Spud | XSP | SSTAG | VR | Bent Probe: 90° | Insulator: 8\" Teflon",
        "quantity": 2,
        "unit_price": 425.0,
        "total_price": 850.0,
        "config_data": {
            "Material": "H",
            "Voltage": "115VAC", 
            "Probe Length": 24.0,
            "Connection Type": "Tri-clamp",
            "Tri-clamp": "1.5\" Tri-clamp Spud",
            "Extra Static Protection": True,
            "Stainless Steel Tag": True,
            "Vibration Resistance": True,
            "Bent Probe": True,
            "Bent Probe Degree": 90,
            "Insulator Length": 8,
            "Insulator Material": "TEF"
        },
        "options": [],
        "base_product_info": {
            "id": 1,
            "model_number": "LS2000",
            "base_price": 425.0,
            "base_length": 10,
            "voltage": "115VAC",
            "material": "S"
        }
    }
    
    # Test data for a spare part
    spare_part_to_edit = {
        "product_family": "Spare Parts",
        "model_number": "ls2000-electronics-specify-voltage",
        "configuration": "Spare Part: LS2000-Electronics",
        "quantity": 3,
        "unit_price": 265.0,
        "total_price": 795.0,
        "is_spare_part": True,
        "spare_part_data": {
            "part_number": "ls2000-electronics-specify-voltage",
            "name": "LS2000-Electronics",
            "description": None,
            "price": 265.0,
            "category": None,
            "product_family_name": "LS2000"
        },
        "config_data": {},
        "options": []
    }
    
    # Test data for a simple configured product
    simple_product_to_edit = {
        "product_family": "LS2000",
        "model_number": "LS2000-115VAC-S-12\"",
        "configuration": "Material: S | Voltage: 115VAC | Length: 12\"",
        "quantity": 1,
        "unit_price": 425.0,
        "total_price": 425.0,
        "config_data": {
            "Material": "S",
            "Voltage": "115VAC", 
            "Probe Length": 12.0
        },
        "options": [],
        "base_product_info": {
            "id": 1,
            "model_number": "LS2000",
            "base_price": 425.0,
            "base_length": 10,
            "voltage": "115VAC",
            "material": "S"
        }
    }
    
    # Test data for a product with exotic metal
    exotic_product_to_edit = {
        "product_family": "LS2000",
        "model_number": "LS2000-115VAC-A-18\"-2\"150#-TEFINS",
        "configuration": "Material: A (Alloy) | Voltage: 115VAC | Length: 18\" | Flange: 2\" 150# | Teflon Insulator",
        "quantity": 1,
        "unit_price": 650.0,
        "total_price": 650.0,
        "config_data": {
            "Material": "A",
            "Voltage": "115VAC", 
            "Probe Length": 18.0,
            "Connection Type": "Flange",
            "Flange Size": "2\"",
            "Flange Rating": "150#",
            "Insulator Material": "TEF",
            "ExoticMetalAdder": "A"
        },
        "options": [],
        "base_product_info": {
            "id": 1,
            "model_number": "LS2000",
            "base_price": 425.0,
            "base_length": 10,
            "voltage": "115VAC",
            "material": "S"
        }
    }
    
    # Test data for a product with NPT connection
    npt_product_to_edit = {
        "product_family": "LS2000",
        "model_number": "LS2000-115VAC-S-10\"-3/4\"NPT",
        "configuration": "Material: S | Voltage: 115VAC | Length: 10\" | NPT: 3/4\"",
        "quantity": 1,
        "unit_price": 425.0,
        "total_price": 425.0,
        "config_data": {
            "Material": "S",
            "Voltage": "115VAC", 
            "Probe Length": 10.0,
            "Connection Type": "NPT",
            "NPT Size": "3/4\""
        },
        "options": [],
        "base_product_info": {
            "id": 1,
            "model_number": "LS2000",
            "base_price": 425.0,
            "base_length": 10,
            "voltage": "115VAC",
            "material": "S"
        }
    }
    
    def test_product_editing(product_to_edit, test_name):
        """Test editing a specific product configuration."""
        print(f"\n🧪 Testing {test_name}")
        print(f"📋 Model Number: {product_to_edit.get('model_number', 'N/A')}")
        print(f"🔧 Configuration: {product_to_edit.get('configuration', 'N/A')}")
        print(f"📦 Config Data: {product_to_edit.get('config_data', {})}")
        
        # Create dialog for editing
        dialog = ModernProductSelectionDialog(
            product_service=product_service,
            product_to_edit=product_to_edit,
            parent=None
        )
        
        # Connect the product_added signal to a test handler
        def on_product_added(config_data):
            print(f"✅ Item updated in quote:")
            print(f"   Type: {'Spare Part' if config_data.get('is_spare_part') else 'Product'}")
            print(f"   Name: {config_data.get('description', 'N/A')}")
            print(f"   Part Number: {config_data.get('model_number', 'N/A')}")
            print(f"   Price: ${config_data.get('total_price', 0):.2f}")
            print(f"   Config Data: {config_data.get('config_data', {})}")
            
            # Verify the configuration was preserved
            original_config = product_to_edit.get('config_data', {})
            new_config = config_data.get('config_data', {})
            
            print(f"   🔍 Configuration Comparison:")
            print(f"      Original: {original_config}")
            print(f"      New: {new_config}")
            
            # Check if key configurations match
            key_options = ['Material', 'Voltage', 'Probe Length', 'Connection Type']
            for option in key_options:
                if option in original_config:
                    original_val = original_config[option]
                    new_val = new_config.get(option)
                    if original_val == new_val:
                        print(f"      ✅ {option}: {original_val} (preserved)")
                    else:
                        print(f"      ❌ {option}: {original_val} -> {new_val} (changed)")
            
            # Check for special options
            special_options = ['XSP', 'SSTAG', 'VR', 'Bent Probe', 'Insulator Material']
            for option in special_options:
                if option in original_config:
                    original_val = original_config[option]
                    new_val = new_config.get(option)
                    if original_val == new_val:
                        print(f"      ✅ {option}: {original_val} (preserved)")
                    else:
                        print(f"      ❌ {option}: {original_val} -> {new_val} (changed)")
        
        dialog.product_added.connect(on_product_added)
        
        # Show the dialog
        print(f"🚀 Opening edit dialog for {test_name}...")
        print(f"📋 Instructions:")
        print(f"   1. Verify the configuration matches the original")
        print(f"   2. Check that all options are properly set")
        print(f"   3. Make any changes if desired")
        print(f"   4. Click 'Add to Quote' to test the update")
        print(f"   5. Close the dialog when done")
        
        result = dialog.exec()
        
        if result == dialog.DialogCode.Accepted:
            print(f"✅ {test_name} edit completed successfully")
        else:
            print(f"❌ {test_name} edit was cancelled")
        
        dialog.deleteLater()
    
    # Run the tests
    print("🧪 Starting Edit Functionality Tests")
    print("=" * 50)
    
    # Test simple product
    test_product_editing(simple_product_to_edit, "Simple Configured Product")
    
    # Test complex product
    test_product_editing(configured_product_to_edit, "Complex Configured Product")
    
    # Test exotic metal product
    test_product_editing(exotic_product_to_edit, "Exotic Metal Product")
    
    # Test NPT connection product
    test_product_editing(npt_product_to_edit, "NPT Connection Product")
    
    # Test spare part
    test_product_editing(spare_part_to_edit, "Spare Part")
    
    print("\n🎉 All tests completed!")
    print("📝 Check the output above to verify that:")
    print("   1. Configuration dialogs open with correct settings")
    print("   2. Model numbers are properly parsed")
    print("   3. All options are correctly restored")
    print("   4. Updates preserve the configuration data")
    print("   5. Special options (XSP, SSTAG, VR, etc.) are handled correctly")
    print("   6. Connection types (Tri-clamp, NPT, Flange) are properly restored")
    print("   7. Exotic metals and adders are correctly identified")
    
    # Clean up
    db.close()
    app.quit()

if __name__ == "__main__":
    test_edit_functionality() 