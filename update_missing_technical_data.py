#!/usr/bin/env python3
"""
Update Missing Technical Data
Updates missing housing data and insulator information.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel

def update_missing_technical_data():
    """Update missing housing data and insulator information."""
    
    db = SessionLocal()
    try:
        print("=== UPDATING MISSING TECHNICAL DATA ===\n")
        
        # Get all base models
        base_models = db.query(BaseModel).all()
        
        updated_count = 0
        
        for model in base_models:
            model_number = model.model_number
            updates = []
            
            # Update LS6000 housing data
            if "LS6000" in model_number:
                if not getattr(model, 'housing_type', None):
                    model.housing_type = "Cast Aluminum, Explosion Proof - Class I, Groups C & D; Class II, Groups E, F & G"
                    updates.append("housing_type")
                
                if not getattr(model, 'housing_ratings', None):
                    model.housing_ratings = "7"
                    updates.append("housing_ratings")
            
            # Update FS10000 insulator data
            if "FS10000" in model_number:
                if not getattr(model, 'insulator_material', None):
                    model.insulator_material = "UHMWPE"
                    updates.append("insulator_material")
                
                if not getattr(model, 'insulator_length', None):
                    model.insulator_length = 1.0  # Base insulator length
                    updates.append("insulator_length")
                
                if not getattr(model, 'insulator_temp_rating', None):
                    model.insulator_temp_rating = "-30F to 450F"
                    updates.append("insulator_temp_rating")
            
            # Update LS7500 insulator data
            if "LS7500" in model_number:
                if not getattr(model, 'insulator_material', None):
                    model.insulator_material = "UHMWPE"
                    updates.append("insulator_material")
                
                if not getattr(model, 'insulator_length', None):
                    model.insulator_length = 1.0  # Base insulator length
                    updates.append("insulator_length")
                
                if not getattr(model, 'insulator_temp_rating', None):
                    model.insulator_temp_rating = "-30F to 450F"
                    updates.append("insulator_temp_rating")
            
            # Update LS8500 insulator data
            if "LS8500" in model_number:
                if not getattr(model, 'insulator_material', None):
                    model.insulator_material = "UHMWPE"
                    updates.append("insulator_material")
                
                if not getattr(model, 'insulator_length', None):
                    model.insulator_length = 1.0  # Base insulator length
                    updates.append("insulator_length")
                
                if not getattr(model, 'insulator_temp_rating', None):
                    model.insulator_temp_rating = "-30F to 450F"
                    updates.append("insulator_temp_rating")
            
            # Update TRAN-EX insulator data (assuming it's similar to LS8000/2)
            if "TRAN-EX" in model_number:
                if not getattr(model, 'insulator_material', None):
                    model.insulator_material = "TEF"
                    updates.append("insulator_material")
                
                if not getattr(model, 'insulator_length', None):
                    model.insulator_length = 4.0
                    updates.append("insulator_length")
                
                if not getattr(model, 'insulator_temp_rating', None):
                    model.insulator_temp_rating = "450F"
                    updates.append("insulator_temp_rating")
                
                if not getattr(model, 'housing_type', None):
                    model.housing_type = "Cast Aluminum, NEMA 7, C, D; NEMA 9, E, F, & G"
                    updates.append("housing_type")
                
                if not getattr(model, 'housing_ratings', None):
                    model.housing_ratings = "7"
                    updates.append("housing_ratings")
            
            if updates:
                updated_count += 1
                print(f"✓ {model_number}: Updated {', '.join(updates)}")
        
        if updated_count > 0:
            db.commit()
            print(f"\nSuccessfully updated {updated_count} models")
        else:
            print("\nNo updates were made")
        
        # Show summary of current state
        print("\n=== CURRENT TECHNICAL DATA STATE ===")
        for model in base_models:
            print(f"\n{model.model_number}:")
            
            insulator = getattr(model, 'insulator_material', None)
            insulator_len = getattr(model, 'insulator_length', None)
            insulator_temp = getattr(model, 'insulator_temp_rating', None)
            housing = getattr(model, 'housing_type', None)
            housing_ratings = getattr(model, 'housing_ratings', None)
            
            if insulator:
                print(f"  Insulator: {insulator}")
                if insulator_len:
                    print(f"  Insulator Length: {insulator_len}\"")
                if insulator_temp:
                    print(f"  Insulator Temp: {insulator_temp}")
            
            if housing:
                print(f"  Housing: {housing}")
                if housing_ratings:
                    print(f"  Housing Ratings: {housing_ratings}")
        
    except Exception as e:
        print(f"Error updating technical data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_missing_technical_data() 