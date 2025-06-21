#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def fix_cpvc_assignments():
    db = SessionLocal()
    try:
        print("Fixing CPVC material assignments...")

        # Find the CPVC material option
        cpvc_option = None
        all_material_options = (
            db.query(Option).filter(Option.category == "Material").all()
        )
        for opt in all_material_options:
            if opt.choices and isinstance(opt.choices, list):
                for choice in opt.choices:
                    if isinstance(choice, dict) and choice.get("code") == "CPVC":
                        cpvc_option = opt
                        break
                if cpvc_option:
                    break

        if not cpvc_option:
            print("❌ CPVC material option not found!")
            return

        print(f"✅ Found CPVC material option (ID: {cpvc_option.id})")

        # Define which families should have CPVC (only LS6000 and LS7000)
        families_should_have_cpvc = ["LS6000", "LS7000"]

        # Define which families should NOT have CPVC (remove from these)
        families_should_not_have_cpvc = ["LS2000", "LS2100", "LS8000"]

        print(f"CPVC should be available for: {families_should_have_cpvc}")
        print(f"CPVC should be removed from: {families_should_not_have_cpvc}")

        # Remove CPVC from families that shouldn't have it
        print("\n=== REMOVING CPVC FROM INCORRECT FAMILIES ===")
        for family_name in families_should_not_have_cpvc:
            print(f"\nProcessing {family_name}...")

            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if not family:
                print(f"  ⚠️  Family {family_name} not found!")
                continue

            # Find and remove CPVC assignment
            cpvc_assignment = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.product_family_id == family.id)
                .filter(ProductFamilyOption.option_id == cpvc_option.id)
                .first()
            )

            if cpvc_assignment:
                db.delete(cpvc_assignment)
                print(f"  ✅ Removed CPVC from {family_name}")
            else:
                print(f"  ⚠️  CPVC not assigned to {family_name} (already correct)")

        # Verify CPVC is still available for families that should have it
        print("\n=== VERIFYING CPVC FOR CORRECT FAMILIES ===")
        for family_name in families_should_have_cpvc:
            print(f"\nChecking {family_name}...")

            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if not family:
                print(f"  ❌ Family {family_name} not found!")
                continue

            # Check if CPVC is assigned
            cpvc_assignment = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.product_family_id == family.id)
                .filter(ProductFamilyOption.option_id == cpvc_option.id)
                .first()
            )

            if cpvc_assignment:
                print(f"  ✅ CPVC correctly assigned to {family_name}")
            else:
                print(f"  ❌ CPVC missing from {family_name} - adding it...")
                # Add CPVC assignment
                assignment = ProductFamilyOption(
                    product_family_id=family.id,
                    option_id=cpvc_option.id,
                    is_available=1,
                )
                db.add(assignment)
                print(f"    ✅ Added CPVC to {family_name}")

        db.commit()
        print("\n✅ Successfully fixed CPVC assignments")

        # Final verification
        print("\n=== FINAL VERIFICATION ===")
        all_families = db.query(ProductFamily).all()

        for family in all_families:
            material_assignments = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.product_family_id == family.id)
                .join(Option)
                .filter(Option.category == "Material")
                .all()
            )

            current_materials = []
            for assignment in material_assignments:
                option = assignment.option
                if option.choices and isinstance(option.choices, list):
                    for choice in option.choices:
                        if isinstance(choice, dict):
                            current_materials.append(choice.get("code"))

            cpvc_status = "✅" if "CPVC" in current_materials else "❌"
            should_have_cpvc = family.name in families_should_have_cpvc
            status = (
                "CORRECT"
                if (should_have_cpvc and "CPVC" in current_materials)
                or (not should_have_cpvc and "CPVC" not in current_materials)
                else "INCORRECT"
            )

            print(f"{family.name}: {cpvc_status} CPVC - {status}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_cpvc_assignments()
