#!/usr/bin/env python3
"""
Debug Housing UI Data Structure

This script checks the exact data structure of housing options as they come from the service
to understand why they're not showing as dropdowns.
"""

import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService

def debug_housing_data():
    """Debug housing options data structure."""
    db = SessionLocal()
    service = ProductService(db)
    
    try:
        # Get housing options for a specific family
        family_name = "LS8000"
        print(f"Getting additional options for family: {family_name}")
        
        options = service.get_additional_options(db, family_name)
        print(f"Total options returned: {len(options)}")
        
        housing_options = [opt for opt in options if opt.get('category') == 'Housing']
        print(f"Housing options found: {len(housing_options)}")
        
        for i, option in enumerate(housing_options):
            print(f"\nHousing Option {i+1}:")
            print(f"  Name: {option.get('name')}")
            print(f"  Category: {option.get('category')}")
            print(f"  Choices: {option.get('choices')} (type: {type(option.get('choices'))})")
            print(f"  Choices length: {len(option.get('choices', []))}")
            print(f"  Adders: {option.get('adders')}")
            print(f"  Full option dict: {option}")
            
            # Check if it should be a dropdown
            choices = option.get('choices', [])
            if choices and len(choices) > 1:
                print(f"  SHOULD BE DROPDOWN: Yes (has {len(choices)} choices)")
            else:
                print(f"  SHOULD BE DROPDOWN: No (choices: {choices})")
                
    finally:
        db.close()

if __name__ == "__main__":
    debug_housing_data() 