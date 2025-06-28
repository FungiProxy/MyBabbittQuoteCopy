#!/usr/bin/env python3
"""
Debug script to check product families in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models import ProductFamily

def main():
    """Check what product families are in the database"""
    db = SessionLocal()
    
    try:
        print("=== CHECKING PRODUCT FAMILIES IN DATABASE ===")
        
        # Get all product families
        families = db.query(ProductFamily).all()
        
        print(f"\nTotal product families found: {len(families)}")
        print("\nAll product families:")
        for family in families:
            print(f"  - ID: {family.id}, Name: '{family.name}', Description: '{family.description}'")
        
        # Check specifically for LS7000/2 and LS8000/3
        print("\n=== CHECKING FOR SPECIFIC MODELS ===")
        
        ls7000_2 = db.query(ProductFamily).filter(ProductFamily.name == "LS7000/2").first()
        if ls7000_2:
            print(f"✓ LS7000/2 found: ID={ls7000_2.id}, Description='{ls7000_2.description}'")
        else:
            print("✗ LS7000/2 NOT found in database")
        
        ls8000_3 = db.query(ProductFamily).filter(ProductFamily.name == "LS8000/3").first()
        if ls8000_3:
            print(f"✓ LS8000/3 found: ID={ls8000_3.id}, Description='{ls8000_3.description}'")
        else:
            print("✗ LS8000/3 NOT found in database")
        
        # Check for similar names
        print("\n=== CHECKING FOR SIMILAR NAMES ===")
        ls7000_families = db.query(ProductFamily).filter(ProductFamily.name.like("LS7000%")).all()
        print(f"LS7000 families: {[f.name for f in ls7000_families]}")
        
        ls8000_families = db.query(ProductFamily).filter(ProductFamily.name.like("LS8000%")).all()
        print(f"LS8000 families: {[f.name for f in ls8000_families]}")
        
        # Check for families with /2 or /3 in the name
        families_with_slash = db.query(ProductFamily).filter(
            ProductFamily.name.like("%/%")
        ).all()
        print(f"\nFamilies with / in name: {[f.name for f in families_with_slash]}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main() 