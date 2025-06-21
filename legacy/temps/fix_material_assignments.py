#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def fix_material_assignments():
    db = SessionLocal()
    try:
        print("Fixing material assignments for specific models...")

        # Define the correct material order and families to fix
        families_to_fix = ["LS2000", "LS2100", "LS6000", "LS7000"]
        correct_order = ["S", "H", "TS", "U", "T", "C"]

        for family_name in families_to_fix:
            print(f"\nProcessing {family_name}...")

            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if not family:
                print(f"  ❌ Product family {family_name} not found!")
                continue

            # Remove any existing material assignments for this family
            existing_assignments = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.product_family_id == family.id)
                .join(Option)
                .filter(Option.category == "Material")
                .all()
            )

            if existing_assignments:
                print(
                    f"  Removing {len(existing_assignments)} existing material assignments..."
                )
                for assignment in existing_assignments:
                    db.delete(assignment)

            # Add material assignments in correct order
            print(f"  Adding material assignments in order: {correct_order}")
            for material_code in correct_order:
                # Find the material option that contains this code (manual search)
                material_option = None
                all_material_options = (
                    db.query(Option).filter(Option.category == "Material").all()
                )
                for opt in all_material_options:
                    if opt.choices and isinstance(opt.choices, list):
                        for choice in opt.choices:
                            if (
                                isinstance(choice, dict)
                                and choice.get("code") == material_code
                            ):
                                material_option = opt
                                break
                    if material_option:
                        break
                if material_option:
                    # Create the assignment
                    assignment = ProductFamilyOption(
                        product_family_id=family.id,
                        option_id=material_option.id,
                        is_available=1,
                    )
                    db.add(assignment)
                    print(f"    ✅ Added {material_code} ({material_option.name})")
                else:
                    print(f"    ❌ Material option for {material_code} not found!")

            db.commit()
            print(f"  ✅ Completed {family_name}")

        # Verify the fixes
        print("\n=== VERIFYING FIXES ===")
        for family_name in families_to_fix:
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
                for assignment in assignments:
                    if assignment.option.choices and isinstance(
                        assignment.option.choices, list
                    ):
                        for choice in assignment.option.choices:
                            if isinstance(choice, dict):
                                materials.append(choice.get("code"))

                print(
                    f"  {family_name}: {len(assignments)} assignments, materials: {materials}"
                )

        print("\nMaterial assignments fixed!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_material_assignments()
