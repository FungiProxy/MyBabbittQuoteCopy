#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option


def check_duplicate_c_materials():
    db = SessionLocal()
    try:
        print("=== CHECKING FOR DUPLICATE C MATERIALS ===\n")

        # Get all material options
        all_material_options = (
            db.query(Option).filter(Option.category == "Material").all()
        )

        print(f"Total material options: {len(all_material_options)}")

        # Find all options that contain C code
        c_options = []
        for opt in all_material_options:
            if opt.choices and isinstance(opt.choices, list):
                for choice in opt.choices:
                    if isinstance(choice, dict) and choice.get("code") == "C":
                        c_options.append(opt)
                        break

        print(f"\nFound {len(c_options)} material options with C code:")
        for i, opt in enumerate(c_options):
            print(f"\nC Material Option {i+1}:")
            print(f"  ID: {opt.id}")
            print(f"  Name: {opt.name}")
            print(f"  Choices: {opt.choices}")
            print(f"  Adders: {opt.adders}")
            print(f"  Price: {opt.price}")

        if len(c_options) > 1:
            print(
                f"\n❌ WARNING: Found {len(c_options)} C material options! This could cause doubling."
            )
        else:
            print(f"\n✅ Only one C material option found.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    check_duplicate_c_materials()
