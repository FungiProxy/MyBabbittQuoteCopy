#!/usr/bin/env python3
"""
Debug material option associations.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import get_db
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily
from sqlalchemy.orm import Session


def debug_material_associations():
    """Debug material option associations."""
    db: Session = next(get_db())

    try:
        # Check all material options
        material_options = db.query(Option).filter(Option.name == "Material").all()
        print(f"Material options found: {len(material_options)}")

        for opt in material_options:
            print(f"  ID: {opt.id}, Name: {opt.name}, Category: {opt.category}")
            print(f"  Choices: {opt.choices}")
            print(f"  Adders: {opt.adders}")

        # Check all product families
        families = db.query(ProductFamily).all()
        print(f"\nProduct families found: {len(families)}")
        for family in families:
            print(f"  ID: {family.id}, Name: {family.name}")

        # Check all associations
        associations = db.query(ProductFamilyOption).all()
        print(f"\nAll associations found: {len(associations)}")
        for assoc in associations:
            print(
                f"  Family ID: {assoc.product_family_id}, Option ID: {assoc.option_id}, Available: {assoc.is_available}"
            )

        # Check material option associations specifically
        material_associations = (
            db.query(ProductFamilyOption)
            .join(Option)
            .filter(Option.name == "Material")
            .all()
        )
        print(f"\nMaterial option associations: {len(material_associations)}")
        for assoc in material_associations:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.id == assoc.product_family_id)
                .first()
            )
            print(
                f"  Family: {family.name if family else 'Unknown'}, Available: {assoc.is_available}"
            )

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    debug_material_associations()
