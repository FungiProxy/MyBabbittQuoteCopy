#!/usr/bin/env python3
"""
Fix material adders - TS should be $110 base adder, and ensure U/T have proper length adders
"""

import json
from src.core.database import engine
from sqlalchemy import text

def fix_material_adders():
    """Fix material adders in the database"""
    try:
        print("=== FIXING MATERIAL ADDERS ===")
        
        # Define the correct material adders for each product family
        material_adders = {
            # LS2000, LS2100, LS6000, LS7000, LS8000 families
            "LS2000": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 110, "U": 40, "T": 50}  # TS is now $110
            },
            "LS2100": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 110, "U": 40, "T": 50}  # TS is now $110
            },
            "LS6000": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 110, "U": 40, "T": 50}  # TS is now $110
            },
            "LS7000": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 110, "U": 40, "T": 50}  # TS is now $110
            },
            "LS8000": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 110, "U": 40, "T": 50}  # TS is now $110
            }
        }
        
        # Connect to database
        with engine.connect() as conn:
            print("\n1. Updating material adders...")
            
            # Update each material option
            for family_name, config in material_adders.items():
                print(f"\n2. Processing family: {family_name}")
                
                # Find the material option for this family
                result = conn.execute(
                    text("SELECT id FROM options WHERE name = 'Material' AND product_families LIKE :family"),
                    {"family": f"%{family_name}%"}
                )
                row = result.fetchone()
                
                if row:
                    option_id = row[0]
                    choices_json = json.dumps(config["choices"])
                    adders_json = json.dumps(config["adders"])
                    
                    print(f"   Found option ID {option_id}")
                    print(f"   Updating adders: {config['adders']}")
                    
                    conn.execute(
                        text("UPDATE options SET choices = :choices, adders = :adders WHERE id = :id"),
                        {
                            "choices": choices_json,
                            "adders": adders_json,
                            "id": option_id
                        }
                    )
                    print(f"   ✓ Updated Material option ID {option_id}")
                else:
                    print(f"   ⚠ No material option found for family: {family_name}")
            
            # Commit changes
            conn.commit()
            print("\n3. All changes committed successfully!")
            
            # Verify the fix
            print("\n4. Verifying the fix...")
            result = conn.execute(text("SELECT id, name, choices, adders, product_families FROM options WHERE name = 'Material'"))
            rows = result.fetchall()
            
            for row in rows:
                option_id, name, choices, adders, product_families = row
                print(f"\nMaterial option ID {option_id} for families: {product_families}")
                
                try:
                    choices_data = json.loads(choices) if choices else []
                    adders_data = json.loads(adders) if adders else {}
                    
                    # Check specific materials
                    for choice in choices_data:
                        if isinstance(choice, dict) and 'code' in choice:
                            code = choice['code']
                            display_name = choice.get('display_name', 'Unknown')
                            adder = adders_data.get(code, 0)
                            print(f"    {code} ({display_name}): ${adder}")
                    
                except json.JSONDecodeError as e:
                    print(f"  ✗ JSON decode error: {e}")
            
            print("\n=== MATERIAL ADDERS FIXED ===")
            
    except Exception as e:
        print(f"Error fixing material adders: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_material_adders() 