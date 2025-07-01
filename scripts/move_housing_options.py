#!/usr/bin/env python3
"""
Move Housing Options to Correct Category

This script moves housing-related options from the Accessories category
to the Housing category for better organization.
"""

import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.core.database import SessionLocal
from src.core.models.option import Option

def move_housing_options():
    """Move housing-related options to Housing category."""
    db = SessionLocal()
    
    try:
        # Find housing-related options in Accessories category
        housing_related = db.query(Option).filter(
            Option.category == "Accessories",
            (Option.name.ilike('%housing%') | 
             Option.name.ilike('%enclosure%') | 
             Option.name.ilike('%nema%') | 
             Option.name.ilike('%explosion%') |
             Option.name.ilike('%receiver%'))
        ).all()
        
        print(f"Found {len(housing_related)} housing-related options in Accessories category:")
        
        for option in housing_related:
            print(f"  - {option.name}")
            option.category = "Housing"
            print(f"    Moved to Housing category")
        
        if housing_related:
            db.commit()
            print(f"\nSuccessfully moved {len(housing_related)} options to Housing category!")
        else:
            print("No housing-related options found in Accessories category.")
        
    except Exception as e:
        print(f"Error moving housing options: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    move_housing_options() 