#!/usr/bin/env python3
"""
Fix the material options structure by removing the generic ALL materials entry
and ensuring each family has proper individual material options.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "./")))

from src.core.database import SessionLocal
from src.core.models.option import Option


def fix_material_structure():
    """Fix the material options structure."""
    db = SessionLocal()
    try:
        print("=== FIXING MATERIAL STRUCTURE ===")

        # 1. Remove the generic ALL materials option (ID: 1)
        generic_option = (
            db.query(Option).filter(Option.id == 1, Option.name == "Material").first()
        )
        if generic_option:
            print(f"Removing generic material option (ID: {generic_option.id})")
            db.delete(generic_option)
            db.commit()
            print("✓ Removed generic material option")
        else:
            print("No generic material option found")

        # 2. Check and fix each family's material options
        family_materials = {
            "LS2000": {
                "choices": ["S", "H", "U", "T", "C"],
                "adders": {"S": 0, "H": 110, "U": 20, "T": 60, "C": 80},
            },
            "LS2100": {
                "choices": ["S", "H", "U", "T", "C"],
                "adders": {"S": 0, "H": 110, "U": 20, "T": 60, "C": 80},
            },
            "LS6000": {
                "choices": ["S", "H", "U", "T", "C"],
                "adders": {"S": 0, "H": 110, "U": 20, "T": 60, "C": 80},
            },
            "LS7000": {
                "choices": ["S", "H", "U", "T", "C"],
                "adders": {"S": 0, "H": 110, "U": 20, "T": 60, "C": 80},
            },
            "LS7000/2": {
                "choices": ["S", "H", "U", "T", "C"],
                "adders": {"S": 0, "H": 110, "U": 20, "T": 60, "C": 80},
            },
            "LS8000": {
                "choices": [
                    "S",
                    "H",
                    "TS",
                    "U",
                    "T",
                    "C",
                    "CPVC",
                    "A",
                    "HC",
                    "HB",
                    "TT",
                ],
                "adders": {
                    "S": 0,
                    "H": 110,
                    "TS": 110,
                    "U": 20,
                    "T": 60,
                    "C": 80,
                    "CPVC": 0,
                    "A": 0,
                    "HC": 0,
                    "HB": 0,
                    "TT": 0,
                },
            },
            "LS8000/2": {
                "choices": [
                    "S",
                    "H",
                    "TS",
                    "U",
                    "T",
                    "C",
                    "CPVC",
                    "A",
                    "HC",
                    "HB",
                    "TT",
                ],
                "adders": {
                    "S": 0,
                    "H": 110,
                    "TS": 110,
                    "U": 20,
                    "T": 60,
                    "C": 80,
                    "CPVC": 0,
                    "A": 0,
                    "HC": 0,
                    "HB": 0,
                    "TT": 0,
                },
            },
            "LT9000": {
                "choices": ["S", "H", "U", "T", "C"],
                "adders": {"S": 0, "H": 110, "U": 20, "T": 60, "C": 80},
            },
            "FS10000": {
                "choices": ["S", "H", "U", "T", "C"],
                "adders": {"S": 0, "H": 110, "U": 20, "T": 60, "C": 80},
            },
            "LS7500": {
                "choices": ["S", "A", "HC", "HB", "TT"],
                "adders": {"S": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0},
            },
            "LS8500": {
                "choices": ["S", "A", "HC", "HB", "TT"],
                "adders": {"S": 0, "A": 0, "HC": 0, "HB": 0, "TT": 0},
            },
        }

        # Update each family's material option
        for family_name, materials in family_materials.items():
            # Find the material option for this family using string search
            option = db.query(Option).filter(Option.name == "Material").all()

            # Find the one that matches this family
            target_option = None
            for opt in option:
                if hasattr(opt, "product_families") and opt.product_families:
                    if isinstance(opt.product_families, list):
                        family_list = [pf.name for pf in opt.product_families]
                    else:
                        family_list = str(opt.product_families).split(",")

                    if family_name in family_list:
                        target_option = opt
                        break

            if target_option:
                print(f"\nUpdating {family_name}:")
                print(f"  Old choices: {target_option.choices}")
                print(f"  New choices: {materials['choices']}")
                print(f"  Old adders: {target_option.adders}")
                print(f"  New adders: {materials['adders']}")

                # Update with simple string choices and proper adders
                target_option.choices = materials["choices"]
                target_option.adders = materials["adders"]

                print(f"  ✓ Updated {family_name}")
            else:
                print(f"  ❌ No material option found for {family_name}")

        db.commit()
        print(f"\n✓ Material structure fixed!")

        # 3. Verify the fix
        print(f"\n=== VERIFICATION ===")
        material_options = db.query(Option).filter(Option.name == "Material").all()
        print(f"Found {len(material_options)} material options:")

        for option in material_options:
            print(f"\n{option.product_families}:")
            print(f"  Choices: {option.choices}")
            print(f"  Adders: {option.adders}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_material_structure()
