#!/usr/bin/env python3
"""
Fix FS10000 material options by removing incorrect materials.
"""

from src.core.database import SessionLocal
from src.core.models.option import Option

def fix_fs10000_materials():
    """Fix FS10000 material options to only include valid materials."""
    db = SessionLocal()
    try:
        # Find the FS10000 material option
        fs10000_material = db.query(Option).filter(
            Option.product_families == 'FS10000',
            Option.name == 'Material'
        ).first()
        
        if not fs10000_material:
            print("No FS10000 material option found!")
            return
            
        print(f"Current FS10000 material option ID: {fs10000_material.id}")
        print(f"Current choices: {fs10000_material.choices}")
        print(f"Current adders: {fs10000_material.adders}")
        
        # Define correct FS10000 materials (only S for base material)
        correct_choices = [
            {'code': 'S', 'display_name': 'S - 316 Stainless Steel'},
        ]
        
        correct_adders = {
            'S': 0.0,
        }
        
        # Update the option
        fs10000_material.choices = correct_choices
        fs10000_material.adders = correct_adders
        
        db.commit()
        
        print("\nFixed FS10000 material options:")
        print(f"Updated choices: {fs10000_material.choices}")
        print(f"Updated adders: {fs10000_material.adders}")
        print("FS10000 material options have been corrected!")
        print("\nNote: Exotic metals (A, HC, HB, TT) are handled by the separate 'Exotic Metal' option.")
        
    except Exception as e:
        print(f"Error fixing FS10000 materials: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_fs10000_materials() 