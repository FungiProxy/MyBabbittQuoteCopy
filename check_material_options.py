#!/usr/bin/env python3
"""
Check material options for different families.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.services.product_service import ProductService
from src.core.database import get_db


def check_material_options():
    """Check material options for different families."""
    db = next(get_db())
    ps = ProductService()

    try:
        # Get all families
        families = ps.get_product_families(db)
        print("Families:")
        for f in families:
            print(f"  {f['name']}")

        # Check materials for different families
        test_families = ["LS2000", "LS8000", "LS8500", "FS10000"]

        for family_name in test_families:
            print(f"\nMaterials for {family_name}:")
            materials = ps.get_available_materials_for_product(db, family_name)
            print(f"  {len(materials)} material options")

            for material in materials:
                print(f"    Name: {material['name']}")
                print(f"    Choices: {material['choices']}")
                print(f"    Adders: {material['adders']}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    check_material_options()
