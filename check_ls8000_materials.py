#!/usr/bin/env python3
"""
Check LS8000 and LS8000/2 material options specifically.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.services.product_service import ProductService
from src.core.database import get_db


def check_ls8000_materials():
    """Check LS8000 and LS8000/2 material options."""
    db = next(get_db())
    ps = ProductService()

    try:
        # Check LS8000
        print("LS8000 materials:")
        materials = ps.get_available_materials_for_product(db, "LS8000")
        print(f"  {len(materials)} material options")
        for material in materials:
            print(f"    Name: {material['name']}")
            print(f"    Choices: {material['choices']}")
            print(f"    Adders: {material['adders']}")

        # Check LS8000/2
        print("\nLS8000/2 materials:")
        materials = ps.get_available_materials_for_product(db, "LS8000/2")
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
    check_ls8000_materials()
