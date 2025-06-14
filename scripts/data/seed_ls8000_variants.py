"""
Script to seed the database with all possible LS8000 product variants.
"""

import itertools
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

        materials = ["S", "H", "TS", "CPVC"]
        voltages = ["115VAC", "12VDC", "24VDC", "240VAC"]
        probe_types = ["Standard", '3/4" diameter']
        housings = ["Standard", "Stainless Steel (NEMA 4X)"]
        mountings = ["Standard", "Flanged", "Tri-Clamp"]

        # Base prices for S and H, TS, CPVC
        base_prices = {
            "S": 750.0,  # Base price for 316SS
            "H": 860.0,  # Base price for Halar
            "TS": 860.0,  # Same as Halar for Teflon Sleeve
            "CPVC": 770.0,  # Base price for CPVC
        }
        # Price adders
        probe_adder = {'3/4" diameter': 175.0, "Standard": 0.0}
        housing_adder = {"Stainless Steel (NEMA 4X)": 285.0, "Standard": 0.0}
        # Model number suffixes
        probe_suffix = {'3/4" diameter': '-3/4"', "Standard": ""}
        housing_suffix = {"Stainless Steel (NEMA 4X)": "-SS", "Standard": ""}

        variants = []
        for material, voltage, probe_type, housing, mounting in itertools.product(
            materials, voltages, probe_types, housings, mountings
        ):
            # Compose model number
            model_number = (
                f"LS8000-{voltage}-{material}-10"
                + probe_suffix[probe_type]
                + housing_suffix[housing]
            )
            description = f'LS 8000 level switch, {voltage}, 10" {material} probe, {probe_type}, {housing}, {mounting} mounting'
            base_price = (
                base_prices[material] + probe_adder[probe_type] + housing_adder[housing]
            )
            variant = ProductVariant(
                product_family_id=ls8000.id,
                model_number=model_number,
                description=description,
                base_price=base_price,
                base_length=10.0,
                voltage=voltage,
                material=material,
            )
            variants.append(variant)

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
