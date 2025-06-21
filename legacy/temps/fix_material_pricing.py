#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def fix_material_pricing():
    db = SessionLocal()
    try:
        print("Fixing material pricing issues...")

        # 1. Fix material options - remove base_price from choices, keep only adders
        material_options = db.query(Option).filter(Option.category == "Material").all()
        for opt in material_options:
            if opt.choices and isinstance(opt.choices, list):
                updated_choices = []
                for choice in opt.choices:
                    if isinstance(choice, dict):
                        # Remove base_price, keep only code and display_name
                        updated_choice = {
                            "code": choice.get("code"),
                            "display_name": choice.get("display_name"),
                        }
                        updated_choices.append(updated_choice)
                opt.choices = updated_choices
                print(f"  Updated {opt.name}: removed base_price from choices")

        # 2. Fix adders for specific materials
        # C should be 80, H should be 110, TS should be 110, others as they are
        for opt in material_options:
            if opt.choices and isinstance(opt.choices, list):
                for choice in opt.choices:
                    if isinstance(choice, dict):
                        code = choice.get("code")
                        if code == "C":
                            opt.adders = {"C": 80.0}
                        elif code == "H":
                            opt.adders = {"H": 110.0}
                        elif code == "TS":
                            opt.adders = {"TS": 110.0}
                        elif code == "T":
                            opt.adders = {"T": 60.0}
                        elif code == "U":
                            opt.adders = {"U": 20.0}
                        elif code == "S":
                            opt.adders = {"S": 0.0}
                        elif code == "CPVC":
                            opt.adders = {"CPVC": 400.0}

        db.commit()
        print("Material pricing fixed!")

        # 3. Fix material order for specific families
        families_to_fix = ["LS2000", "LS2100", "LS6000", "LS7000"]
        correct_order = ["S", "H", "TS", "U", "T", "C"]

        for family_name in families_to_fix:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if family:
                # Remove current material assignments
                assignments = (
                    db.query(ProductFamilyOption)
                    .filter(ProductFamilyOption.product_family_id == family.id)
                    .join(Option)
                    .filter(Option.category == "Material")
                    .all()
                )
                for a in assignments:
                    db.delete(a)

                # Add in correct order
                for material_code in correct_order:
                    material_option = (
                        db.query(Option)
                        .filter(
                            Option.category == "Material",
                            Option.choices.contains([{"code": material_code}]),
                        )
                        .first()
                    )
                    if material_option:
                        db.add(
                            ProductFamilyOption(
                                product_family_id=family.id,
                                option_id=material_option.id,
                                is_available=1,
                            )
                        )
                        print(f"  Added {material_code} to {family_name}")

                db.commit()
                print(f"  Fixed material order for {family_name}")

        # 4. Fix H and TS adders for specific families (no adders for LS7000/2, LS8000/2, LT9000)
        no_adder_families = ["LS7000/2", "LS8000/2", "LT9000"]
        for family_name in no_adder_families:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if family:
                # Find H and TS material options for this family
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

                # Update the adders for these specific assignments
                for assignment in h_assignments + ts_assignments:
                    if assignment.option.choices and isinstance(
                        assignment.option.choices, list
                    ):
                        for choice in assignment.option.choices:
                            if isinstance(choice, dict):
                                code = choice.get("code")
                                if code in ["H", "TS"]:
                                    assignment.option.adders = {code: 0.0}

                print(f"  Fixed H/TS adders for {family_name}")

        db.commit()
        print("All material pricing issues fixed!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_material_pricing()
