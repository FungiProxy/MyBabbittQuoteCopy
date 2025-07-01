#!/usr/bin/env python3
"""
Debug script to see exactly what's happening with insulator material UI.
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
        print("=== DATABASE STATE ===")
        
        # Check insulator material option
        insulator_option = db.query(Option).filter_by(name='Insulator Material').first()
        if insulator_option:
            print(f"Insulator Material option:")
            print(f"  Choices: {insulator_option.choices}")
            print(f"  Adders: {insulator_option.adders}")
        else:
            print("No Insulator Material option found!")
            return
        
        # Check base models
        print(f"\n=== BASE MODELS ===")
        base_models = db.query(BaseModel).filter(
            BaseModel.insulator_material.isnot(None)
        ).all()
        
        for model in base_models:
            print(f"  {model.model_number}: {model.insulator_material}")
        
        # Test options for different families
        print(f"\n=== OPTIONS BY FAMILY ===")
        
        families = ["LS2000", "LS6000", "LS7000/2"]
        for family in families:
            print(f"\n{family}:")
            # Get options for this family
            options = db.query(Option).filter(
                Option.product_families.like(f"%{family}%")
            ).all()
            
            for opt in options:
                if opt.name == 'Insulator Material':
                    print(f"  Found Insulator Material option:")
                    print(f"    Choices: {opt.choices}")
                    print(f"    Adders: {opt.adders}")
                    
                    # Check if this family has a base model with insulator material
                    base_model = db.query(BaseModel).filter(
                        BaseModel.model_number.like(f"{family}%")
                    ).first()
                    
                    if base_model and base_model.insulator_material:
                        print(f"    Base model insulator: {base_model.insulator_material}")
                        
                        # Test the matching logic
                        base_code = base_model.insulator_material.strip().upper()
                        print(f"    Looking for code: '{base_code}'")
                        
                        for choice in opt.choices:
                            if isinstance(choice, dict):
                                choice_code = choice.get('code', '').strip().upper()
                                display_name = choice.get('display_name', '')
                                print(f"      Choice: {choice_code} ({display_name})")
                                if choice_code == base_code:
                                    print(f"      *** MATCH FOUND ***")
                            else:
                                print(f"      Choice: {choice}")
                    break
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main() 