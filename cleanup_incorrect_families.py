#!/usr/bin/env python3
"""
Cleanup script to remove incorrectly created product families.
Removes LS7000-2 and LS8000-2 families that should be LS7000/2 and LS8000/2.
"""

import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily
from src.core.models.base_model import BaseModel
from src.core.models.option import ProductFamilyOption


def cleanup_incorrect_families():
    """Remove incorrectly created product families."""
    db = SessionLocal()
    
    try:
        print("Cleaning up incorrectly created product families...")
        
        # Find and remove incorrect families
        incorrect_families = ['LS7000-2', 'LS8000-2']
        
        for family_name in incorrect_families:
            family = db.query(ProductFamily).filter_by(name=family_name).first()
            if family:
                print(f"Removing family: {family_name}")
                
                # Remove associated base models
                base_models = db.query(BaseModel).filter_by(product_family_id=family.id).all()
                for bm in base_models:
                    print(f"  Removing base model: {bm.model_number}")
                    db.delete(bm)
                
                # Remove family-option associations
                family_options = db.query(ProductFamilyOption).filter_by(product_family_id=family.id).all()
                for fo in family_options:
                    print(f"  Removing family-option association: {fo.product_family_id}-{fo.option_id}")
                    db.delete(fo)
                
                # Remove the family itself
                db.delete(family)
                print(f"  Removed family: {family_name}")
            else:
                print(f"Family not found: {family_name}")
        
        db.commit()
        print("Cleanup completed successfully!")
        
        # Print remaining families
        print("\nRemaining product families:")
        families = db.query(ProductFamily).all()
        for family in families:
            print(f"  {family.name}")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    cleanup_incorrect_families() 