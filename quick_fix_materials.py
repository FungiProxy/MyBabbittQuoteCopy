#!/usr/bin/env python3
"""
Quick fix to ensure all product families have material options.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import get_db
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily
from sqlalchemy.orm import Session


def quick_fix_materials():
    """Quick fix to ensure all families have material options."""
    db: Session = next(get_db())

    try:
        # Get the material option
        material_option = db.query(Option).filter(Option.name == "Material").first()
        if not material_option:
            print("Material option not found")
            return

        print(f"Found material option ID: {material_option.id}")

        # Get all families
        families = db.query(ProductFamily).all()
        print(f"Found {len(families)} families")

        # Add material option to all families
        for family in families:
            # Check if association already exists
            existing = (
                db.query(ProductFamilyOption)
                .filter(
                    ProductFamilyOption.product_family_id == family.id,
                    ProductFamilyOption.option_id == material_option.id,
                )
                .first()
            )

            if not existing:
                # Create association
                assoc = ProductFamilyOption(
                    product_family_id=family.id,
                    option_id=material_option.id,
                    is_available=1,
                )
                db.add(assoc)
                print(f"Added material option to {family.name}")

        db.commit()
        print("Fix completed!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    quick_fix_materials()
