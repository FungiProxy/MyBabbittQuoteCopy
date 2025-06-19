#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily
from src.core.services.product_service import ProductService


def check_material_options():
    db = SessionLocal()
    try:
        print("=== CHECKING MATERIAL OPTIONS FOR SPECIFIC MODELS ===\n")

        # Check the models that should have material options
        models_to_check = ["LS2000", "LS2100", "LS6000", "LS7000"]

        for model_name in models_to_check:
            print(f"\n--- {model_name} ---")

            # Check if family exists
            family = (
                db.query(ProductFamily).filter(ProductFamily.name == model_name).first()
            )
            if not family:
                print(f"  ❌ Product family {model_name} not found!")
                continue

            print(f"  ✅ Product family found: {family.name}")

            # Check material assignments
            material_assignments = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.product_family_id == family.id)
                .join(Option)
                .filter(Option.category == "Material")
                .all()
            )

            print(f"  Material assignments: {len(material_assignments)}")

            if material_assignments:
                for assignment in material_assignments:
                    option = assignment.option
                    print(
                        f"    - {option.name}: choices={option.choices}, adders={option.adders}"
                    )
            else:
                print("    ❌ No material assignments found!")

            # Test ProductService output
            print(f"  Testing ProductService.get_additional_options():")
            product_service = ProductService()
            additional_options = product_service.get_additional_options(db, model_name)

            material_options = [
                opt for opt in additional_options if opt.get("category") == "Material"
            ]
            print(f"    Material options returned: {len(material_options)}")

            for opt in material_options:
                print(
                    f"      - {opt.get('name')}: choices={opt.get('choices')}, adders={opt.get('adders')}"
                )

        # Also check all material options in the database
        print(f"\n=== ALL MATERIAL OPTIONS IN DATABASE ===")
        all_material_options = (
            db.query(Option).filter(Option.category == "Material").all()
        )
        print(f"Total material options: {len(all_material_options)}")

        for opt in all_material_options:
            print(f"  {opt.name}: choices={opt.choices}, adders={opt.adders}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    check_material_options()
