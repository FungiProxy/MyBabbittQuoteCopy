#!/usr/bin/env python3
"""
Check database for corrupted JSON fields
"""

import json
from src.core.database import SessionLocal
from src.core.models.option import Option

def check_json_fields():
    """Check for corrupted JSON fields in the options table"""
    db = SessionLocal()
    try:
        print("Checking options table for corrupted JSON fields...")
        
        options = db.query(Option).all()
        print(f"Found {len(options)} options")
        
        for option in options:
            print(f"\nChecking option: {option.name} (ID: {option.id})")
            
            # Check choices field
            if option.choices is not None:
                try:
                    if isinstance(option.choices, str):
                        json.loads(option.choices)
                        print(f"  ✓ choices field is valid JSON")
                    else:
                        print(f"  ✓ choices field is already a Python object: {type(option.choices)}")
                except json.JSONDecodeError as e:
                    print(f"  ✗ choices field has invalid JSON: {e}")
                    print(f"    Raw value: {option.choices}")
            
            # Check adders field
            if option.adders is not None:
                try:
                    if isinstance(option.adders, str):
                        json.loads(option.adders)
                        print(f"  ✓ adders field is valid JSON")
                    else:
                        print(f"  ✓ adders field is already a Python object: {type(option.adders)}")
                except json.JSONDecodeError as e:
                    print(f"  ✗ adders field has invalid JSON: {e}")
                    print(f"    Raw value: {option.adders}")
            
            # Check rules field
            if option.rules is not None:
                try:
                    if isinstance(option.rules, str):
                        json.loads(option.rules)
                        print(f"  ✓ rules field is valid JSON")
                    else:
                        print(f"  ✓ rules field is already a Python object: {type(option.rules)}")
                except json.JSONDecodeError as e:
                    print(f"  ✗ rules field has invalid JSON: {e}")
                    print(f"    Raw value: {option.rules}")
        
        print("\nDatabase check completed.")
        
    except Exception as e:
        print(f"Error checking database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_json_fields() 