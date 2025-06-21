#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily
from src.core.services.product_service import ProductService


def check_cpvc_material():
    db = SessionLocal()
    try:
        print("=== CHECKING CPVC MATERIAL STATUS ===\n")

        # First, check if CPVC material option exists in the database
        cpvc_option = None
        all_material_options = (
            db.query(Option).filter(Option.category == "Material").all()
        )

        print("All material options in database:")
        for opt in all_material_options:
            if opt.choices and isinstance(opt.choices, list):
                for choice in opt.choices:
                    if isinstance(choice, dict):
                        code = choice.get("code")
                        if code == "CPVC":
                            cpvc_option = opt
                        print(f"  - {opt.name}: code={code}, adders={opt.adders}")

        if cpvc_option:
            print("\n✅ CPVC material option found:")
            print(f"  Choices: {cpvc_option.choices}")
            print(f"  Adders: {cpvc_option.adders}")
        else:
            print("\n❌ CPVC material option not found in database!")
            return

        # Check which product families have CPVC assigned
        print("\n=== CPVC ASSIGNMENTS ===")
        cpvc_assignments = (
            db.query(ProductFamilyOption)
            .filter(ProductFamilyOption.option_id == cpvc_option.id)
            .all()
        )

        families_with_cpvc = []
        for assignment in cpvc_assignments:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.id == assignment.product_family_id)
                .first()
            )
            if family:
                families_with_cpvc.append(family.name)

        print(f"Product families with CPVC assigned: {families_with_cpvc}")

        # Check all product families to see which ones should have CPVC
        print("\n=== CHECKING ALL PRODUCT FAMILIES ===")
        all_families = db.query(ProductFamily).all()

        for family in all_families:
            print(f"\n--- {family.name} ---")

            # Get material assignments for this family
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

            print(f"  Current materials: {sorted(current_materials)}")

            # Check if CPVC should be available for this family
            # Based on typical usage, CPVC is usually available for most families
            if "CPVC" not in current_materials:
                print(f"  ❌ CPVC missing from {family.name}")
            else:
                print(f"  ✅ CPVC available for {family.name}")

        # Test ProductService for a few families
        print("\n=== PRODUCT SERVICE TEST ===")
        test_families = ["LS2000", "LS6000", "LS7000", "LS8000"]

        product_service = ProductService()
        for family_name in test_families:
            additional_options = product_service.get_additional_options(db, family_name)
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
                                f"  ✅ {family_name}: CPVC available (adder: ${opt.get('adders', {}).get('CPVC', 0):.2f})"
                            )
                            break
                    if cpvc_found:
                        break

            if not cpvc_found:
                print(f"  ❌ {family_name}: CPVC not available")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    check_cpvc_material()
