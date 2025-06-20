#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService


def debug_material_pricing():
    db = SessionLocal()
    try:
        ps = ProductService()

        # Check what material options are returned for LS2000
        print('=== Material Options for LS2000 ===')
        options = ps.get_additional_options(db, 'LS2000')
        material_options = [opt for opt in options if opt.get('name') == 'Material']

        for i, opt in enumerate(material_options):
            print(f'Material Option {i+1}:')
            print(f"  Name: {opt.get('name')}")
            print(f"  Category: {opt.get('category')}")
            print(f"  Choices: {opt.get('choices')}")
            print(f"  Adders: {opt.get('adders')}")
            print(f"  Excluded Products: {opt.get('excluded_products')}")
            print()

        # Test specific material lookups
        print('=== Testing Material Adder Lookups ===')
        if material_options:
            adders = material_options[0].get('adders', {})
            test_materials = ['S', 'H', 'TS', 'HC', 'CPVC']

            for material in test_materials:
                if material in adders:
                    print(f'  {material}: ${adders[material]}')
                else:
                    print(f'  {material}: NOT FOUND in adders')

    finally:
        db.close()


if __name__ == '__main__':
    debug_material_pricing()
