#!/usr/bin/env python3
"""
Check the base product info for LS8000/2.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.core.database import Database
from src.core.services.product_service import ProductService


def check_ls8000_2_base_product():
    """Check the base product info for LS8000/2."""
    db = Database()
    product_service = ProductService()

    try:
        # Get all products
        products = product_service.get_products(db)

        # Find LS8000/2
        ls8000_2_product = None
        for product in products:
            if product["name"] == "LS8000/2":
                ls8000_2_product = product
                break

        if not ls8000_2_product:
            print("LS8000/2 product not found!")
            return

        print("LS8000/2 base product info:")
        print(f"  ID: {ls8000_2_product['id']}")
        print(f"  Name: {ls8000_2_product['name']}")
        print(f"  Base Price: {ls8000_2_product.get('base_price', 'Not set')}")
        print(f"  Material: {ls8000_2_product.get('material', 'Not set')}")
        print(f"  Voltage: {ls8000_2_product.get('voltage', 'Not set')}")
        print(f"  Base Length: {ls8000_2_product.get('base_length', 'Not set')}")

        # Get variants for LS8000/2
        variants = product_service.get_variants(db, ls8000_2_product["id"])
        print("\nVariants for LS8000/2:")
        for variant in variants:
            print(f"  Variant ID: {variant.id}")
            print(f"    Model Number: {variant.model_number}")
            print(f"    Base Price: {variant.base_price}")
            print(f"    Material: {variant.material}")
            print(f"    Voltage: {variant.voltage}")
            print(f"    Probe Length: {variant.probe_length}")
            print()

    except Exception as e:
        print(f"Error: {e!s}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    check_ls8000_2_base_product()
