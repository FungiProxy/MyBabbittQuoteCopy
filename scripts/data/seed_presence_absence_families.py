"""
Script to seed the database with presence/absence switch product families.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily


def seed_presence_absence_families():
    """Seed the database with presence/absence switch product families."""
    db = SessionLocal()
    try:
        # Create LS7500 family
        ls7500 = ProductFamily(
            name='LS7500',
            description='LS 7500 Presence/Absence Switch (replaces Princo L3515)',
            category='Presence/Absence Switches',
        )
        db.add(ls7500)

        # Create LS8500 family
        ls8500 = ProductFamily(
            name='LS8500',
            description='LS 8500 Presence/Absence Switch (replaces Princo L3545)',
            category='Presence/Absence Switches',
        )
        db.add(ls8500)

        db.commit()
        print('Added presence/absence switch product families to database')
    except Exception as e:
        print(f'Error seeding presence/absence switch families: {e}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    seed_presence_absence_families()
