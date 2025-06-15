"""
Script to seed the database with all possible LS8000 product variants.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily, ProductVariant


def seed_ls8000_variants():
    """Seed the database with all possible LS8000 product variants."""
    db = SessionLocal()
    try:
        # Get the LS8000 family
        ls8000 = db.query(ProductFamily).filter(ProductFamily.name == "LS8000").first()
        if not ls8000:
            print("LS8000 family not found in database")
            return

        # Define variants
        variants = [
            ProductVariant(
                product_family_id=ls8000.id,
                model_number='LS8000-115VAC-S-10"',
                description='LS8000 level switch with 115VAC power and 10" 316SS probe',
                base_price=715.0,
                base_length=10.0,
                voltage="115VAC",
                material="S",
            ),
            ProductVariant(
                product_family_id=ls8000.id,
                model_number='LS8000-115VAC-H-10"',
                description='LS8000 level switch with 115VAC power and 10" Halar coated probe',
                base_price=825.0,
                base_length=10.0,
                voltage="115VAC",
                material="H",
            ),
            ProductVariant(
                product_family_id=ls8000.id,
                model_number='LS8000-115VAC-U-4"',
                description='LS8000 level switch with 115VAC power and 4" UHMWPE blind end probe',
                base_price=735.0,
                base_length=4.0,
                voltage="115VAC",
                material="U",
            ),
            ProductVariant(
                product_family_id=ls8000.id,
                model_number='LS8000-115VAC-T-4"',
                description='LS8000 level switch with 115VAC power and 4" Teflon blind end probe',
                base_price=775.0,
                base_length=4.0,
                voltage="115VAC",
                material="T",
            ),
            ProductVariant(
                product_family_id=ls8000.id,
                model_number='LS8000-115VAC-TS-10"',
                description='LS8000 level switch with 115VAC power and 10" Teflon sleeve probe',
                base_price=825.0,
                base_length=10.0,
                voltage="115VAC",
                material="TS",
            ),
            ProductVariant(
                product_family_id=ls8000.id,
                model_number='LS8000-115VAC-C-12"',
                description='LS8000 level switch with 115VAC power and 12" Cable probe',
                base_price=795.0,
                base_length=12.0,
                voltage="115VAC",
                material="C",
            ),
        ]

        # Add variants to database
        db.add_all(variants)
        db.commit()
        print(f"Added {len(variants)} LS8000 variants to database")
    except Exception as e:
        print(f"Error seeding LS8000 variants: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_ls8000_variants()
