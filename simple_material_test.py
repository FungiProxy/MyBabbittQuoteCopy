#!/usr/bin/env python3
"""
Simple test for material length reset functionality
"""

import sys
import logging
from PySide6.QtWidgets import QApplication

# Set up logging to see debug output
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Test material defaults
from src.core.config.material_defaults import get_material_default_length

def test_material_defaults():
    """Test material default lengths"""
    print("=== TESTING MATERIAL DEFAULTS ===")
    
    test_materials = ["S", "H", "TS", "U", "T", "C", "CPVC"]
    for material in test_materials:
        default_length = get_material_default_length(material)
        print(f"{material}: {default_length}\"")

if __name__ == "__main__":
    test_material_defaults()
    
    # Create QApplication for testing
    app = QApplication(sys.argv)
    
    try:
        from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog
        from src.core.services.product_service import ProductService
        from src.core.database import SessionLocal
        
        print("\n=== TESTING DIALOG CREATION ===")
        
        # Create database session and product service
        db = SessionLocal()
        product_service = ProductService(db)
        
        # Create dialog
        dialog = ModernProductSelectionDialog(product_service)
        print("Dialog created successfully")
        
        # Test material default function
        print("\n=== TESTING MATERIAL LENGTH RESET ===")
        test_length = get_material_default_length("S")
        print(f"Testing reset to material S default: {test_length}")
        
        # This should trigger the reset function
        dialog._reset_probe_length_to_material_default(test_length)
        
        print("Test completed successfully")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc() 