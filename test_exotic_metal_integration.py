"""
Test script to verify exotic metal integration into material dropdown.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))

from src.core.database import SessionLocal
from src.core.models.option import Option


def test_exotic_metal_integration():
    """Test that exotic metals are properly integrated into material options."""
    db = SessionLocal()
    try:
        print('Testing exotic metal integration...')

        # Get all material options
        material_options = (
            db.query(Option)
            .filter(Option.name == 'Material', Option.category == 'Material')
            .all()
        )

        exotic_metals = ['Alloy 20', 'Hastelloy-C-276', 'Hastelloy-B', 'Titanium']

        print(f'\nFound {len(material_options)} material options:')

        for option in material_options:
            print(f'\nProduct Families: {option.product_families}')
            print(f'Choices: {option.choices}')
            print(f'Adders: {option.adders}')

            # Check if exotic metals are included
            missing_exotics = []
            for exotic in exotic_metals:
                if exotic not in option.choices:
                    missing_exotics.append(exotic)

            if missing_exotics:
                print(f'  ❌ Missing exotic metals: {missing_exotics}')
            else:
                print('  ✅ All exotic metals present')

            # Check if exotic metals have 0 adders (manual override)
            exotic_adders = {
                k: v for k, v in option.adders.items() if k in exotic_metals
            }
            print(f'  Exotic metal adders: {exotic_adders}')

            # Verify all exotic metals have 0 adders
            non_zero_adders = {k: v for k, v in exotic_adders.items() if v != 0}
            if non_zero_adders:
                print(f'  ⚠️  Non-zero adders for exotic metals: {non_zero_adders}')
            else:
                print('  ✅ All exotic metals have 0 adders (manual override)')

        # Check that separate exotic metal options are removed
        exotic_metal_options = (
            db.query(Option).filter(Option.category == 'Exotic Metal').all()
        )

        if exotic_metal_options:
            print(
                f'\n❌ Found {len(exotic_metal_options)} separate exotic metal options (should be 0)'
            )
            for option in exotic_metal_options:
                print(f'  - {option.name} for {option.product_families}')
        else:
            print('\n✅ No separate exotic metal options found (correct)')

        print('\nTest complete!')

    except Exception as e:
        print(f'Error testing exotic metal integration: {e}')
    finally:
        db.close()


if __name__ == '__main__':
    test_exotic_metal_integration()
