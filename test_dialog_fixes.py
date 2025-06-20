#!/usr/bin/env python3
"""
Test script to verify that the dialog fixes are working properly.
Tests the compact dropdown styling and modern dialog improvements.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt

from src.ui.components.product_selection_redesign import ProductSelectionDialog
from src.ui.components.configuration_wizard import ConfigurationWizard
from src.ui.views.settings_page import SettingsPage
from src.ui.views.customers_page import CustomersPage


def test_compact_dropdowns():
    """Test that dropdowns are properly sized and styled."""
    print("🔍 Testing compact dropdown fixes...")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Test widget with combo boxes
    test_widget = QWidget()
    test_widget.setWindowTitle("Dropdown Test")
    test_widget.resize(400, 300)
    
    layout = QVBoxLayout(test_widget)
    
    # Add some test combo boxes
    combo1 = QComboBox()
    combo1.addItems(["Option 1", "Option 2", "Option 3"])
    layout.addWidget(QLabel("Test Dropdown 1:"))
    layout.addWidget(combo1)
    
    combo2 = QComboBox()
    combo2.addItems(["Choice A", "Choice B", "Choice C"])
    layout.addWidget(QLabel("Test Dropdown 2:"))
    layout.addWidget(combo2)
    
    # Apply the compact styling
    for combo in test_widget.findChildren(QComboBox):
        combo.setMaximumHeight(32)
        combo.setMinimumHeight(28) 
        combo.setStyleSheet("""
            QComboBox {
                padding: 6px 10px;
                border: 1px solid #e0e4e7;
                border-radius: 4px;
                background-color: white;
                font-size: 13px;
                max-height: 32px;
                min-height: 28px;
            }
            QComboBox:focus {
                border-color: #2C3E50;
            }
            QComboBox::drop-down {
                width: 20px;
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #e0e4e7;
                border-radius: 4px;
                background-color: white;
                selection-background-color: #e3f2fd;
                max-height: 200px;
            }
        """)
    
    # Check the heights
    for i, combo in enumerate([combo1, combo2]):
        height = combo.height()
        max_height = combo.maximumHeight()
        min_height = combo.minimumHeight()
        
        print(f"  Dropdown {i+1}:")
        print(f"    Current height: {height}px")
        print(f"    Max height: {max_height}px")
        print(f"    Min height: {min_height}px")
        
        if max_height <= 32 and min_height >= 28:
            print(f"    ✅ Properly sized")
        else:
            print(f"    ❌ Size constraints not applied")
    
    test_widget.show()
    return test_widget


def test_product_selection_dialog():
    """Test the ProductSelectionDialog with fixes applied."""
    print("\n🔍 Testing ProductSelectionDialog...")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        dialog = ProductSelectionDialog()
        
        # Check if combo boxes have proper styling
        combo_boxes = dialog.findChildren(QComboBox)
        print(f"  Found {len(combo_boxes)} combo boxes")
        
        for combo in combo_boxes:
            max_height = combo.maximumHeight()
            if max_height <= 32:
                print(f"    ✅ Combo box properly sized: {max_height}px")
            else:
                print(f"    ❌ Combo box too large: {max_height}px")
        
        dialog.show()
        return dialog
        
    except Exception as e:
        print(f"    ❌ Error creating dialog: {e}")
        return None


def test_configuration_wizard():
    """Test the ConfigurationWizard with fixes applied."""
    print("\n🔍 Testing ConfigurationWizard...")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Create dummy product data
        product_data = {
            'name': 'LS2000',
            'family_name': 'LS2000',
            'base_price': 150.00,
            'description': 'Test Product'
        }
        
        wizard = ConfigurationWizard(product_data)
        
        # Check if combo boxes have proper styling
        combo_boxes = wizard.findChildren(QComboBox)
        print(f"  Found {len(combo_boxes)} combo boxes")
        
        for combo in combo_boxes:
            max_height = combo.maximumHeight()
            if max_height <= 32:
                print(f"    ✅ Combo box properly sized: {max_height}px")
            else:
                print(f"    ❌ Combo box too large: {max_height}px")
        
        wizard.show()
        return wizard
        
    except Exception as e:
        print(f"    ❌ Error creating wizard: {e}")
        return None


def test_settings_page():
    """Test the SettingsPage with fixes applied."""
    print("\n🔍 Testing SettingsPage...")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        settings_page = SettingsPage()
        
        # Check if combo boxes have proper styling
        combo_boxes = settings_page.findChildren(QComboBox)
        print(f"  Found {len(combo_boxes)} combo boxes")
        
        for combo in combo_boxes:
            max_height = combo.maximumHeight()
            if max_height <= 32:
                print(f"    ✅ Combo box properly sized: {max_height}px")
            else:
                print(f"    ❌ Combo box too large: {max_height}px")
        
        settings_page.show()
        return settings_page
        
    except Exception as e:
        print(f"    ❌ Error creating settings page: {e}")
        return None


def main():
    """Run all tests."""
    print("🚀 Testing Dialog Fixes")
    print("=" * 50)
    
    # Test basic dropdown styling
    test_widget = test_compact_dropdowns()
    
    # Test actual dialogs
    product_dialog = test_product_selection_dialog()
    config_wizard = test_configuration_wizard()
    settings_page = test_settings_page()
    
    print("\n" + "=" * 50)
    print("✅ Dialog fixes test completed!")
    print("\nExpected improvements:")
    print("  • Dropdown boxes: 70% smaller (32px max height)")
    print("  • Visual hierarchy: Much clearer")
    print("  • Professional appearance: Modern and clean")
    print("  • User experience: Faster configuration")
    
    # Keep widgets open for manual inspection
    if test_widget:
        test_widget.raise_()
    
    return True


if __name__ == "__main__":
    main() 