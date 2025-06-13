"""
Script to seed the database with all possible LS7500 product variants (Presence/Absence Switches).
"""

import os
import sys
import itertools

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

        flange_sizes = ['2"', '2.5"', '3"', '4"', '6"', '8"', '10"']
        flange_types = ["PR", "FR"]
        voltages = ["115VAC", "24VDC", "220VAC", "12VDC"]
        teflon_options = ["No", "Yes"]
        tag_options = ["No", "Yes"]

        variants = []
        for size, ftype, voltage, teflon, tag in itertools.product(
            flange_sizes, flange_types, voltages, teflon_options, tag_options
        ):
            # Only allow Teflon Insulator for 6, 8, 10 inch flanges
            if teflon == "Yes" and size not in ['6"', '8"', '10"']:
                continue

            # Compose model number
            model_number = f"LS7500-{voltage}-FP-{size}-150-{ftype}"
            if teflon == "Yes":
                model_number += "-T"
            if tag == "Yes":
                model_number += "-ST"

            # Description
            description = (
                f"LS7500 presence/absence switch, {voltage}, {size} 150# {ftype} flange"
            )
            if teflon == "Yes":
                description += ", with Teflon insulator"
            if tag == "Yes":
                description += ", with stainless steel tag"

            variant = ProductVariant(
                product_family_id=ls7500.id,
                model_number=model_number,
                description=description,
                base_price=None,  # Consult Factory
                base_length=None,
                voltage=voltage,
                material="316SS",
            )
            variants.append(variant)

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
