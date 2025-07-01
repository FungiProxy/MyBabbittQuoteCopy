#!/usr/bin/env python3
"""
Update base model prices in the database.

This script updates only the base_price field in the base_models table
according to the new pricing specifications.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel


def update_base_model_prices():
    """Update base model prices according to new specifications."""
    
    # New prices mapping by model number
    new_prices = {
        'LS2000-115VAC-S-10"': 455.0,
        'LS2100-24VDC-S-10"': 480.0,
        'LS6000-115VAC-S-10"': 580.0,
        'LS7000-115VAC-S-10"': 715.0,
        'LS7000/2-115VAC-H-10"': 800.0,
        'LS8000-115VAC-S-10"': 750.0,
        'LS8000/2-115VAC-H-10"': 900.0,
        'LT9000-115VAC-H-10"': 920.0,
        'FS10000-115VAC-S-6"': 1980.0,
        'LS8000/2-TRAN-EX-S-10': 570.0,
    }
    
    db = SessionLocal()
    try:
        print("Updating base model prices...")
        print("-" * 50)
        
        updated_count = 0
        for model_number, new_price in new_prices.items():
            # Find the base model by model number
            base_model = db.query(BaseModel).filter_by(model_number=model_number).first()
            
            if base_model:
                old_price = base_model.base_price
                base_model.base_price = new_price
                print(f"✓ {model_number}: ${old_price:.2f} → ${new_price:.2f}")
                updated_count += 1
            else:
                print(f"✗ {model_number}: NOT FOUND in database")
        
        # Commit the changes
        db.commit()
        
        print("-" * 50)
        print(f"✅ Successfully updated {updated_count} base model prices")
        
        # Verify the updates
        print("\nVerifying updates:")
        print("-" * 30)
        for model_number, expected_price in new_prices.items():
            base_model = db.query(BaseModel).filter_by(model_number=model_number).first()
            if base_model:
                actual_price = base_model.base_price
                status = "✓" if actual_price == expected_price else "✗"
                print(f"{status} {model_number}: ${actual_price:.2f}")
            else:
                print(f"✗ {model_number}: NOT FOUND")
        
    except Exception as e:
        print(f"❌ Error updating base model prices: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    update_base_model_prices() 