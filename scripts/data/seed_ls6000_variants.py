"""
Script to seed the database with LS6000 product variants.
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily, ProductVariant

def seed_ls6000_variants():
    """Seed the database with LS6000 product variants."""
    db = SessionLocal()
    try:
        # Get the LS6000 family
        ls6000 = db.query(ProductFamily).filter(ProductFamily.name == "LS6000").first()
        if not ls6000:
            print("LS6000 family not found in database")
            return

        # Define variants
        variants = [
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-115VAC-S-10\"",
                description="LS 6000 level switch with 115VAC power and 10\" 316SS probe",
                base_price=550.0,
                base_length=10.0,
                voltage="115VAC",
                material="S"
            ),
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-115VAC-H-10\"",
                description="LS 6000 level switch with 115VAC power and 10\" Halar coated probe",
                base_price=660.0,
                base_length=10.0,
                voltage="115VAC",
                material="H"
            ),
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-24VDC-S-10\"",
                description="LS 6000 level switch with 24VDC power and 10\" 316SS probe",
                base_price=550.0,
                base_length=10.0,
                voltage="24VDC",
                material="S"
            ),
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-24VDC-H-10\"",
                description="LS 6000 level switch with 24VDC power and 10\" Halar coated probe",
                base_price=660.0,
                base_length=10.0,
                voltage="24VDC",
                material="H"
            ),
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-12VDC-S-10\"",
                description="LS 6000 level switch with 12VDC power and 10\" 316SS probe",
                base_price=550.0,
                base_length=10.0,
                voltage="12VDC",
                material="S"
            ),
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-12VDC-H-10\"",
                description="LS 6000 level switch with 12VDC power and 10\" Halar coated probe",
                base_price=660.0,
                base_length=10.0,
                voltage="12VDC",
                material="H"
            ),
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-240VAC-S-10\"",
                description="LS 6000 level switch with 240VAC power and 10\" 316SS probe",
                base_price=550.0,
                base_length=10.0,
                voltage="240VAC",
                material="S"
            ),
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-240VAC-H-10\"",
                description="LS 6000 level switch with 240VAC power and 10\" Halar coated probe",
                base_price=660.0,
                base_length=10.0,
                voltage="240VAC",
                material="H"
            ),
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-115VAC-S-10\"-3/4\"",
                description="LS 6000 level switch with 115VAC power and 10\" 316SS probe (3/4\" diameter)",
                base_price=725.0,
                base_length=10.0,
                voltage="115VAC",
                material="S"
            ),
            ProductVariant(
                product_family_id=ls6000.id,
                model_number="LS6000-115VAC-H-10\"-3/4\"",
                description="LS 6000 level switch with 115VAC power and 10\" Halar coated probe (3/4\" diameter)",
                base_price=835.0,
                base_length=10.0,
                voltage="115VAC",
                material="H"
            )
        ]

        # Add variants to database
        db.add_all(variants)
        db.commit()
        print(f"Added {len(variants)} LS6000 variants to database")
    except Exception as e:
        print(f"Error seeding LS6000 variants: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_ls6000_variants() 