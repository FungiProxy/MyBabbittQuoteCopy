"""
Script to seed the database with LS7000/2 connection options.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.connection_option import ConnectionOption
from src.core.models.product_variant import ProductFamily


def seed_ls7000_2_connections():
    """Seed the database with LS7000/2 connection options."""
    db = SessionLocal()
    try:
        # Get the LS7000/2 family
        ls7000_2 = (
            db.query(ProductFamily).filter(ProductFamily.name == 'LS7000/2').first()
        )
        if not ls7000_2:
            print('LS7000/2 family not found in database')
            return

        # Define NPT connection options
        npt_options = [
            ConnectionOption(
                type='NPT',
                rating=None,
                size='3/4"',
                price=0.0,
                product_family_id=ls7000_2.id,
            ),
            ConnectionOption(
                type='NPT',
                rating=None,
                size='1"',
                price=0.0,
                product_family_id=ls7000_2.id,
            ),
        ]

        # Define Flange connection options
        flange_options = [
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='1"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='1.5"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='2"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='3"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
            ConnectionOption(
                type='Flange',
                rating='150#',
                size='4"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
        ]

        # Define Tri-Clamp connection options
        tri_clamp_options = [
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='1"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='1.5"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='2"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='3"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
            ConnectionOption(
                type='Tri-Clamp',
                rating=None,
                size='4"',
                price=None,
                product_family_id=ls7000_2.id,
            ),
        ]

        all_options = npt_options + flange_options + tri_clamp_options
        db.add_all(all_options)
        db.commit()
        print(f'Added {len(all_options)} connection options for LS7000/2')
    except Exception as e:
        print(f'Error seeding LS7000/2 connection options: {e}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    seed_ls7000_2_connections()
