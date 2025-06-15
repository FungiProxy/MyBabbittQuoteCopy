"""
Script to seed the database with all possible LS7500 product variants (Presence/Absence Switches).
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily, ProductVariant


def seed_ls7500_variants():
    """Seed the database with all possible LS7500 product variants."""
    db = SessionLocal()
    try:
        # Get the LS7500 family
        ls7500 = db.query(ProductFamily).filter(ProductFamily.name == "LS7500").first()
        if not ls7500:
            print("LS7500 family not found in database")
            return

        # Define variants
        variants = [
            ProductVariant(
                product_family_id=ls7500.id,
                model_number='LS7500-115VAC-PR-2"',
                description='LS7500 presence/absence switch with 115VAC power and 2" 316SS probe',
                base_price=0.0,
                base_length=2.0,
                voltage="115VAC",
                material="S",
            ),
            ProductVariant(
                product_family_id=ls7500.id,
                model_number='LS7500-115VAC-PR-2-1/2"',
                description='LS7500 presence/absence switch with 115VAC power and 2-1/2" 316SS probe',
                base_price=0.0,
                base_length=2.5,
                voltage="115VAC",
                material="S",
            ),
            ProductVariant(
                product_family_id=ls7500.id,
                model_number='LS7500-115VAC-PR-3"',
                description='LS7500 presence/absence switch with 115VAC power and 3" 316SS probe',
                base_price=0.0,
                base_length=3.0,
                voltage="115VAC",
                material="S",
            ),
            ProductVariant(
                product_family_id=ls7500.id,
                model_number='LS7500-115VAC-PR-4"',
                description='LS7500 presence/absence switch with 115VAC power and 4" 316SS probe',
                base_price=0.0,
                base_length=4.0,
                voltage="115VAC",
                material="S",
            ),
            ProductVariant(
                product_family_id=ls7500.id,
                model_number='LS7500-115VAC-PR-6"',
                description='LS7500 presence/absence switch with 115VAC power and 6" 316SS probe',
                base_price=0.0,
                base_length=6.0,
                voltage="115VAC",
                material="S",
            ),
            ProductVariant(
                product_family_id=ls7500.id,
                model_number='LS7500-115VAC-PR-8"',
                description='LS7500 presence/absence switch with 115VAC power and 8" 316SS probe',
                base_price=0.0,
                base_length=8.0,
                voltage="115VAC",
                material="S",
            ),
            ProductVariant(
                product_family_id=ls7500.id,
                model_number='LS7500-115VAC-PR-10"',
                description='LS7500 presence/absence switch with 115VAC power and 10" 316SS probe',
                base_price=0.0,
                base_length=10.0,
                voltage="115VAC",
                material="S",
            ),
        ]
        
        # Add variants to database
        db.add_all(variants)
        db.commit()
        print(f"Added {len(variants)} LS7500 variants to database")
    except Exception as e:
        print(f"Error seeding LS7500 variants: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_ls7500_variants()
