#!/usr/bin/env python3
"""
Test script to verify exotic metals functionality in the UI.
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

from PySide6.QtWidgets import QApplication
from src.ui.product_selection_dialog_improved import ModernOptionWidget
from PySide6.QtWidgets import QVBoxLayout, QWidget

def test_exotic_metals_widget():
    """Test the ModernOptionWidget with exotic metals."""
    app = QApplication(sys.argv)
    
    # Create a test window
    window = QWidget()
    window.setWindowTitle("Exotic Metals Test")
    window.resize(400, 300)
    
    layout = QVBoxLayout(window)
    
    # Test material options with exotic metals
    material_choices = ["S", "H", "TS", "A", "HB", "HC", "TT"]
    material_adders = {
        "S": 0,
        "H": 110,
        "TS": 110,
        "A": 0,  # Exotic metal - will show manual input
        "HB": 0,  # Exotic metal - will show manual input
        "HC": 0,  # Exotic metal - will show manual input
        "TT": 0,  # Exotic metal - will show manual input
    }
    
    # Create the material widget
    material_widget = ModernOptionWidget(
        option_name="Material",
        choices=material_choices,
        adders=material_adders,
        widget_type='combobox'
    )
    
    layout.addWidget(material_widget)
    
    # Test a non-material widget to ensure it doesn't show exotic metal input
    voltage_choices = ["115VAC", "24VDC", "230VAC"]
    voltage_adders = {"115VAC": 0, "24VDC": 0, "230VAC": 0}
    
    voltage_widget = ModernOptionWidget(
        option_name="Voltage",
        choices=voltage_choices,
        adders=voltage_adders,
        widget_type='combobox'
    )
    
    layout.addWidget(voltage_widget)
    
    # Connect signals to test functionality
    def on_material_changed(option_name, value):
        print(f"Material changed to: {value}")
        if value in ["A", "HB", "HC", "TT"]:
            print(f"  Exotic metal selected: {value}")
            print(f"  Manual adder value: {material_widget.get_manual_adder_value()}")
            print(f"  Current adder value: {material_widget.get_current_adder_value()}")
    
    material_widget.option_changed.connect(on_material_changed)
    
    window.show()
    
    print("Exotic Metals Test Window opened.")
    print("Instructions:")
    print("1. Select different materials from the dropdown")
    print("2. When you select A, HB, HC, or TT, a manual adder input should appear")
    print("3. Change the manual adder value and observe the price display update")
    print("4. Select non-exotic metals to see the manual input disappear")
    
    return app.exec()

if __name__ == "__main__":
    test_exotic_metals_widget() 