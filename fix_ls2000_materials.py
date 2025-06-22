#!/usr/bin/env python3
"""
Fix LS2000 material options by removing incorrect materials.
"""

from src.core.database import SessionLocal
from src.core.models.option import Option

def fix_ls2000_materials():
    """Fix LS2000 material options to only include valid materials."""
    db = SessionLocal()
    try:
        # Find the LS2000 material option
        ls2000_material = db.query(Option).filter(
            Option.product_families == 'LS2000',
            Option.name == 'Material'
        ).first()
        
        if not ls2000_material:
            print("No LS2000 material option found!")
            return
            
        print(f"Current LS2000 material option ID: {ls2000_material.id}")
        print(f"Current choices: {ls2000_material.choices}")
        print(f"Current adders: {ls2000_material.adders}")
        
        # Define correct LS2000 materials
        correct_choices = [
            {'code': 'S', 'display_name': 'S - 316 Stainless Steel'},
            {'code': 'H', 'display_name': 'H - Halar Coated'},
            {'code': 'TS', 'display_name': 'TS - Teflon Sleeve'},
            {'code': 'U', 'display_name': 'U - UHMWPE'},
            {'code': 'T', 'display_name': 'T - Teflon'},
            {'code': 'C', 'display_name': 'C - Cable'},
        ]
        
        correct_adders = {
            'S': 0.0,
            'H': 110.0,
            'TS': 110.0,
            'U': 20.0,
            'T': 60.0,
            'C': 80.0,
        }
        
        # Update the option
        ls2000_material.choices = correct_choices
        ls2000_material.adders = correct_adders
        
        db.commit()
        
        print("\nFixed LS2000 material options:")
        print(f"Updated choices: {ls2000_material.choices}")
        print(f"Updated adders: {ls2000_material.adders}")
        print("LS2000 material options have been corrected!")
        
    except Exception as e:
        print(f"Error fixing LS2000 materials: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_ls2000_materials() 