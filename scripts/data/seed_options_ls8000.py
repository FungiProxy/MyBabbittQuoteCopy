"""
Script to seed the database with LS8000 options.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal, init_db
from src.core.models.option import Option

FAMILY_NAME = 'LS8000'

EXAMPLE_OPTIONS = [
    Option(
        name='Material',
        description='Probe material',
        product_families=FAMILY_NAME,
        price=0.0,
        price_type='fixed',
        category='Mechanical',
        choices=['S', 'H', 'TS', 'CPVC'],
        adders={'S': 0, 'H': 110, 'TS': 110, 'CPVC': 400},
        rules=None,
        excluded_products='',
    ),
    Option(
        name='Voltage',
        description='Supply voltage for the product',
        product_families=FAMILY_NAME,
        price=0.0,
        price_type='fixed',
        category='Electrical',
        choices=['115VAC', '12VDC', '24VDC', '240VAC'],
        adders={'115VAC': 0, '12VDC': 0, '24VDC': 0, '240VAC': 0},
        rules=None,
        excluded_products='',
    ),
    Option(
        name='Probe Length',
        description='Length of the probe in inches',
        product_families=FAMILY_NAME,
        price=0.0,
        price_type='per_inch',
        category='Mechanical',
        choices=['10', '20', '30', '40', '50', '60', '72'],
        adders={'10': 0, '20': 20, '30': 40, '40': 60, '50': 80, '60': 100, '72': 144},
        rules='Standard is 10". For S, add $45/foot over 10". For H or TS, add $110/foot over 10". For CPVC, add $50/inch over 4". $300 adder for non-standard lengths (except TS). Halar max 72". For longer, use TS.',
        excluded_products='',
    ),
    Option(
        name='Probe Type',
        description='Type of probe',
        product_families=FAMILY_NAME,
        price=0.0,
        price_type='fixed',
        category='Mechanical',
        choices=['Standard', '3/4" diameter'],
        adders={'Standard': 0, '3/4" diameter': 175},
        rules=None,
        excluded_products='',
    ),
    Option(
        name='Housing',
        description='Type of housing',
        product_families=FAMILY_NAME,
        price=0.0,
        price_type='fixed',
        category='Enclosure',
        choices=['Standard', 'Stainless Steel (NEMA 4X)'],
        adders={'Standard': 0, 'Stainless Steel (NEMA 4X)': 285},
        rules=None,
        excluded_products='',
    ),
    Option(
        name='Mounting',
        description='Type of mounting',
        product_families=FAMILY_NAME,
        price=0.0,
        price_type='fixed',
        category='Mechanical',
        choices=['Standard', 'Flanged', 'Tri-Clamp'],
        adders={'Standard': 0, 'Flanged': 0, 'Tri-Clamp': 0},
        rules=None,
        excluded_products='',
    ),
    Option(
        name='Bent Probe',
        description='Bent probe option',
        product_families=FAMILY_NAME,
        price=0.0,
        price_type='fixed',
        category='Mechanical',
        choices=['No', 'Yes'],
        adders={'No': 0, 'Yes': 50.00},
        rules=None,
        excluded_products='',
    ),
    Option(
        name='Stainless Steel Tag',
        description='Stainless steel tag option',
        product_families=FAMILY_NAME,
        price=0.0,
        price_type='fixed',
        category='Mechanical',
        choices=['No', 'Yes'],
        adders={'No': 0, 'Yes': 30.00},
        rules=None,
        excluded_products='',
    ),
]


def print_options(db):
    options = (
        db.query(Option).filter(Option.product_families.like(f'%{FAMILY_NAME}%')).all()
    )
    if not options:
        print(f'No options found for {FAMILY_NAME}.')
    else:
        print(f'Options for {FAMILY_NAME}:')
        for opt in options:
            print(f'- {opt.name}: {opt.choices} (Adders: {opt.adders})')


def seed_options(db):
    print(f'Seeding options for {FAMILY_NAME}...')
    for opt in EXAMPLE_OPTIONS:
        db.add(opt)
    db.commit()
    print('Seeding complete.')


def main():
    init_db()
    db = SessionLocal()
    try:
        print_options(db)
        options = (
            db.query(Option)
            .filter(Option.product_families.like(f'%{FAMILY_NAME}%'))
            .all()
        )
        if not options:
            seed_options(db)
            print_options(db)
    finally:
        db.close()


if __name__ == '__main__':
    main()
