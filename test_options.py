#!/usr/bin/env python3
"""
Quick test script to check database options.
"""

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily

def test_options():
    db = SessionLocal()
    try:
        # Check options
        options = db.query(Option).all()
        print(f'Total options: {len(options)}')
        
        for i, option in enumerate(options[:10]):  # Show first 10
            print(f'\nOption {i+1}:')
            print(f'  Name: {option.name}')
            print(f'  Category: {option.category}')
            print(f'  Choices: {option.choices}')
            print(f'  Adders: {option.adders}')
            print(f'  Product Families: {option.product_families}')
        
        # Check product families
        families = db.query(ProductFamily).all()
        print(f'\nTotal product families: {len(families)}')
        for family in families:
            print(f'  - {family.name}')
            
        # Check ProductFamilyOption relationships
        family_options = db.query(ProductFamilyOption).all()
        print(f'\nTotal ProductFamilyOption records: {len(family_options)}')
        for fo in family_options[:10]:  # Show first 10
            family = db.query(ProductFamily).filter_by(id=fo.product_family_id).first()
            option = db.query(Option).filter_by(id=fo.option_id).first()
            print(f'  {family.name if family else "Unknown"} -> {option.name if option else "Unknown"} (available: {fo.is_available})')
            
    finally:
        db.close()

if __name__ == '__main__':
    test_options() 