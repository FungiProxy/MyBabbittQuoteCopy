#!/usr/bin/env python3
"""
Standardize all material options to use the LS2000 format.
Convert simple string choices to structured objects with code and display_name.
This will make the UI code simpler and more consistent across all families.
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal
from src.core.models.option import Option
import json
from sqlalchemy import and_

def standardize_material_format():
    db = SessionLocal()
    try:
        print("Standardizing material options format across all families...")
        
        # Material code to display name mapping
        material_display_names = {
            "S": "S - 316 Stainless Steel",
            "H": "H - Halar Coated", 
            "TS": "TS - Teflon Sleeve",
            "T": "T - Teflon",
            "U": "U - UHMWPE",
            "CPVC": "CPVC - CPVC",
            "C": "C - Cable",
            "A": "A - Alloy 20",
            "HC": "HC - Hastelloy C-276",
            "HB": "HB - Hastelloy B", 
            "TT": "TT - Titanium",
            "M": "M - Monel",
            "I": "I - Inconel"
        }
        
        material_options = db.query(Option).filter(
            and_(Option.name == "Material", Option.category == "Material")
        ).all()
        
        for option in material_options:
            changed = False
            choices = option.choices
            
            # Handle string format (needs conversion)
            if isinstance(choices, str):
                try:
                    choices = json.loads(choices)
                except Exception:
                    continue
            
            # Check if already in structured format
            if choices and isinstance(choices[0], dict):
                print(f"  {option.product_families}: Already in structured format")
                continue
            
            # Convert simple strings to structured format
            new_choices = []
            for choice in choices:
                if isinstance(choice, str):
                    display_name = material_display_names.get(choice, choice)
                    new_choices.append({
                        "code": choice,
                        "display_name": display_name
                    })
                    changed = True
                else:
                    new_choices.append(choice)
            
            if changed:
                option.choices = new_choices
                print(f"  ✅ Converted {option.product_families}: {len(choices)} → {len(new_choices)} structured choices")
        
        db.commit()
        print("\n✅ Material format standardization complete!")
        print("All families now use structured format with code and display_name properties.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    standardize_material_format() 