#!/usr/bin/env python3
"""
Test script to verify the part number fix for quote items.
This script tests that spare parts show full part numbers and configured products show dynamic part numbers.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog

def test_part_number_logic():
    """Test the part number logic for different item types."""
    app = QApplication(sys.argv)
    
    # Initialize services
    db = SessionLocal()
    product_service = ProductService(db=db)
    
    # Create the dialog
    dialog = ModernProductSelectionDialog(product_service=product_service)
    
    # Connect the product_added signal to a test handler
    def on_product_added(config_data):
        print(f"✅ Item added to quote:")
        print(f"   Type: {'Spare Part' if config_data.get('is_spare_part') else 'Product'}")
        print(f"   Name: {config_data.get('description', 'N/A')}")
        print(f"   Part Number: {config_data.get('model_number', 'N/A')}")
        print(f"   Price: ${config_data.get('total_price', 0):.2f}")
        
        # Verify part number logic
        if config_data.get('is_spare_part'):
            # For spare parts, should show full part number
            expected_part_number = config_data.get('model_number', '')
            if expected_part_number and expected_part_number != 'N/A':
                print(f"   ✅ Spare part shows full part number: {expected_part_number}")
            else:
                print(f"   ❌ Spare part missing part number")
        else:
            # For configured products, should show dynamic part number
            expected_part_number = config_data.get('model_number', '')
            if expected_part_number and expected_part_number != 'N/A':
                print(f"   ✅ Configured product shows dynamic part number: {expected_part_number}")
            else:
                print(f"   ❌ Configured product missing part number")
    
    dialog.product_added.connect(on_product_added)
    
    # Show the dialog
    print("🚀 Opening product selection dialog...")
    print("📋 Instructions for testing part number logic:")
    print("   1. Test spare parts:")
    print("      - Look for 'Spare Parts' in the left panel")
    print("      - Click on 'Spare Parts' to enter spare parts mode")
    print("      - Select a spare part and add to quote")
    print("      - Verify the part number shows the full spare part number")
    print("   2. Test configured products:")
    print("      - Select a product family (e.g., LS2000)")
    print("      - Configure options (material, voltage, length)")
    print("      - Add to quote")
    print("      - Verify the part number shows the dynamic part number")
    print()
    
    result = dialog.exec()
    
    if result == dialog.DialogCode.Accepted:
        print("✅ Dialog closed normally")
    else:
        print("❌ Dialog was cancelled")
    
    db.close()
    return result

if __name__ == "__main__":
    test_part_number_logic() 