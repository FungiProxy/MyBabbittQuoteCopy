import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.core.models.option import Option


def fix_cpvc_options():
    """Fix CPVC options to ensure it's only in Material dropdown for LS6000 and LS7000."""
    db = SessionLocal()
    try:
        # First, remove any standalone CPVC options
        standalone_cpvc = db.query(Option).filter(Option.name == 'CPVC').all()
        for option in standalone_cpvc:
            print(f'Removing standalone CPVC option for {option.product_families}')
            db.delete(option)

        # Remove CPVC from any other models' Material options
        other_models_material = (
            db.query(Option)
            .filter(
                Option.name == 'Material',
                ~Option.product_families.like('%LS6000%'),
                ~Option.product_families.like('%LS7000%'),
            )
            .all()
        )
        for option in other_models_material:
            if 'CPVC' in option.choices:
                print(
                    f'Removing CPVC from Material choices for {option.product_families}'
                )
                option.choices.remove('CPVC')
                if 'CPVC' in option.adders:
                    del option.adders['CPVC']

        # Ensure CPVC is in Material dropdown for LS6000
        ls6000_material = (
            db.query(Option)
            .filter(Option.name == 'Material', Option.product_families.like('%LS6000%'))
            .first()
        )
        if ls6000_material:
            if 'CPVC' not in ls6000_material.choices:
                print('Adding CPVC to LS6000 Material choices')
                ls6000_material.choices.append('CPVC')
            if ls6000_material.adders.get('CPVC') != 400:
                print('Setting CPVC adder to 400 for LS6000')
                ls6000_material.adders['CPVC'] = 400
        else:
            print('Creating Material option for LS6000 with CPVC')
            ls6000_material = Option(
                name='Material',
                description='Probe material',
                product_families='LS6000',
                price=0.0,
                price_type='fixed',
                category='Mechanical',
                choices=['S', 'H', 'TS', 'CPVC'],
                adders={'S': 0, 'H': 110, 'TS': 110, 'CPVC': 400},
                rules=None,
                excluded_products='',
            )
            db.add(ls6000_material)

        # Ensure CPVC is in Material dropdown for LS7000
        ls7000_material = (
            db.query(Option)
            .filter(Option.name == 'Material', Option.product_families.like('%LS7000%'))
            .first()
        )
        if ls7000_material:
            if 'CPVC' not in ls7000_material.choices:
                print('Adding CPVC to LS7000 Material choices')
                ls7000_material.choices.append('CPVC')
            if ls7000_material.adders.get('CPVC') != 400:
                print('Setting CPVC adder to 400 for LS7000')
                ls7000_material.adders['CPVC'] = 400
        else:
            print('Creating Material option for LS7000 with CPVC')
            ls7000_material = Option(
                name='Material',
                description='Probe material',
                product_families='LS7000',
                price=0.0,
                price_type='fixed',
                category='Mechanical',
                choices=['S', 'H', 'TS', 'CPVC'],
                adders={'S': 0, 'H': 110, 'TS': 110, 'CPVC': 400},
                rules=None,
                excluded_products='',
            )
            db.add(ls7000_material)

        # Remove the standalone CPVC Probe option from LS6000
        cpvc_probe = (
            db.query(Option)
            .filter(
                Option.name == 'CPVC Probe', Option.product_families.like('%LS6000%')
            )
            .first()
        )
        if cpvc_probe:
            print('Removing standalone CPVC Probe option from LS6000')
            db.delete(cpvc_probe)

        db.commit()
        print('\nVerification of changes:')
        for model in ['LS6000', 'LS7000']:
            material_option = (
                db.query(Option)
                .filter(
                    Option.name == 'Material',
                    Option.product_families.like(f'%{model}%'),
                )
                .first()
            )
            if material_option:
                print(f'\n{model} Material options:')
                print(f'Choices: {material_option.choices}')
                print(f'Adders: {material_option.adders}')

    finally:
        db.close()


if __name__ == '__main__':
    fix_cpvc_options()
