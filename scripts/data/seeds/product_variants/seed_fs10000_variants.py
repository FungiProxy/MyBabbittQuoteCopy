"""
Script to seed the database with LS2000 product variants.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily, ProductVariant


def seed_fs10000_variants():
    """Seed the database with FS10000 product variants."""
    db = SessionLocal()
    try:
        # Get the FS10000 family
        fs10000 = (
            db.query(ProductFamily).filter(ProductFamily.name == "FS10000").first()
        )
        if not fs10000:
            print("FS10000 family not found in database")
            return

        # Define variants
        variants = [
            ProductVariant(
                product_family_id=fs10000.id,
                model_number='FS10000-115VAC-S-6"',
                description='FS10000 flow switch with 115VAC power and 6" 316SS probe',
                base_price=1885.0,
                base_length=6.0,
                voltage="115VAC",
                material="S",
            ),
            ProductVariant(
                product_family_id=fs10000.id,
                model_number='FS10000-115VAC-S-3"',
                description='FS10000 flow switch with 115VAC power and 3" 316SS probe',
                base_price=1885.0,
                base_length=3.0,
                voltage="115VAC",
                material="S",
            ),
            ProductVariant(
                product_family_id=fs10000.id,
                model_number='FS10000-115VAC-S-1.5"',
                description='FS10000 flow switch with 115VAC power and 1.5" 316SS probe',
                base_price=1885.0,
                base_length=1.5,
                voltage="115VAC",
                material="S",
            ),
        ]

        # Add variants to database
        db.add_all(variants)
        db.commit()
        print(f"Added {len(variants)} FS10000 variants to database")
    except Exception as e:
        print(f"Error seeding FS10000 variants: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_fs10000_variants()
