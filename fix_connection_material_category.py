#!/usr/bin/env python3
"""
Fix the category of Connection Material option
"""

import os
import sys
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal
from src.core.models.option import Option

def fix_connection_material_category():
    """Fix the category of Connection Material option."""
    db = SessionLocal()
    try:
        # Find the Connection Material option with wrong category
        connection_material = db.query(Option).filter_by(
            name="Connection Material",
            category="Connection Material"
        ).first()
        
        if connection_material:
            print(f"Found Connection Material option with wrong category (ID: {connection_material.id})")
            connection_material.category = "Connections"
            db.commit()
            print("✓ Fixed category to 'Connections'")
        else:
            print("No Connection Material option found with wrong category")
            
        # Verify the fix
        fixed_option = db.query(Option).filter_by(
            name="Connection Material",
            category="Connections"
        ).first()
        
        if fixed_option:
            print(f"✓ Verification: Connection Material option now has category '{fixed_option.category}'")
        else:
            print("✗ Verification failed: Connection Material option not found with correct category")
            
    finally:
        db.close()

if __name__ == "__main__":
    fix_connection_material_category() 