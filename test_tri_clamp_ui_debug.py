#!/usr/bin/env python3
"""
Test script to debug Tri-clamp UI issue
"""

import os
import sys
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal
from src.core.models.option import Option
import json

def test_tri_clamp_ui_debug():
    """Test to debug why Tri-clamp UI isn't showing."""
    db = SessionLocal()
    try:
        print("=== TRI-CLAMP UI DEBUG TEST ===\n")
        
        # Check all connection options
        connection_options = db.query(Option).filter_by(category="Connections").all()
        print(f"Found {len(connection_options)} connection options:")
        
        for opt in connection_options:
            print(f"  - {opt.name} (ID: {opt.id})")
            
            # Parse choices and adders
            choices = json.loads(opt.choices) if isinstance(opt.choices, str) else opt.choices
            adders = json.loads(opt.adders) if isinstance(opt.adders, str) else opt.adders
            
            print(f"    Choices: {choices}")
            print(f"    Adders: {adders}")
            print(f"    Product Families: {opt.product_families}")
            print()
        
        # Specifically check Tri-clamp option
        tri_clamp_option = db.query(Option).filter_by(
            name="Tri-clamp",
            category="Connections"
        ).first()
        
        if tri_clamp_option:
            print("✓ Tri-clamp option found in database")
            choices = json.loads(tri_clamp_option.choices) if isinstance(tri_clamp_option.choices, str) else tri_clamp_option.choices
            print(f"  Choices: {choices}")
        else:
            print("✗ Tri-clamp option NOT found in database")
            
        # Check Connection Type option
        connection_type_option = db.query(Option).filter_by(
            name="Connection Type",
            category="Connections"
        ).first()
        
        if connection_type_option:
            print("\n✓ Connection Type option found")
            choices = json.loads(connection_type_option.choices) if isinstance(connection_type_option.choices, str) else connection_type_option.choices
            print(f"  Choices: {choices}")
        else:
            print("\n✗ Connection Type option NOT found")
            
    finally:
        db.close()

if __name__ == "__main__":
    test_tri_clamp_ui_debug() 