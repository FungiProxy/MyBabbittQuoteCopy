#!/usr/bin/env python3
"""
Check Housing Options in Database

This script checks what housing options are currently in the database
and their associations with product families.
"""

import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily

def check_housing_options():
    """Check housing options in the database."""
    db = SessionLocal()
    
    try:
        # Get all housing options
        housing_options = db.query(Option).filter_by(category="Housing").all()
        
        print(f"Found {len(housing_options)} housing options in database:")
        print()
        
        for option in housing_options:
            print(f"Option: {option.name}")
            print(f"  Description: {option.description}")
            print(f"  Choices: {option.choices}")
            print(f"  Adders: {option.adders}")
            print(f"  Rules: {option.rules}")
            
            # Get associated product families
            family_links = db.query(ProductFamilyOption).filter_by(option_id=option.id).all()
            families = []
            for link in family_links:
                family = db.query(ProductFamily).filter_by(id=link.product_family_id).first()
                if family:
                    families.append(family.name)
            
            print(f"  Associated Families: {', '.join(families)}")
            print()
        
        # Also check for any options with housing-related names
        housing_related = db.query(Option).filter(
            Option.name.ilike('%housing%') | 
            Option.name.ilike('%enclosure%') | 
            Option.name.ilike('%nema%') | 
            Option.name.ilike('%explosion%') |
            Option.name.ilike('%receiver%')
        ).all()
        
        if housing_related:
            print(f"Found {len(housing_related)} additional housing-related options:")
            for option in housing_related:
                print(f"  - {option.name} (Category: {option.category})")
        
    except Exception as e:
        print(f"Error checking housing options: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    check_housing_options() 