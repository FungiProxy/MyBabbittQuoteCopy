#!/usr/bin/env python3
"""
Debug script to check voltage options issue.
"""

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService

def debug_voltage_issue():
    """Debug why voltage options aren't being found."""
    db = SessionLocal()
    product_service = ProductService()
    
    try:
        family_name = "LS2000"
        print(f"Debugging voltage options for {family_name}")
        
        # Get all additional options
        all_options = product_service.get_additional_options(db, family_name)
        print(f"Total additional options: {len(all_options)}")
        
        # Find voltage options
        voltage_options = [opt for opt in all_options if opt.get('name') == 'Voltage']
        print(f"Voltage options found: {len(voltage_options)}")
        
        if voltage_options:
            voltage_opt = voltage_options[0]
            print(f"Voltage option details:")
            print(f"  - Name: {voltage_opt.get('name')}")
            print(f"  - Category: {voltage_opt.get('category')}")
            print(f"  - Choices: {voltage_opt.get('choices')}")
            print(f"  - Adders: {voltage_opt.get('adders')}")
        
        # Try the get_available_voltages method
        voltages = product_service.get_available_voltages(db, family_name)
        print(f"get_available_voltages result: {voltages}")
        
        # Check if we should use the voltage option from additional_options instead
        if voltage_options:
            voltage_opt = voltage_options[0]
            choices = voltage_opt.get('choices', [])
            print(f"Voltage choices from additional_options: {choices}")
            
            # Extract voltage values
            voltage_values = []
            for choice in choices:
                if isinstance(choice, dict):
                    voltage_values.append(choice.get('code', choice.get('display_name', choice)))
                else:
                    voltage_values.append(choice)
            
            print(f"Extracted voltage values: {voltage_values}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_voltage_issue() 