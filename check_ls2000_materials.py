#!/usr/bin/env python3
"""
Check LS2000 material options in the database.
"""

from src.core.database import SessionLocal
from src.core.models.option import Option

def check_ls2000_materials():
    """Check what material options are currently configured for LS2000."""
    db = SessionLocal()
    try:
        options = db.query(Option).filter(
            Option.product_families.like('%LS2000%'),
            Option.name == 'Material'
        ).all()
        
        print("Current LS2000 Material Options:")
        print("=" * 50)
        
        for opt in options:
            print(f"ID: {opt.id}")
            print(f"Choices: {opt.choices}")
            print(f"Adders: {opt.adders}")
            print(f"Product Families: {opt.product_families}")
            print("-" * 30)
            
        if not options:
            print("No material options found for LS2000")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_ls2000_materials() 