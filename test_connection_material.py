#!/usr/bin/env python3
"""
Test script to check if Connection Material option exists in database
"""

import os
import sys
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal
from src.core.models.option import Option

def test_connection_material():
    """Test if Connection Material option exists in database."""
    db = SessionLocal()
    try:
        # Check if Connection Material option exists
        connection_material = db.query(Option).filter_by(
            name="Connection Material",
            category="Connections"
        ).first()
        
        if connection_material:
            print(f"✓ Connection Material option found:")
            print(f"  ID: {connection_material.id}")
            print(f"  Name: {connection_material.name}")
            print(f"  Category: {connection_material.category}")
            print(f"  Product Families: {connection_material.product_families}")
            print(f"  Choices: {connection_material.choices}")
            print(f"  Adders: {connection_material.adders}")
        else:
            print("✗ Connection Material option NOT found in database")
            
        # Check all connection options
        all_connection_options = db.query(Option).filter_by(category="Connections").all()
        print(f"\nAll Connection options ({len(all_connection_options)}):")
        for opt in all_connection_options:
            print(f"  - {opt.name} (ID: {opt.id})")
            
        # Check if the option exists with different category
        other_categories = db.query(Option).filter_by(name="Connection Material").all()
        if other_categories:
            print(f"\nConnection Material found with other categories:")
            for opt in other_categories:
                print(f"  - Category: {opt.category}, ID: {opt.id}")
                
    finally:
        db.close()

if __name__ == "__main__":
    test_connection_material() 