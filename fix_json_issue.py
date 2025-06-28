#!/usr/bin/env python3
"""
Fix corrupted JSON fields in the database
"""

import json
from src.core.database import SessionLocal, engine
from src.core.models.option import Option
from sqlalchemy import text

def fix_json_fields():
    """Fix corrupted JSON fields in the options table"""
    db = SessionLocal()
    try:
        print("Fixing corrupted JSON fields in options table...")
        
        # First, let's see what we have
        result = db.execute(text("SELECT id, name, choices, adders, rules FROM options LIMIT 10"))
        rows = result.fetchall()
        
        print(f"Found {len(rows)} options to check")
        
        for row in rows:
            option_id, name, choices, adders, rules = row
            print(f"\nChecking option: {name} (ID: {option_id})")
            
            # Fix choices field
            if choices == '' or choices == 'null' or choices is None:
                print(f"  Fixing empty choices field")
                db.execute(text("UPDATE options SET choices = '[]' WHERE id = :id"), {"id": option_id})
            
            # Fix adders field
            if adders == '' or adders == 'null' or adders is None:
                print(f"  Fixing empty adders field")
                db.execute(text("UPDATE options SET adders = '{}' WHERE id = :id"), {"id": option_id})
            
            # Fix rules field
            if rules == '' or rules == 'null' or rules is None:
                print(f"  Fixing empty rules field")
                db.execute(text("UPDATE options SET rules = 'null' WHERE id = :id"), {"id": option_id})
        
        # Commit the changes
        db.commit()
        print("\nDatabase fixes completed.")
        
        # Now try to query the options again
        print("\nTesting database query...")
        options = db.query(Option).limit(5).all()
        print(f"Successfully queried {len(options)} options")
        
        for option in options:
            print(f"  - {option.name}: choices={type(option.choices)}, adders={type(option.adders)}")
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_json_fields() 