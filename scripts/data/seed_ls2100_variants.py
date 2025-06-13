"""
Script to seed the database with LS2100 product variants.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily, ProductVariant


def seed_ls2100_variants():
    """Seed the database with LS2100 product variants."""
    db = SessionLocal()
    try:
        # Get the LS2100 family
        ls2100 = db.query(ProductFamily).filter(ProductFamily.name == 'LS2100').first()
        if not ls2100:
            print('LS2100 family not found in database')
            return

        # Define variants
        variants = [
            ProductVariant(
                product_family_id=ls2100.id,
                model_number='LS2100-115VAC-S-10"',
                description='LS 2100 level switch with 115VAC power and 10" 316SS probe',
                base_price=475.0,
                base_length=10.0,
                voltage='115VAC',
                material='S',
            ),
            ProductVariant(
                product_family_id=ls2100.id,
                model_number='LS2100-115VAC-H-10"',
                description='LS 2100 level switch with 115VAC power and 10" Halar coated probe',
                base_price=585.0,
                base_length=10.0,
                voltage='115VAC',
                material='H',
            ),
            ProductVariant(
                product_family_id=ls2100.id,
                model_number='LS2100-24VDC-S-10"',
                description='LS 2100 level switch with 24VDC power and 10" 316SS probe',
                base_price=475.0,
                base_length=10.0,
                voltage='24VDC',
                material='S',
            ),
            ProductVariant(
                product_family_id=ls2100.id,
                model_number='LS2100-24VDC-H-10"',
                description='LS 2100 level switch with 24VDC power and 10" Halar coated probe',
                base_price=585.0,
                base_length=10.0,
                voltage='24VDC',
                material='H',
            ),
            ProductVariant(
                product_family_id=ls2100.id,
                model_number='LS2100-115VAC-U-4"',
                description='LS 2100 level switch with 115VAC power and 4" UHMWPE blind end probe',
                base_price=495.0,
                base_length=4.0,
                voltage='115VAC',
                material='U',
            ),
            ProductVariant(
                product_family_id=ls2100.id,
                model_number='LS2100-115VAC-T-4"',
                description='LS 2100 level switch with 115VAC power and 4" Teflon blind end probe',
                base_price=535.0,
                base_length=4.0,
                voltage='115VAC',
                material='T',
            ),
        ]

        # Add variants to database
        db.add_all(variants)
        db.commit()
        print(f'Added {len(variants)} LS2100 variants to database')
    except Exception as e:
        print(f'Error seeding LS2100 variants: {e}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    seed_ls2100_variants()
