"""
Script to seed the database with LS6000 connection options.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.connection_option import ConnectionOption
from src.core.models.product_variant import ProductFamily


def seed_ls6000_connections():
    """Seed the database with LS6000 connection options."""
    db = SessionLocal()
    try:
        # Get the LS6000 family
        ls6000 = db.query(ProductFamily).filter(ProductFamily.name == 'LS6000').first()
        if not ls6000:
            print('LS6000 family not found in database')
            return

        # Define NPT connection options
        npt_options = [
            ConnectionOption(
                type='NPT',
                rating=None,
                size='1/2"',
                price=0.0,
                product_family_id=ls6000.id,
            ),
            ConnectionOption(
                type='NPT',
                rating=None,
                size='3/4"',
                price=0.0,
                product_family_id=ls6000.id,
            ),
            ConnectionOption(
                type='NPT',
                rating=None,
                size='1"',
                price=0.0,
                product_family_id=ls6000.id,
            ),
            ConnectionOption(
                type='NPT',
                rating=None,
                size='1.5"',
                price=0.0,
                product_family_id=ls6000.id,
            ),
            ConnectionOption(
                type='NPT',
                rating=None,
                size='2"',
                price=0.0,
                product_family_id=ls6000.id,
            ),
        ]

        # Add NPT options to database
        db.add_all(npt_options)
        db.commit()
        print(f'Added {len(npt_options)} NPT connection options for LS6000')
    except Exception as e:
        print(f'Error seeding LS6000 connection options: {e}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    seed_ls6000_connections()
