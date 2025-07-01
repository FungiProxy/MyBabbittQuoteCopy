#!/usr/bin/env python3
"""
Migration script to add RTF data columns to base_models table.
Shows the plan before executing.
"""

import sys
import os
import json

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel


def show_migration_plan():
    """Show the migration plan before executing."""
    
    # Load RTF data
    with open("extracted_rtf_data.json", "r", encoding="utf-8") as f:
        rtf_data = json.load(f)
    
    # Create RTF data lookup
    rtf_lookup = {}
    for item in rtf_data:
        family = item['product_family']
        material = item.get('material_type', '')
        key = f"{family}-{material}" if material else family
        rtf_lookup[key] = item
    
    print("=== MIGRATION PLAN ===")
    print("\n1. ADD THESE COLUMNS TO base_models TABLE:")
    print("   - insulator_material (TEXT)")
    print("   - insulator_length (FLOAT)")
    print("   - insulator_temp_rating (TEXT)")
    print("   - process_connection (TEXT)")
    print("   - max_pressure (TEXT)")
    print("   - housing_type (TEXT)")
    print("   - housing_ratings (TEXT)")
    print("   - application_notes (TEXT)")
    print("   - special_notes (TEXT)")
    
    print("\n2. DATA MAPPING (Base Model → RTF Template):")
    
    db = SessionLocal()
    try:
        base_models = db.query(BaseModel).all()
        
        for model in base_models:
            print(f"\n{model.model_number}:")
            
            # Determine which RTF template to use based on material
            material = model.material
            family = model.model_number.split('-')[0]
            
            # Check if there's a specific RTF template for this material
            if material == 'S':
                # Look for explicit Stainless Steel template first
                rtf_key = f"{family}-Stainless Steel"
                if rtf_key not in rtf_lookup:
                    # If no explicit template, use base family template
                    rtf_key = family
            elif material == 'H':
                rtf_key = f"{family}-HALAR"
            else:
                rtf_key = family
            
            rtf_item = rtf_lookup.get(rtf_key)
            
            if rtf_item:
                print(f"  → RTF Template: {rtf_key}")
                print(f"  → Insulator: {rtf_item.get('insulator_material', 'N/A')}")
                print(f"  → Process Connection: {rtf_item.get('process_connection', 'N/A')}")
                print(f"  → Max Pressure: {rtf_item.get('max_pressure', 'N/A')}")
                print(f"  → Housing: {rtf_item.get('housing_type', 'N/A')}")
            else:
                print(f"  → NO RTF TEMPLATE FOUND for {rtf_key}")
    
    finally:
        db.close()
    
    print("\n3. SQL TO EXECUTE:")
    print("""
ALTER TABLE base_models ADD COLUMN insulator_material TEXT;
ALTER TABLE base_models ADD COLUMN insulator_length FLOAT;
ALTER TABLE base_models ADD COLUMN insulator_temp_rating TEXT;
ALTER TABLE base_models ADD COLUMN process_connection TEXT;
ALTER TABLE base_models ADD COLUMN max_pressure TEXT;
ALTER TABLE base_models ADD COLUMN housing_type TEXT;
ALTER TABLE base_models ADD COLUMN housing_ratings TEXT;
ALTER TABLE base_models ADD COLUMN application_notes TEXT;
ALTER TABLE base_models ADD COLUMN special_notes TEXT;
    """)
    
    print("=== END PLAN ===")
    print("\nShould I proceed with this migration?")


if __name__ == "__main__":
    show_migration_plan() 