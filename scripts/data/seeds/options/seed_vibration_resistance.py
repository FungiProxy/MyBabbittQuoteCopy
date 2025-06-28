"""
Seed file for Vibration Resistance accessory option.
This option is available for all product families with a $50 adder.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.option import Option


def seed_vibration_resistance():
    """Seed the Vibration Resistance accessory option."""
    db = SessionLocal()

    try:
        # Get all product family names
        from src.core.models.product_variant import ProductFamily
        product_families = db.query(ProductFamily).all()
        family_names = [str(family.name) for family in product_families]

        # Create Vibration Resistance option
        vibration_resistance_option = Option(
            name="Vibration Resistance",
            description="Vibration resistance feature for enhanced durability",
            price=0.0,
            price_type="fixed",
            category="Accessories",
            choices=["VR"],
            adders={
                "True": 50.0,  # $50 adder for Vibration Resistance when checked
            },
            product_families=",".join(family_names),  # Available for all product families
        )

        # Check if option already exists
        existing_option = db.query(Option).filter_by(
            name="Vibration Resistance",
            category="Accessories"
        ).first()

        if existing_option:
            print("Vibration Resistance option already exists, skipping...")
        else:
            db.add(vibration_resistance_option)
            db.commit()
            print(f"Added Vibration Resistance option for {len(family_names)} product families")

    except Exception as e:
        print(f"Error seeding Vibration Resistance option: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_vibration_resistance() 