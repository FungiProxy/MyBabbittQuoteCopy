#!/usr/bin/env python3
"""
Add Housing Types to Housing Type Option

This script adds more housing types to the "Housing Type" option to make it a proper dropdown.
"""

import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.core.database import SessionLocal
from src.core.models.option import Option

def add_housing_types():
    """Add more housing types to the Housing Type option."""
    db = SessionLocal()
    
    try:
        # Find the Housing Type option
        housing_option = db.query(Option).filter_by(name='Housing Type').first()
        
        if not housing_option:
            print("Housing Type option not found!")
            return
        
        print(f"Current Housing Type choices: {housing_option.choices}")
        print(f"Current Housing Type adders: {housing_option.adders}")
        
        # Define the new housing types with their adders
        new_choices = [
            'Cast Aluminum',  # Standard
            'Stainless Steel (NEMA 4X)',  # Add $285.00
            'Big Housing (High Vibration)'  # No extra charge
        ]
        
        new_adders = {
            'Cast Aluminum': 0.0,
            'Stainless Steel (NEMA 4X)': 285.0,
            'Big Housing (High Vibration)': 0.0
        }
        
        # Update the option
        housing_option.choices = new_choices
        housing_option.adders = new_adders
        
        db.commit()
        
        print(f"Updated Housing Type choices: {housing_option.choices}")
        print(f"Updated Housing Type adders: {housing_option.adders}")
        print("Successfully updated Housing Type option!")
        
    except Exception as e:
        print(f"Error updating housing types: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_housing_types() 