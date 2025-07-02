#!/usr/bin/env python3
"""
Debug script to check NPT Size options in the database for LS8000.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.option import Option

def debug_ls8000_npt():
    """Debug NPT Size options for LS8000."""
    print("=== Debugging LS8000 NPT Size Options ===")
    
    db = SessionLocal()
    
    # Get all NPT Size options
    npt_options = db.query(Option).filter(Option.name == "NPT Size").all()
    
    print(f"Found {len(npt_options)} total NPT Size options in database:")
    
    for opt in npt_options:
        print(f"\nOption ID: {opt.id}")
        print(f"Name: {opt.name}")
        print(f"Category: {opt.category}")
        print(f"Product Families: {opt.product_families}")
        print(f"Choices: {opt.choices}")
        print(f"Adders: {opt.adders}")
        
        # Check if this option applies to LS8000
        if opt.product_families and "LS8000" in opt.product_families:
            print("  ✓ This option applies to LS8000")
        else:
            print("  ✗ This option does NOT apply to LS8000")
    
    # Check specifically for LS8000 options
    print(f"\n=== Options that contain 'LS8000' in product_families ===")
    ls8000_options = db.query(Option).filter(
        Option.product_families.contains("LS8000")
    ).all()
    
    for opt in ls8000_options:
        print(f"\nOption ID: {opt.id}")
        print(f"Name: {opt.name}")
        print(f"Category: {opt.category}")
        print(f"Product Families: {opt.product_families}")
        if opt.name == "NPT Size":
            print(f"Choices: {opt.choices}")
            print(f"Adders: {opt.adders}")
    
    db.close()

if __name__ == "__main__":
    debug_ls8000_npt() 