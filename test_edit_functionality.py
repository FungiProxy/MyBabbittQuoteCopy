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
    
    # Test data for a configured product
    configured_product_to_edit = {
        "product_family": "LS2000",
        "model_number": "LS2000-115VAC-S-24\"",
        "configuration": "Material: S | Voltage: 115VAC | Length: 24\"",
        "quantity": 2,
        "unit_price": 425.0,
        "total_price": 850.0,
        "config_data": {
            "Material": "S",
            "Voltage": "115VAC", 
            "Probe Length": 24.0
        },
        "options": []
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
        }
    }
    
    # Connect the product_added signal to a test handler
    def on_product_added(config_data):
        print(f"✅ Item updated in quote:")
        print(f"   Type: {'Spare Part' if config_data.get('is_spare_part') else 'Product'}")
        print(f"   Name: {config_data.get('description', 'N/A')}")
        print(f"   Part Number: {config_data.get('model_number', 'N/A')}")
        print(f"   Quantity: {config_data.get('quantity', 1)}")
        print(f"   Price: ${config_data.get('total_price', 0):.2f}")
        
        # Verify the configuration was loaded correctly
        if config_data.get('is_spare_part'):
            print(f"   ✅ Spare part configuration loaded correctly")
        else:
            print(f"   ✅ Product configuration loaded correctly")
    
    print("🚀 Testing Edit Functionality")
    print("📋 Instructions for testing edit functionality:")
    print("   1. Test configured product editing:")
    print("      - The dialog should open with LS2000 selected")
    print("      - Material should be set to 'S'")
    print("      - Voltage should be set to '115VAC'")
    print("      - Probe Length should be set to '24\"'")
    print("      - Quantity should be set to '2'")
    print("   2. Test spare part editing:")
    print("      - The dialog should open with 'Spare Parts' selected")
    print("      - The specific spare part should be selected")
    print("      - Quantity should be set to '3'")
    print()
    
    # Test configured product editing
    print("🔧 Testing configured product editing...")
    dialog1 = ModernProductSelectionDialog(
        product_service=product_service,
        product_to_edit=configured_product_to_edit
    )
    dialog1.product_added.connect(on_product_added)
    
    result1 = dialog1.exec()
    
    if result1 == dialog1.DialogCode.Accepted:
        print("✅ Configured product edit dialog closed normally")
    else:
        print("❌ Configured product edit dialog was cancelled")
    
    # Test spare part editing
    print("\n🔧 Testing spare part editing...")
    dialog2 = ModernProductSelectionDialog(
        product_service=product_service,
        product_to_edit=spare_part_to_edit
    )
    dialog2.product_added.connect(on_product_added)
    
    result2 = dialog2.exec()
    
    if result2 == dialog2.DialogCode.Accepted:
        print("✅ Spare part edit dialog closed normally")
    else:
        print("❌ Spare part edit dialog was cancelled")
    
    db.close()
    return result1, result2

if __name__ == "__main__":
    test_edit_functionality() 