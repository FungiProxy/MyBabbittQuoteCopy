"""
Script to seed the database with LS7000/2 product variants.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily, ProductVariant


def seed_ls7000_2_variants():
    """Seed the database with LS7000/2 product variants."""
    db = SessionLocal()
    try:
        # Get the LS7000/2 family
        ls7000_2 = db.query(ProductFamily).filter(ProductFamily.name == "LS7000/2").first()
        if not ls7000_2:
            print("LS7000/2 family not found in database")
            return

        # Define variants
        variants = [
            ProductVariant(
                product_family_id=ls7000_2.id,
                model_number='LS7000/2-115VAC-H-10"',
                description='LS7000/2 level switch with 115VAC power and 10" Halar coated probe',
                base_price=770.0,
                base_length=10.0,
                voltage="115VAC",
                material="H",
            ),
            ProductVariant(
                product_family_id=ls7000_2.id,
                model_number='LS7000/2-24VDC-H-10"',
                description='LS7000/2 level switch with 24VDC power and 10" Halar coated probe',
                base_price=770.0,
                base_length=10.0,
                voltage="24VDC",
                material="H",
            ),
            ProductVariant(
                product_family_id=ls7000_2.id,
                model_number='LS7000/2-12VDC-H-10"',
                description='LS7000/2 level switch with 12VDC power and 10" Halar coated probe',
                base_price=770.0,
                base_length=10.0,
                voltage="12VDC",
                material="H",
            ),
            ProductVariant(
                product_family_id=ls7000_2.id,
                model_number='LS7000/2-230VAC-H-10"',
                description='LS7000/2 level switch with 230VAC power and 10" Halar coated probe',
                base_price=770.0,
                base_length=10.0,
                voltage="230VAC",
                material="H",
            ),
            ProductVariant(
                product_family_id=ls7000_2.id,
                model_number='LS7000/2-115VAC-TS-10"',
                description='LS7000/2 level switch with 115VAC power and 10" Teflon Sleeve probe',
                base_price=770.0,
                base_length=10.0,
                voltage="115VAC",
                material="TS",
            ),
            ProductVariant(
                product_family_id=ls7000_2.id,
                model_number='LS7000/2-24VDC-TS-10"',
                description='LS 7000/2 level switch with 24VDC power and 10" Teflon Sleeve probe',
                base_price=770.0,
                base_length=10.0,
                voltage="24VDC",
                material="TS",
            ),
            ProductVariant(
                product_family_id=ls7000_2.id,
                model_number='LS7000/2-12VDC-TS-10"',
                description='LS7000/2 level switch with 12VDC power and 10" Teflon Sleeve probe',
                base_price=770.0,
                base_length=10.0,
                voltage="12VDC",
                material="TS",
            ),
            ProductVariant(
                product_family_id=ls7000_2.id,
                model_number='LS7000/2-230VAC-TS-10"',
                description='LS7000/2 level switch with 230VAC power and 10" Teflon Sleeve probe',
                base_price=770.0,
                base_length=10.0,
                voltage="230VAC",
                material="TS",
            ),
        ]

        # Add variants to database
        db.add_all(variants)
        db.commit()
        print(f"Added {len(variants)} LS7000/2 variants to database")
    except Exception as e:
        print(f"Error seeding LS7000/2 variants: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_ls7000_2_variants()
