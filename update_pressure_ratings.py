#!/usr/bin/env python3
"""
Update Pressure Ratings Based on NPT Connection Sizes
Updates missing pressure ratings based on the NPT connection size.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel

def update_pressure_ratings():
    """Update pressure ratings based on NPT connection sizes."""
    
    db = SessionLocal()
    try:
        print("=== UPDATING PRESSURE RATINGS ===\n")
        
        # NPT size to pressure mapping
        npt_pressure_map = {
            '3/4"': '300',
            '1"': '1500'
        }
        
        # Get all base models missing pressure ratings
        models_to_update = db.query(BaseModel).filter(
            BaseModel.max_pressure.is_(None)
        ).all()
        
        print(f"Found {len(models_to_update)} models missing pressure ratings")
        print()
        
        updated_count = 0
        
        for model in models_to_update:
            connection_size = getattr(model, 'process_connection_size', None)
            
            if connection_size and connection_size in npt_pressure_map:
                pressure = npt_pressure_map[connection_size]
                model.max_pressure = pressure
                updated_count += 1
                print(f"✓ {model.model_number}: {connection_size} NPT → {pressure} PSI")
            else:
                print(f"✗ {model.model_number}: No NPT size found or unknown size '{connection_size}'")
        
        if updated_count > 0:
            db.commit()
            print(f"\nSuccessfully updated {updated_count} pressure ratings")
        else:
            print("\nNo pressure ratings were updated")
        
        # Show remaining models that still need pressure ratings
        remaining = db.query(BaseModel).filter(
            BaseModel.max_pressure.is_(None)
        ).all()
        
        if remaining:
            print(f"\n=== REMAINING MODELS NEEDING PRESSURE RATINGS ===")
            print(f"Count: {len(remaining)}")
            for model in remaining:
                connection_size = getattr(model, 'process_connection_size', None)
                print(f"• {model.model_number} (Connection: {connection_size or 'NOT SET'})")
        
    except Exception as e:
        print(f"Error updating pressure ratings: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_pressure_ratings() 