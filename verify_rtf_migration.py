#!/usr/bin/env python3
"""
Verify the RTF migration results.
"""

import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel


def verify_migration():
    """Verify the RTF migration results."""
    db = SessionLocal()
    
    try:
        print("=== VERIFYING RTF MIGRATION ===")
        
        base_models = db.query(BaseModel).all()
        
        print(f"\nTotal base models: {len(base_models)}")
        
        # Check which models have RTF data
        models_with_data = []
        models_without_data = []
        
        for model in base_models:
            if model.insulator_material:
                models_with_data.append(model)
            else:
                models_without_data.append(model)
        
        print(f"\nModels with RTF data: {len(models_with_data)}")
        print(f"Models without RTF data: {len(models_without_data)}")
        
        print("\n=== MODELS WITH RTF DATA ===")
        for model in models_with_data:
            print(f"\n{model.model_number}:")
            print(f"  Insulator Material: {model.insulator_material}")
            print(f"  Insulator Length: {model.insulator_length}")
            print(f"  Temp Rating: {model.insulator_temp_rating}")
            print(f"  Process Connection: {model.process_connection}")
            print(f"  Max Pressure: {model.max_pressure}")
            print(f"  Housing Type: {model.housing_type}")
            print(f"  Housing Ratings: {model.housing_ratings}")
            print(f"  Application Notes: {model.application_notes}")
            print(f"  Special Notes: {model.special_notes}")
        
        print("\n=== MODELS WITHOUT RTF DATA ===")
        for model in models_without_data:
            print(f"  - {model.model_number}")
        
        print("\n✓ Verification completed!")
        
    except Exception as e:
        print(f"Error during verification: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    verify_migration() 