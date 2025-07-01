#!/usr/bin/env python3
"""
Execute the RTF migration - add columns and update base models with cleaned RTF data.
"""

import sys
import os
import json
import re

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from sqlalchemy import text
from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel


def clean_rtf_text(text):
    """Clean RTF formatting artifacts from text."""
    if not text:
        return None
    
    # Remove RTF artifacts and clean up
    text = re.sub(r'\\[a-z]+\d*', '', text)
    text = re.sub(r'\\[{}]', '', text)
    text = re.sub(r'\\\'[0-9a-f]{2}', '', text)
    text = re.sub(r'\\\*\\[a-z]+', '', text)
    text = re.sub(r'\\[a-z]+\s*\{[^}]*\}', '', text)
    text = re.sub(r'{\\?[^}]*}', '', text)
    text = re.sub(r'\\[a-z]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Remove trailing artifacts
    text = re.sub(r'\s*\{\s*$', '', text)
    text = re.sub(r'\s*\\\s*$', '', text)
    
    return text if text else None


def execute_migration():
    """Execute the RTF migration."""
    db = SessionLocal()
    
    try:
        print("=== EXECUTING RTF MIGRATION ===")
        
        # Step 1: Add new columns
        print("\n1. Adding new columns to base_models table...")
        
        # Execute ALTER TABLE statements
        alter_statements = [
            "ALTER TABLE base_models ADD COLUMN insulator_material TEXT;",
            "ALTER TABLE base_models ADD COLUMN insulator_length FLOAT;",
            "ALTER TABLE base_models ADD COLUMN insulator_temp_rating TEXT;",
            "ALTER TABLE base_models ADD COLUMN process_connection TEXT;",
            "ALTER TABLE base_models ADD COLUMN max_pressure TEXT;",
            "ALTER TABLE base_models ADD COLUMN housing_type TEXT;",
            "ALTER TABLE base_models ADD COLUMN housing_ratings TEXT;",
            "ALTER TABLE base_models ADD COLUMN application_notes TEXT;",
            "ALTER TABLE base_models ADD COLUMN special_notes TEXT;"
        ]
        
        for statement in alter_statements:
            db.execute(text(statement))
            print(f"  ✓ {statement}")
        
        db.commit()
        print("  ✓ Columns added successfully!")
        
        # Step 2: Load and clean RTF data
        print("\n2. Loading and cleaning RTF data...")
        
        with open("extracted_rtf_data.json", "r", encoding="utf-8") as f:
            rtf_data = json.load(f)
        
        # Create RTF data lookup
        rtf_lookup = {}
        for item in rtf_data:
            family = item['product_family']
            material = item.get('material_type', '')
            key = f"{family}-{material}" if material else family
            rtf_lookup[key] = item
        
        # Step 3: Update base models
        print("\n3. Updating base models with RTF data...")
        
        base_models = db.query(BaseModel).all()
        
        for model in base_models:
            print(f"\nProcessing: {model.model_number}")
            
            # Determine which RTF template to use
            material = model.material
            family = model.model_number.split('-')[0]
            
            if material == 'S':
                rtf_key = f"{family}-Stainless Steel"
                if rtf_key not in rtf_lookup:
                    rtf_key = family
            elif material == 'H':
                rtf_key = f"{family}-HALAR"
            else:
                rtf_key = family
            
            rtf_item = rtf_lookup.get(rtf_key)
            
            if rtf_item:
                print(f"  → Using RTF template: {rtf_key}")
                
                # Clean and update the data
                model.insulator_material = clean_rtf_text(rtf_item.get('insulator_material'))
                model.insulator_length = rtf_item.get('insulator_length')
                model.insulator_temp_rating = clean_rtf_text(rtf_item.get('insulator_temp_rating'))
                model.process_connection = clean_rtf_text(rtf_item.get('process_connection'))
                model.max_pressure = rtf_item.get('max_pressure')
                model.housing_type = clean_rtf_text(rtf_item.get('housing_type'))
                model.housing_ratings = clean_rtf_text(rtf_item.get('housing_ratings'))
                model.application_notes = clean_rtf_text(rtf_item.get('application_notes'))
                
                # Handle special notes (list)
                special_notes = rtf_item.get('special_notes', [])
                if special_notes:
                    cleaned_notes = [clean_rtf_text(note) for note in special_notes if clean_rtf_text(note) is not None]
                    model.special_notes = '; '.join(cleaned_notes) if cleaned_notes else None
                else:
                    model.special_notes = None
                
                print(f"  ✓ Updated with RTF data")
            else:
                print(f"  → No RTF template found for {rtf_key} - leaving empty")
        
        db.commit()
        print("\n✓ Migration completed successfully!")
        
        # Show summary
        print("\n=== MIGRATION SUMMARY ===")
        updated_count = sum(1 for model in base_models if model.insulator_material is not None)
        print(f"Base models updated with RTF data: {updated_count}/{len(base_models)}")
        
        for model in base_models:
            if model.insulator_material:
                print(f"  ✓ {model.model_number}: {model.insulator_material}")
            else:
                print(f"  - {model.model_number}: No RTF data")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    execute_migration() 