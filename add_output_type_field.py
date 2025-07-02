#!/usr/bin/env python3
"""
Add output_type field to base_models table and populate with correct values.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal, engine
from src.core.models.base_model import BaseModel
from sqlalchemy import text

def add_output_type_field():
    """Add output_type field to base_models table and populate it."""
    
    db = SessionLocal()
    try:
        print("=== ADDING OUTPUT_TYPE FIELD ===\n")
        
        # Add the output_type column to the table
        try:
            db.execute(text("ALTER TABLE base_models ADD COLUMN output_type TEXT"))
            db.commit()
            print("✓ Added output_type column to base_models table")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("✓ output_type column already exists")
            else:
                raise e
        
        # Output type mapping for each product family
        output_types = {
            "LS2000": "10 Amp SPDT Relay",
            "LS2100": "Normal 8mA; Alarm 16mA", 
            "LS6000": "5 Amp DPDT Relay",
            "LS7000": "2 Form C contacts 5 Amp DPDT Relay",
            "LS7000/2": "2 Form C contacts 5 Amp DPDT Relay",
            "LS8000": "5 Amp DPDT Relay",
            "LS8000/2": "10 Amp SPDT Relay",
            "LT9000": "4 to 20mA",
            "FS10000": "5 Amp DPDT Relay",
            "LS7500": "2 Form C Contacts; 5 Amp DPDT Relay",
            "LS8500": "2 Form C Contacts; 5 Amp DPDT Relay",
            "TRAN-EX": "5 Amp DPDT Relay"  # Assuming similar to LS8000/2
        }
        
        # Update each model with the correct output type
        updated_count = 0
        for model in db.query(BaseModel).all():
            family_name = model.product_family.name if model.product_family else 'Unknown'
            
            if family_name in output_types:
                model.output_type = output_types[family_name]
                updated_count += 1
                print(f"✓ {model.model_number}: {output_types[family_name]}")
            else:
                print(f"✗ {model.model_number}: No output type found for family '{family_name}'")
        
        if updated_count > 0:
            db.commit()
            print(f"\nSuccessfully updated {updated_count} output types")
        else:
            print("\nNo output types were updated")
        
        # Show summary
        print("\n=== OUTPUT TYPE SUMMARY ===")
        for model in db.query(BaseModel).all():
            output_type = getattr(model, 'output_type', None)
            if output_type:
                print(f"• {model.model_number}: {output_type}")
            else:
                print(f"• {model.model_number}: No output type set")
        
    except Exception as e:
        print(f"Error adding output_type field: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_output_type_field() 