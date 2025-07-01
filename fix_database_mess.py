#!/usr/bin/env python3
"""
Fix the database mess - remove all incorrect base models added by the RTF integration.
"""

import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel
from src.core.models.option import ProductFamilyOption


def fix_database_mess():
    """Remove all the incorrect base models I added."""
    db = SessionLocal()
    
    try:
        print("Fixing database mess - removing incorrect base models...")
        
        # Find all base models with -XX suffix or incorrect specifications
        incorrect_models = db.query(BaseModel).filter(
            BaseModel.model_number.like('%-XX')
        ).all()
        
        print(f"Found {len(incorrect_models)} incorrect base models to remove:")
        
        for model in incorrect_models:
            print(f"  Removing: {model.model_number} (ID: {model.id})")
            
            # Remove any family-option associations that might have been created
            # for these incorrect models (though they shouldn't exist)
            
            # Remove the base model
            db.delete(model)
        
        # Also remove any base models with clearly incorrect descriptions
        incorrect_descriptions = db.query(BaseModel).filter(
            BaseModel.description.like('%specification from RTF template%')
        ).all()
        
        for model in incorrect_descriptions:
            if model not in incorrect_models:  # Avoid double deletion
                print(f"  Removing: {model.model_number} (ID: {model.id}) - incorrect description")
                db.delete(model)
        
        db.commit()
        print("Database cleanup completed successfully!")
        
        # Show remaining base models
        print("\nRemaining base models:")
        remaining_models = db.query(BaseModel).all()
        for model in remaining_models:
            print(f"  {model.model_number}: {model.description}")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    fix_database_mess() 