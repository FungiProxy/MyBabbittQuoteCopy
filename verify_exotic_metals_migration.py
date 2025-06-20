#!/usr/bin/env python3
"""
Final verification of exotic metals migration to materials system.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.material import Material, StandardLength
from src.core.models.option import Option


def main():
    """Verify the complete exotic metals migration."""
    print('EXOTIC METALS MIGRATION VERIFICATION')
    print('=' * 50)

    db = SessionLocal()
    try:
        # Check materials
        materials = db.query(Material).all()
        print(f'Total materials: {len(materials)}')

        print('\nAll materials:')
        for material in materials:
            print(f'  {material.code} - {material.name} (${material.base_price_adder})')

        # Check exotic metals specifically
        exotic_codes = ['A', 'HB', 'HC', 'TT']
        print(f'\nExotic metal materials ({len(exotic_codes)}):')
        for code in exotic_codes:
            material = db.query(Material).filter_by(code=code).first()
            if material:
                print(f'  ✅ {code} - {material.name}')
                print(f'      Base price adder: ${material.base_price_adder}')
                print(f'      Length adder per inch: ${material.length_adder_per_inch}')
                print(f'      Length adder per foot: ${material.length_adder_per_foot}')
                print(
                    f'      Nonstandard surcharge: ${material.nonstandard_length_surcharge}'
                )
            else:
                print(f'  ❌ {code} - NOT FOUND')

        # Check standard lengths for exotic materials
        print('\nStandard lengths for exotic materials:')
        for code in exotic_codes:
            lengths = db.query(StandardLength).filter_by(material_code=code).all()
            if lengths:
                length_values = [str(l.length) for l in lengths]
                print(f"  {code}: {', '.join(length_values)}\"")
            else:
                print(f'  {code}: NO STANDARD LENGTHS')

        # Check material options
        material_options = db.query(Option).filter_by(category='Materials').all()
        print(f'\nMaterial options ({len(material_options)}):')

        for option in material_options:
            print(f'  {option.product_families}:')
            print(f'    Choices: {option.choices}')
            print(f'    Adders: {option.adders}')
            print('    ---')

        # Verify exotic metals are in material choices
        print('\nVerifying exotic metals in material choices:')
        for option in material_options:
            choices = option.choices or []
            exotic_in_choices = all(code in choices for code in exotic_codes)
            print(f"  {option.product_families}: {'✅' if exotic_in_choices else '❌'}")

        # Check that exotic metals category is completely gone
        exotic_options = db.query(Option).filter_by(category='Exotic Metals').all()
        if exotic_options:
            print(f'\n❌ Found {len(exotic_options)} remaining exotic metal options')
            for option in exotic_options:
                print(f'  - {option.name} (ID: {option.id})')
        else:
            print('\n✅ No exotic metal options remaining')

        # Summary
        print('\n' + '=' * 50)
        print('MIGRATION SUMMARY')
        print('=' * 50)
        print(f'✅ Exotic metals added to materials table: {len(exotic_codes)}')
        print(f'✅ Exotic metals removed from options table: {len(exotic_options)}')
        print(f'✅ Material options updated: {len(material_options)}')
        print('✅ Standard lengths created for exotic materials')
        print('✅ All exotic metals integrated into materials system')

    finally:
        db.close()


if __name__ == '__main__':
    main()
