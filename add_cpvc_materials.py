#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def add_cpvc_materials():
    db = SessionLocal()
    try:
        print("Adding CPVC material to appropriate product families...")

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
        print(f"CPVC adder: ${cpvc_option.adders.get('CPVC', 0):.2f}")

        # Define which families should have CPVC
        # CPVC is typically available for families that support blind-end materials
        families_to_add_cpvc = ["LS2000", "LS2100", "LS6000", "LS7000", "LS8000"]

        print(f"\nAdding CPVC to families: {families_to_add_cpvc}")

        for family_name in families_to_add_cpvc:
            print(f"\nProcessing {family_name}...")

            # Get the family
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if not family:
                print(f"  ❌ Family {family_name} not found!")
                continue

            # Check if CPVC is already assigned
            existing_assignment = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.product_family_id == family.id)
                .filter(ProductFamilyOption.option_id == cpvc_option.id)
                .first()
            )

            if existing_assignment:
                print(f"  ⚠️  CPVC already assigned to {family_name}")
            else:
                # Create the assignment
                assignment = ProductFamilyOption(
                    product_family_id=family.id,
                    option_id=cpvc_option.id,
                    is_available=1,
                )
                db.add(assignment)
                print(f"  ✅ Added CPVC to {family_name}")

        db.commit()
        print("\n✅ Successfully added CPVC materials")

        # Verify the changes
        print("\n=== VERIFICATION ===")
        for family_name in families_to_add_cpvc:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if family:
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

                print(f"{family_name}: {sorted(current_materials)}")

        # Test ProductService for one family
        print("\n=== PRODUCT SERVICE TEST ===")
        from src.core.services.product_service import ProductService

        product_service = ProductService()

        test_family = "LS2000"
        additional_options = product_service.get_additional_options(db, test_family)
        material_options = [
            opt for opt in additional_options if opt.get("category") == "Material"
        ]

        cpvc_found = False
        for opt in material_options:
            if opt.get("choices") and isinstance(opt.get("choices"), list):
                for choice in opt.get("choices"):
                    if isinstance(choice, dict) and choice.get("code") == "CPVC":
                        cpvc_found = True
                        print(
                            f"✅ {test_family}: CPVC available (adder: ${opt.get('adders', {}).get('CPVC', 0):.2f})"
                        )
                        break
                if cpvc_found:
                    break

        if not cpvc_found:
            print(f"❌ {test_family}: CPVC still not available")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_cpvc_materials()
