#!/usr/bin/env python3
"""
Standardize exotic metal codes in the options table for all product families.
- Replace 'A20' with 'A' (Alloy 20)
- Replace 'TI' with 'TT' (Titanium)
- Remove any old codes from choices/adders
- Ensure only 'A' and 'TT' are present for Alloy 20 and Titanium
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal
from src.core.models.option import Option
import json
from sqlalchemy import and_

def standardize_exotic_material_codes():
    db = SessionLocal()
    try:
        print("Standardizing exotic metal codes in options table...")
        material_options = db.query(Option).filter(
            and_(Option.name == "Material", Option.category == "Material")
        ).all()
        for option in material_options:
            changed = False
            # Handle choices (could be list of dicts or strings)
            choices = option.choices
            if isinstance(choices, str):
                try:
                    choices = json.loads(choices)
                except Exception:
                    pass
            # Remove any TI/A20 entries (as string or dict)
            filtered_choices = []
            for c in choices:
                if isinstance(c, dict):
                    code = c.get('code', '')
                    if code in ('TI', 'A20'):
                        changed = True
                        continue
                    filtered_choices.append(c)
                elif c in ('TI', 'A20'):
                    changed = True
                    continue
                else:
                    filtered_choices.append(c)
            # Ensure 'A' and 'TT' are present with correct display names
            codes_in_choices = set(
                c['code'] if isinstance(c, dict) else c for c in filtered_choices
            )
            if 'A' not in codes_in_choices:
                filtered_choices.append({'code': 'A', 'display_name': 'A - Alloy 20'})
                changed = True
            if 'TT' not in codes_in_choices:
                filtered_choices.append({'code': 'TT', 'display_name': 'TT - Titanium'})
                changed = True
            # Remove duplicates
            seen = set()
            deduped_choices = []
            for x in filtered_choices:
                key = json.dumps(x, sort_keys=True) if isinstance(x, dict) else str(x)
                if key not in seen:
                    seen.add(key)
                    deduped_choices.append(x)
            new_choices = deduped_choices
            # Handle adders
            adders = option.adders
            if isinstance(adders, str):
                try:
                    adders = json.loads(adders)
                except Exception:
                    pass
            new_adders = {}
            for k, v in adders.items():
                if k == 'A20':
                    new_adders['A'] = v
                    changed = True
                elif k == 'TI':
                    new_adders['TT'] = v
                    changed = True
                else:
                    new_adders[k] = v
            # Remove old keys if present
            if 'A20' in new_adders:
                del new_adders['A20']
                changed = True
            if 'TI' in new_adders:
                del new_adders['TI']
                changed = True
            # Ensure adders for 'A' and 'TT' exist
            if 'A' not in new_adders:
                new_adders['A'] = 0
                changed = True
            if 'TT' not in new_adders:
                new_adders['TT'] = 0
                changed = True
            # Save changes if any
            if changed:
                option.choices = new_choices
                option.adders = new_adders
                print(f"Updated Material Option for Product Family: {option.product_families}")
        db.commit()
        print("Standardization complete!")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    standardize_exotic_material_codes() 