"""
Script to seed the database with LS8000 connection options.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.connection_option import ConnectionOption
from src.core.models.product_variant import ProductFamily


def seed_ls8000_connections():
    """Seed the database with LS8000 connection options."""
    db = SessionLocal()
    try:
        # Get the LS8000 family
        ls8000 = db.query(ProductFamily).filter(ProductFamily.name == 'LS8000').first()
        if not ls8000:
            print('LS8000 family not found in database')
            return

        # Define NPT connection options
        npt_options = [
            ConnectionOption(
                type='NPT',
                rating=None,
                size='1/2"',
                price=0.0,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='NPT',
                rating=None,
                size='3/4"',
                price=0.0,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='NPT',
                rating=None,
                size='1"',
                price=0.0,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='NPT',
                rating=None,
                size='1.5"',
                price=0.0,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='NPT',
                rating=None,
                size='2"',
                price=0.0,
                product_family_id=ls8000.id,
            ),
        ]

        # Define Flange connection options
        flange_options = [
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='1"',
                price=None,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='1.5"',
                price=None,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='2"',
                price=None,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='3"',
                price=None,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='4"',
                price=None,
                product_family_id=ls8000.id,
            ),
        ]

        # Define Tri-Clamp connection options
        tri_clamp_options = [
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='1"',
                price=None,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='1.5"',
                price=None,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='2"',
                price=None,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='3"',
                price=None,
                product_family_id=ls8000.id,
            ),
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='4"',
                price=None,
                product_family_id=ls8000.id,
            ),
        ]

        all_options = npt_options + flange_options + tri_clamp_options
        db.add_all(all_options)
        db.commit()
        print(f'Added {len(all_options)} connection options for LS8000')
    except Exception as e:
        print(f'Error seeding LS8000 connection options: {e}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    seed_ls8000_connections()
