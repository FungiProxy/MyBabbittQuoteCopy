#!/usr/bin/env python3
"""
Restore material options with correct choices and adders
"""

import json
from src.core.database import engine
from sqlalchemy import text

def restore_material_options():
    """Restore material options with correct choices and adders"""
    try:
        print("=== RESTORING MATERIAL OPTIONS ===")
        
        # Define the material options for each product family
        material_options = {
            # LS2000, LS2100, LS6000, LS7000, LS8000 families
            "LS2000": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 45, "U": 40, "T": 50}
            },
            "LS2100": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 45, "U": 40, "T": 50}
            },
            "LS6000": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 45, "U": 40, "T": 50}
            },
            "LS7000": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 45, "U": 40, "T": 50}
            },
            "LS8000": {
                "choices": [
                    {"code": "S", "display_name": "S - 316SS"},
                    {"code": "H", "display_name": "H - Hastelloy C"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "U", "display_name": "U - UHMWPE Blind Probe"},
                    {"code": "T", "display_name": "T - Teflon Blind Probe"}
                ],
                "adders": {"H": 110, "TS": 45, "U": 40, "T": 50}
            },
            # LS7000/2 and LS8000/2 families
            "LS7000/2": {
                "choices": [
                    {"code": "H", "display_name": "H - Halar Coated"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "A", "display_name": "A - Alloy 20"},
                    {"code": "HC", "display_name": "HC - Hastelloy C-276"},
                    {"code": "HB", "display_name": "HB - Hastelloy B"},
                    {"code": "TT", "display_name": "TT - Titanium"}
                ],
                "adders": {"TS": 45, "A": 85, "HC": 110, "HB": 95, "TT": 120}
            },
            "LS8000/2": {
                "choices": [
                    {"code": "H", "display_name": "H - Halar Coated"},
                    {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                    {"code": "A", "display_name": "A - Alloy 20"},
                    {"code": "HC", "display_name": "HC - Hastelloy C-276"},
                    {"code": "HB", "display_name": "HB - Hastelloy B"},
                    {"code": "TT", "display_name": "TT - Titanium"}
                ],
                "adders": {"TS": 45, "A": 85, "HC": 110, "HB": 95, "TT": 120}
            }
        }
        
        # Connect to database
        with engine.connect() as conn:
            print("\n1. Finding Material options...")
            result = conn.execute(text("SELECT id, name, product_families FROM options WHERE name = 'Material'"))
            material_options_db = result.fetchall()
            
            print(f"Found {len(material_options_db)} Material options in database")
            
            # Update each material option
            for option_id, name, product_families in material_options_db:
                print(f"\n2. Processing Material option ID {option_id}")
                print(f"   Product families: {product_families}")
                
                # Parse product families
                if product_families:
                    families = [f.strip() for f in product_families.split(',')]
                else:
                    families = []
                
                print(f"   Parsed families: {families}")
                
                # Find matching material configuration
                matching_config = None
                for family in families:
                    if family in material_options:
                        matching_config = material_options[family]
                        print(f"   Found matching config for family: {family}")
                        break
                
                if matching_config:
                    # Update the material option
                    choices_json = json.dumps(matching_config["choices"])
                    adders_json = json.dumps(matching_config["adders"])
                    
                    print(f"   Updating with choices: {matching_config['choices']}")
                    print(f"   Updating with adders: {matching_config['adders']}")
                    
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
                    print(f"   ⚠ No matching config found for families: {families}")
            
            # Commit changes
            conn.commit()
            print("\n3. All changes committed successfully!")
            
            # Verify the fix
            print("\n4. Verifying the fix...")
            result = conn.execute(text("SELECT id, name, choices, adders FROM options WHERE name = 'Material' LIMIT 3"))
            rows = result.fetchall()
            
            for row in rows:
                option_id, name, choices, adders = row
                print(f"  {name} (ID: {option_id}):")
                
                try:
                    choices_data = json.loads(choices) if choices else []
                    adders_data = json.loads(adders) if adders else {}
                    print(f"    ✓ choices: {len(choices_data)} items")
                    print(f"    ✓ adders: {len(adders_data)} items")
                except json.JSONDecodeError as e:
                    print(f"    ✗ JSON decode error: {e}")
            
            print("\n=== MATERIAL OPTIONS RESTORED ===")
            
    except Exception as e:
        print(f"Error restoring material options: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    restore_material_options() 