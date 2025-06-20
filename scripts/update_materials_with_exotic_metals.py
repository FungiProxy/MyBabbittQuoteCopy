"""
Script to update material options to include exotic metals in the material dropdown.
This integrates exotic metals into the material selection instead of keeping them separate.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.core.database import SessionLocal
from src.core.models.option import Option


def update_materials_with_exotic_metals():
    """Update material options to include exotic metals."""
    db = SessionLocal()
    try:
        print("Updating material options to include exotic metals...")

        # Define exotic metals
        exotic_metals = ["Alloy 20", "Hastelloy-C-276", "Hastelloy-B", "Titanium"]

        # Get all material options
        material_options = (
            db.query(Option)
            .filter(Option.name == "Material", Option.category == "Material")
            .all()
        )

        updated_count = 0
        for option in material_options:
            print(f"Processing {option.product_families}...")

            # Add exotic metals to choices if not already present
            current_choices = option.choices if isinstance(option.choices, list) else []
            updated_choices = current_choices.copy()

            for exotic in exotic_metals:
                if exotic not in updated_choices:
                    updated_choices.append(exotic)

            # Add exotic metals to adders with 0 value (manual override)
            current_adders = option.adders if isinstance(option.adders, dict) else {}
            updated_adders = current_adders.copy()

            for exotic in exotic_metals:
                if exotic not in updated_adders:
                    updated_adders[exotic] = 0  # Manual override pricing

            # Update the option
            option.choices = updated_choices
            option.adders = updated_adders
            updated_count += 1

            print(f"  Added exotic metals to {option.product_families}")

        # Remove the separate exotic metal options since they're now integrated
        exotic_metal_options = (
            db.query(Option).filter(Option.category == "Exotic Metal").all()
        )

        removed_count = 0
        for exotic_option in exotic_metal_options:
            print(f"Removing separate exotic metal option: {exotic_option.name}")
            db.delete(exotic_option)
            removed_count += 1

        db.commit()
        print("\nUpdate complete!")
        print(f"Updated {updated_count} material options")
        print(f"Removed {removed_count} separate exotic metal options")
        print(
            "\nExotic metals are now integrated into the material dropdown with manual override pricing."
        )

    except Exception as e:
        print(f"Error updating materials: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    update_materials_with_exotic_metals()
