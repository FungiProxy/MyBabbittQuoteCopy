#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option
from src.core.services.product_service import ProductService


def check_c_material():
    db = SessionLocal()
    try:
        print("=== CHECKING C MATERIAL PRICING ===\n")

        # Check the C material option directly
        c_material_option = (
            db.query(Option)
            .filter(
                Option.category == "Material", Option.choices.contains([{"code": "C"}])
            )
            .first()
        )

        if c_material_option:
            print("C Material Option:")
            print(f"  Name: {c_material_option.name}")
            print(f"  Choices: {c_material_option.choices}")
            print(f"  Adders: {c_material_option.adders}")
            print(f"  Price: {c_material_option.price}")
            print(f"  Price Type: {c_material_option.price_type}")
        else:
            print("❌ C material option not found!")

        # Check all material options to see if there are duplicates
        print("\n=== ALL MATERIAL OPTIONS ===")
        all_material_options = (
            db.query(Option).filter(Option.category == "Material").all()
        )

        for i, opt in enumerate(all_material_options):
            print(f"\nMaterial Option {i+1}:")
            print(f"  Name: {opt.name}")
            print(f"  Choices: {opt.choices}")
            print(f"  Adders: {opt.adders}")
            print(f"  Price: {opt.price}")
            print(f"  Price Type: {opt.price_type}")

        # Test ProductService output for a family that has C material
        print("\n=== TESTING PRODUCT SERVICE ===")
        product_service = ProductService()
        test_family = "LS2000"  # Should have C material

        additional_options = product_service.get_additional_options(db, test_family)
        material_options = [
            opt for opt in additional_options if opt.get("category") == "Material"
        ]

        print(f"Material options returned for {test_family}: {len(material_options)}")
        for opt in material_options:
            print(
                f"  - {opt.get('name')}: choices={opt.get('choices')}, adders={opt.get('adders')}"
            )

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    check_c_material()
