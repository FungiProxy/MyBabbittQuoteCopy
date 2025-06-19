#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily
from src.core.services.product_service import ProductService


def check_ls8000_materials():
    db = SessionLocal()
    try:
        print("=== CHECKING LS8000 MATERIALS ===\n")

        # Check if LS8000 family exists
        family = db.query(ProductFamily).filter(ProductFamily.name == "LS8000").first()
        if not family:
            print("❌ LS8000 product family not found!")
            return

        print(f"✅ LS8000 product family found (ID: {family.id})")

        # Check current material assignments
        material_assignments = (
            db.query(ProductFamilyOption)
            .filter(ProductFamilyOption.product_family_id == family.id)
            .join(Option)
            .filter(Option.category == "Material")
            .all()
        )

        print(f"\nCurrent material assignments: {len(material_assignments)}")

        current_materials = []
        for assignment in material_assignments:
            option = assignment.option
            if option.choices and isinstance(option.choices, list):
                for choice in option.choices:
                    if isinstance(choice, dict):
                        current_materials.append(choice.get("code"))

        print(f"Current materials: {current_materials}")

        # Test ProductService output
        print(f"\n=== PRODUCT SERVICE OUTPUT ===")
        product_service = ProductService()
        additional_options = product_service.get_additional_options(db, "LS8000")
        material_options = [
            opt for opt in additional_options if opt.get("category") == "Material"
        ]

        print(f"Material options returned: {len(material_options)}")
        for opt in material_options:
            print(
                f"  - {opt.get('name')}: choices={opt.get('choices')}, adders={opt.get('adders')}"
            )

        # Check what materials should be available
        print(f"\n=== WHAT SHOULD BE AVAILABLE ===")
        print("LS8000 should have: S, H, TS, U, T, C")
        print(f"Currently has: {current_materials}")

        missing_materials = []
        required_materials = ["S", "H", "TS", "U", "T", "C"]
        for material in required_materials:
            if material not in current_materials:
                missing_materials.append(material)

        if missing_materials:
            print(f"Missing materials: {missing_materials}")
        else:
            print("✅ All required materials are available")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    check_ls8000_materials()
