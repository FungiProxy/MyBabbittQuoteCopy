#!/usr/bin/env python3
"""
Reseed Material Options Script
Uses the configuration file to restore correct material options for each product family.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))

from material_options_config import MATERIAL_OPTIONS_CONFIG
from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def reseed_material_options():
    """Reseed material options using the configuration."""
    db = SessionLocal()
    try:
        print('=== RESEEDING MATERIAL OPTIONS ===')

        # First, remove all existing material options
        existing_materials = db.query(Option).filter(Option.name == 'Material').all()
        print(f'Removing {len(existing_materials)} existing material options...')

        for option in existing_materials:
            db.delete(option)

        db.commit()
        print('✓ Removed existing material options')

        # Get all product families
        product_families = db.query(ProductFamily).all()
        family_map = {pf.name: pf for pf in product_families}

        # Now create new material options for each family
        created_count = 0
        for family_name, config in MATERIAL_OPTIONS_CONFIG.items():
            print(f'\nCreating material option for {family_name}:')
            print(f"  Choices: {config['choices']}")
            print(f"  Adders: {config['adders']}")

            # Check if product family exists
            if family_name not in family_map:
                print(f'  ❌ Product family {family_name} not found in database')
                continue

            product_family = family_map[family_name]

            # Create new material option
            material_option = Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=config['choices'],
                adders=config['adders'],
            )

            db.add(material_option)
            db.flush()  # Get the ID

            # Create the association
            family_option = ProductFamilyOption(
                product_family_id=product_family.id,
                option_id=material_option.id,
                is_available=1,
            )

            db.add(family_option)
            created_count += 1
            print(f'  ✓ Created material option for {family_name}')

        db.commit()
        print(f'\n✓ Successfully created {created_count} material options')

        # Verify the results
        print('\n=== VERIFICATION ===')
        material_options = db.query(Option).filter(Option.name == 'Material').all()
        print(f'Found {len(material_options)} material options:')

        for option in material_options:
            families = [pf.name for pf in option.product_families]
            print(f'\n{families}:')
            print(f'  Choices: {option.choices}')
            print(f'  Adders: {option.adders}')

        print('\n✓ Material options reseed complete!')

    except Exception as e:
        print(f'Error: {e}')
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    reseed_material_options()
