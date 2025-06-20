#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def verify_fixes():
    db = SessionLocal()
    try:
        print("=== VERIFYING MATERIAL PRICING FIXES ===\n")

        # 1. Check material options
        print("1. Material Options (should not have base_price in choices):")
        material_options = db.query(Option).filter(Option.category == "Material").all()
        for opt in material_options:
            print(f"  {opt.name}:")
            print(f"    Choices: {opt.choices}")
            print(f"    Adders: {opt.adders}")
            print()

        # 2. Check material order for specific families
        print("2. Material Order for LS2000, LS2100, LS6000, LS7000:")
        families_to_check = ["LS2000", "LS2100", "LS6000", "LS7000"]
        for family_name in families_to_check:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if family:
                assignments = (
                    db.query(ProductFamilyOption)
                    .filter(ProductFamilyOption.product_family_id == family.id)
                    .join(Option)
                    .filter(Option.category == "Material")
                    .all()
                )
                materials = []
                for a in assignments:
                    if a.option.choices and isinstance(a.option.choices, list):
                        for choice in a.option.choices:
                            if isinstance(choice, dict):
                                materials.append(choice.get("code"))
                print(f"  {family_name}: {materials}")

        # 3. Check base prices
        print("\n3. Base Prices:")
        all_families = db.query(ProductFamily).all()
        for family in all_families:
            price_display = (
                f"${family.base_price}" if family.base_price else "Factory Pricing"
            )
            print(f"  {family.name}: {price_display}")

        # 4. Check H/TS adders for specific families
        print("\n4. H/TS Adders for LS7000/2, LS8000/2, LT9000:")
        no_adder_families = ["LS7000/2", "LS8000/2", "LT9000"]
        for family_name in no_adder_families:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if family:
                h_assignments = (
                    db.query(ProductFamilyOption)
                    .filter(ProductFamilyOption.product_family_id == family.id)
                    .join(Option)
                    .filter(Option.category == "Material")
                    .filter(Option.choices.contains([{"code": "H"}]))
                    .all()
                )
                ts_assignments = (
                    db.query(ProductFamilyOption)
                    .filter(ProductFamilyOption.product_family_id == family.id)
                    .join(Option)
                    .filter(Option.category == "Material")
                    .filter(Option.choices.contains([{"code": "TS"}]))
                    .all()
                )

                h_adder = (
                    h_assignments[0].option.adders.get("H") if h_assignments else "N/A"
                )
                ts_adder = (
                    ts_assignments[0].option.adders.get("TS")
                    if ts_assignments
                    else "N/A"
                )
                print(f"  {family_name}: H=${h_adder}, TS=${ts_adder}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    verify_fixes()
