#!/usr/bin/env python3
"""
Quick test for latest UI changes in the modern product selection dialog
"""

import sys
import logging
import traceback
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QDialog
from PySide6.QtCore import Qt

# Import our modern dialog
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog
from src.core.services.product_service import ProductService
from src.core.database import SessionLocal

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global exception hook to print all uncaught exceptions
def excepthook(type, value, tb):
    print("[GLOBAL EXCEPTION HOOK]")
    traceback.print_exception(type, value, tb)
    sys.__excepthook__(type, value, tb)

sys.excepthook = excepthook

class TestWindow(QMainWindow):
    """Test window for showing the latest modern product selection dialog"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Modern Product Selection Dialog")
        self.setGeometry(100, 100, 400, 200)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Add test button
        test_button = QPushButton("Open Modern Product Selection Dialog")
        test_button.clicked.connect(self.open_dialog)
        layout.addWidget(test_button)
        
        # Add status label
        self.status_label = QLabel("Click the button to test the dialog")
        layout.addWidget(self.status_label)
        
    def open_dialog(self):
        """Open the modern product selection dialog"""
        try:
            print("=== OPENING MODERN PRODUCT SELECTION DIALOG ===")
            
            # Create database session and product service
            db = SessionLocal()
            product_service = ProductService(db)
            
            # Create and show the dialog
            dialog = ModernProductSelectionDialog(product_service, self)
            
            # Test specific models
            self.test_specific_models(dialog, product_service, db)
            
            # Show the dialog
            result = dialog.exec()
            
            if result == QDialog.DialogCode.Accepted:
                self.status_label.setText("Dialog accepted - product added to quote")
            else:
                self.status_label.setText("Dialog cancelled")
                
        except Exception as e:
            print(f"Error opening dialog: {e}")
            traceback.print_exc()
            self.status_label.setText(f"Error: {e}")
    
    def test_specific_models(self, dialog, product_service, db):
        """Test specific models to see if they load properly"""
        print("\n=== TESTING SPECIFIC MODELS ===")
        
        # Test LS7000/2 and LS8000/2 specifically (these exist in the database)
        test_models = ["LS7000/2", "LS8000/2"]
        
        # First, let's see what products are actually loaded in the dialog
        print(f"\n--- Products loaded in dialog ---")
        print(f"Total products in dialog: {len(dialog.products)}")
        for i, product in enumerate(dialog.products):
            print(f"  {i+1}. {product.get('name', 'Unknown')} (ID: {product.get('id', 'N/A')})")
        
        for model_name in test_models:
            print(f"\n--- Testing {model_name} ---")
            try:
                # Check if the model exists in the product list
                found = False
                for product in dialog.products:
                    if product.get('name') == model_name:
                        found = True
                        print(f"✓ {model_name} found in product list")
                        print(f"  Product data: {product}")
                        break
                
                if not found:
                    print(f"✗ {model_name} NOT found in product list")
                    print(f"  Available products: {[p.get('name') for p in dialog.products]}")
                    continue
                
                # Test getting base product info
                base_product = product_service.get_base_product_for_family(db, model_name)
                if base_product:
                    print(f"✓ Base product found for {model_name}: {base_product}")
                else:
                    print(f"✗ No base product found for {model_name}")
                
                # Test getting available materials
                materials = product_service.get_available_materials_for_product(db, model_name)
                if materials:
                    print(f"✓ Materials found for {model_name}: {len(materials)} options")
                    for mat in materials:
                        print(f"  - {mat.get('name', 'Unknown')}: {mat.get('choices', [])}")
                else:
                    print(f"✗ No materials found for {model_name}")
                
                # Test getting available voltages
                voltages = product_service.get_available_voltages(db, model_name)
                if voltages:
                    print(f"✓ Voltages found for {model_name}: {voltages}")
                else:
                    print(f"✗ No voltages found for {model_name}")
                
            except Exception as e:
                print(f"✗ Error testing {model_name}: {e}")
                traceback.print_exc()
        
        print("\n=== SPECIFIC MODEL TESTING COMPLETE ===")

def main():
    """Main function to run the test"""
    app = QApplication(sys.argv)
    
    # Create and show the test window
    window = TestWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 