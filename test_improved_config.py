#!/usr/bin/env python3
"""
Test script to verify the improved product configuration dialog.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt

from src.core.services.product_service import ProductService
from src.ui.product_selection_dialog_improved import ImprovedProductSelectionDialog

class TestWindow(QMainWindow):
    """Test window to verify the improved product configuration."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Improved Product Configuration")
        self.setGeometry(100, 100, 400, 200)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Test Improved Product Configuration")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Test button
        test_button = QPushButton("Open Product Configuration Dialog")
        test_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        test_button.clicked.connect(self.test_product_configuration)
        layout.addWidget(test_button)
        
        # Status label
        self.status_label = QLabel("Click the button to test the product configuration dialog")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #6C757D; margin-top: 20px;")
        layout.addWidget(self.status_label)
        
        # Initialize services
        self.product_service = ProductService()
    
    def test_product_configuration(self):
        """Test the improved product configuration dialog."""
        try:
            self.status_label.setText("Opening product configuration dialog...")
            
            # Create and show the dialog
            dialog = ImprovedProductSelectionDialog(
                product_service=self.product_service,
                parent=self
            )
            
            # Connect to the product added signal
            dialog.product_added.connect(self.on_product_added)
            
            # Show the dialog
            result = dialog.exec()
            
            if result == dialog.Accepted:
                self.status_label.setText("Dialog closed - product was added")
            else:
                self.status_label.setText("Dialog closed - no product added")
                
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            print(f"Error testing product configuration: {e}")
    
    def on_product_added(self, config_data):
        """Handle product added from the dialog."""
        print("Product added successfully!")
        print(f"Product: {config_data.get('product', 'N/A')}")
        print(f"Description: {config_data.get('description', 'N/A')}")
        print(f"Unit Price: ${config_data.get('unit_price', 0):.2f}")
        print(f"Quantity: {config_data.get('quantity', 0)}")
        print(f"Total Price: ${config_data.get('total_price', 0):.2f}")
        print(f"Configuration: {config_data.get('configuration', {})}")
        
        self.status_label.setText(f"Product added: {config_data.get('product', 'N/A')} - ${config_data.get('total_price', 0):.2f}")

def main():
    """Main function to run the test."""
    app = QApplication(sys.argv)
    
    # Create and show the test window
    window = TestWindow()
    window.show()
    
    print("🏭 Testing Improved Product Configuration Dialog")
    print("   ✨ All available options for each product family")
    print("   🎯 Real-time pricing with full pricing system")
    print("   🔥 Material, voltage, length, connection configuration")
    print("   💎 Additional options and adders")
    print("   📊 Professional styling and user experience")
    
    return app.exec()

if __name__ == "__main__":
    main() 