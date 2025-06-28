#!/usr/bin/env python3
"""
Comprehensive fix for all JSON issues in the database
"""

import json
from src.core.database import engine
from sqlalchemy import text

def fix_all_json_issues():
    """Fix all corrupted JSON fields in the database using raw SQL"""
    try:
        print("=== COMPREHENSIVE JSON FIX ===")
        
        # Connect directly to the database
        with engine.connect() as conn:
            # First, let's see what we have
            print("\n1. Checking current state of options table...")
            result = conn.execute(text("SELECT id, name, choices, adders, rules FROM options"))
            rows = result.fetchall()
            
            print(f"Found {len(rows)} options in database")
            
            # Fix all options
            print("\n2. Fixing all JSON fields...")
            for row in rows:
                option_id, name, choices, adders, rules = row
                print(f"  Processing: {name} (ID: {option_id})")
                
                # Fix choices field
                if choices is None or choices == '' or choices == 'null':
                    print(f"    Fixing empty choices field")
                    conn.execute(text("UPDATE options SET choices = '[]' WHERE id = :id"), {"id": option_id})
                elif isinstance(choices, str):
                    try:
                        json.loads(choices)
                        print(f"    ✓ choices field is valid JSON")
                    except json.JSONDecodeError:
                        print(f"    ✗ Fixing invalid choices JSON: {choices}")
                        conn.execute(text("UPDATE options SET choices = '[]' WHERE id = :id"), {"id": option_id})
                
                # Fix adders field
                if adders is None or adders == '' or adders == 'null':
                    print(f"    Fixing empty adders field")
                    conn.execute(text("UPDATE options SET adders = '{}' WHERE id = :id"), {"id": option_id})
                elif isinstance(adders, str):
                    try:
                        json.loads(adders)
                        print(f"    ✓ adders field is valid JSON")
                    except json.JSONDecodeError:
                        print(f"    ✗ Fixing invalid adders JSON: {adders}")
                        conn.execute(text("UPDATE options SET adders = '{}' WHERE id = :id"), {"id": option_id})
                
                # Fix rules field
                if rules is None or rules == '' or rules == 'null':
                    print(f"    Fixing empty rules field")
                    conn.execute(text("UPDATE options SET rules = 'null' WHERE id = :id"), {"id": option_id})
                elif isinstance(rules, str):
                    try:
                        json.loads(rules)
                        print(f"    ✓ rules field is valid JSON")
                    except json.JSONDecodeError:
                        print(f"    ✗ Fixing invalid rules JSON: {rules}")
                        conn.execute(text("UPDATE options SET rules = 'null' WHERE id = :id"), {"id": option_id})
            
            # Commit all changes
            conn.commit()
            print("\n3. All changes committed successfully!")
            
            # Verify the fix
            print("\n4. Verifying the fix...")
            result = conn.execute(text("SELECT id, name, choices, adders, rules FROM options LIMIT 5"))
            rows = result.fetchall()
            
            for row in rows:
                option_id, name, choices, adders, rules = row
                print(f"  {name}: choices={type(choices)}, adders={type(adders)}, rules={type(rules)}")
                
                # Test JSON parsing
                if isinstance(choices, str):
                    try:
                        json.loads(choices)
                        print(f"    ✓ choices parses correctly")
                    except json.JSONDecodeError as e:
                        print(f"    ✗ choices still has issues: {e}")
                
                if isinstance(adders, str):
                    try:
                        json.loads(adders)
                        print(f"    ✓ adders parses correctly")
                    except json.JSONDecodeError as e:
                        print(f"    ✗ adders still has issues: {e}")
                
                if isinstance(rules, str) and rules != 'null':
                    try:
                        json.loads(rules)
                        print(f"    ✓ rules parses correctly")
                    except json.JSONDecodeError as e:
                        print(f"    ✗ rules still has issues: {e}")
            
            print("\n=== JSON FIX COMPLETED ===")
            
    except Exception as e:
        print(f"Error fixing JSON issues: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_all_json_issues() 