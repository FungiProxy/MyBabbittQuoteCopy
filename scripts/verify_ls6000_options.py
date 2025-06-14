import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal, init_db
from src.core.models.option import Option


def verify_ls6000_options():
    """Verify and fix LS6000 options in the database."""
    db = SessionLocal()
    try:
        # Check if Material option exists for LS6000
        material_option = (
            db.query(Option)
            .filter(Option.name == "Material", Option.product_families.like("%LS6000%"))
            .first()
        )

        if not material_option:
            print("Material option not found for LS6000. Creating it...")
            material_option = Option(
                name="Material",
                description="Probe material",
                product_families="LS6000",
                price=0.0,
                price_type="fixed",
                category="Mechanical",
                choices=["S", "H", "TS", "CPVC"],
                adders={"S": 0, "H": 110, "TS": 110, "CPVC": 400},
                rules=None,
                excluded_products="",
            )
            db.add(material_option)
            db.commit()
            print("Material option created successfully.")
        else:
            print("Material option found. Verifying CPVC adder...")
            if "CPVC" not in material_option.choices:
                print("Adding CPVC to choices...")
                material_option.choices.append("CPVC")

            if material_option.adders.get("CPVC") != 400:
                print("Setting CPVC adder to 400...")
                material_option.adders["CPVC"] = 400

            db.commit()
            print("Material option updated successfully.")

        # Print the current state
        print("\nCurrent Material option state:")
        print(f"Choices: {material_option.choices}")
        print(f"Adders: {material_option.adders}")

    finally:
        db.close()


if __name__ == "__main__":
    verify_ls6000_options()
