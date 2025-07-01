#!/usr/bin/env python3
"""
Script to check the current state of insulator material configuration.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.option import Option
from src.core.models.base_model import BaseModel

def main():
    db = SessionLocal()
    
    try:
        print("=== INSULATOR MATERIAL OPTION ===")
        
        # Check insulator material options
        insulator_option = db.query(Option).filter_by(name='Insulator Material').first()
        if insulator_option:
            print(f"Insulator Material option found:")
            print(f"  Choices: {insulator_option.choices}")
            print(f"  Adders: {insulator_option.adders}")
        else:
            print("No Insulator Material option found!")
            return
        
        print("\n=== BASE MODELS WITH INSULATOR MATERIAL ===")
        
        # Check base models with insulator material
        base_models_with_insulator = db.query(BaseModel).filter(
            BaseModel.insulator_material.isnot(None)
        ).all()
        
        print(f"Base models with insulator material: {len(base_models_with_insulator)}")
        for model in base_models_with_insulator:
            print(f"  {model.model_number}: {model.insulator_material}")
        
        print("\n=== ALL INSULATOR OPTIONS ===")
        
        # Check all insulator-related options
        insulator_options = db.query(Option).filter(
            Option.name.like('%Insulator%')
        ).all()
        
        for option in insulator_options:
            print(f"  {option.name} ({option.category}):")
            print(f"    Choices: {option.choices}")
            print(f"    Adders: {option.adders}")
            print()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 