"""
Script to seed the database with all possible LT9000 product variants.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily, ProductVariant


def seed_lt9000_variants():
    """Seed the database with all possible LT9000 product variants."""
    db = SessionLocal()
    try:
        # Get the LT9000 family
        lt9000 = db.query(ProductFamily).filter(ProductFamily.name == "LT9000").first()
        if not lt9000:
            print("LT9000 family not found in database")
            return

        # Define variants
        variants = [
            # 115VAC variants
            ProductVariant(
                product_family_id=lt9000.id,
                model_number='LT9000-115VAC-H-10"',
                description='LT9000 level transmitter with 115VAC power and 10" Halar coated probe',
                base_price=855.0,
                base_length=10.0,
                voltage="115VAC",
                material="H",
            ),
            ProductVariant(
                product_family_id=lt9000.id,
                model_number='LT9000-115VAC-TS-10"',
                description='LT9000 level transmitter with 115VAC power and 10" Teflon sleeve probe',
                base_price=855.0,
                base_length=10.0,
                voltage="115VAC",
                material="TS",
            ),
            # 24VDC variants
            ProductVariant(
                product_family_id=lt9000.id,
                model_number='LT9000-24VDC-H-10"',
                description='LT9000 level transmitter with 24VDC power and 10" Halar coated probe',
                base_price=855.0,
                base_length=10.0,
                voltage="24VDC",
                material="H",
            ),
            ProductVariant(
                product_family_id=lt9000.id,
                model_number='LT9000-24VDC-TS-10"',
                description='LT9000 level transmitter with 24VDC power and 10" Teflon sleeve probe',
                base_price=855.0,
                base_length=10.0,
                voltage="24VDC",
                material="TS",
            ),
            # 230VAC variants
            ProductVariant(
                product_family_id=lt9000.id,
                model_number='LT9000-230VAC-H-10"',
                description='LT9000 level transmitter with 230VAC power and 10" Halar coated probe',
                base_price=855.0,
                base_length=10.0,
                voltage="230VAC",
                material="H",
            ),
            ProductVariant(
                product_family_id=lt9000.id,
                model_number='LT9000-230VAC-TS-10"',
                description='LT9000 level transmitter with 230VAC power and 10" Teflon sleeve probe',
                base_price=855.0,
                base_length=10.0,
                voltage="230VAC",
                material="TS",
            ),
        ]

        # Add variants to database
        db.add_all(variants)
        db.commit()
        print(f"Added {len(variants)} LT9000 variants to database")
    except Exception as e:
        print(f"Error seeding LT9000 variants: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_lt9000_variants()
