#!/usr/bin/env python3
"""
Verify the updated base model prices.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel


def verify_prices():
    """Verify the updated base model prices."""
    
    # Expected prices
    expected_prices = {
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
        print("Verifying base model prices...")
        print("-" * 50)
        
        all_correct = True
        for model_number, expected_price in expected_prices.items():
            base_model = db.query(BaseModel).filter_by(model_number=model_number).first()
            
            if base_model:
                actual_price = base_model.base_price
                status = "✓" if actual_price == expected_price else "✗"
                print(f"{status} {model_number}: ${actual_price:.2f}")
                
                if actual_price != expected_price:
                    all_correct = False
            else:
                print(f"✗ {model_number}: NOT FOUND")
                all_correct = False
        
        print("-" * 50)
        if all_correct:
            print("✅ All prices are correct!")
        else:
            print("❌ Some prices are incorrect!")
            
    except Exception as e:
        print(f"❌ Error verifying prices: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    verify_prices() 