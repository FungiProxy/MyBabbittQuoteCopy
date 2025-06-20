#!/usr/bin/env python3
"""
Master script to reseed all product variants.
This script clears the product_variants table and runs all individual seeding scripts
to ensure correct pricing and material availability.
"""

import importlib.util
import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductVariant


def clear_product_variants():
    """Clear all product variants from the database."""
    db = SessionLocal()
    try:
        print("🗑️  Clearing all product variants...")
        count = db.query(ProductVariant).count()
        db.query(ProductVariant).delete()
        db.commit()
        print(f"✅ Deleted {count} existing product variants")
    except Exception as e:
        print(f"❌ Error clearing product variants: {e}")
        db.rollback()
    finally:
        db.close()


def run_seeding_script(script_path, script_name):
    """Run a specific seeding script."""
    try:
        print(f"\n🌱 Running {script_name}...")

        # Import and run the seeding function
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the seeding function (assumes it's named seed_*_variants)
        seeding_function = None
        for attr_name in dir(module):
            if attr_name.startswith("seed_") and attr_name.endswith("_variants"):
                seeding_function = getattr(module, attr_name)
                break

        if seeding_function:
            seeding_function()
            print(f"✅ {script_name} completed successfully")
        else:
            print(f"❌ Could not find seeding function in {script_name}")

    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")


def reseed_all_variants():
    """Reseed all product variants using the individual seeding scripts."""

    # Define all seeding scripts in order
    seeding_scripts = [
        ("scripts/data/seeds/product_variants/seed_ls2000_variants.py", "LS2000"),
        ("scripts/data/seeds/product_variants/seed_ls2100_variants.py", "LS2100"),
        ("scripts/data/seeds/product_variants/seed_ls6000_variants.py", "LS6000"),
        ("scripts/data/seeds/product_variants/seed_ls7000_variants.py", "LS7000"),
        ("scripts/data/seeds/product_variants/seed_ls7000_2_variants.py", "LS7000/2"),
        ("scripts/data/seeds/product_variants/seed_ls7500_variants.py", "LS7500"),
        ("scripts/data/seeds/product_variants/seed_ls8000_variants.py", "LS8000"),
        ("scripts/data/seeds/product_variants/seed_ls8000_2_variants.py", "LS8000/2"),
        ("scripts/data/seeds/product_variants/seed_ls8500_variants.py", "LS8500"),
        ("scripts/data/seeds/product_variants/seed_lt9000_variants.py", "LT9000"),
        ("scripts/data/seeds/product_variants/seed_fs10000_variants.py", "FS10000"),
    ]

    print("🚀 Starting complete product variant reseeding process...")
    print("=" * 60)

    # Step 1: Clear existing variants
    clear_product_variants()

    # Step 2: Run all seeding scripts
    for script_path, family_name in seeding_scripts:
        if os.path.exists(script_path):
            run_seeding_script(script_path, family_name)
        else:
            print(f"❌ Script not found: {script_path}")

    # Step 3: Verify results
    verify_results()

    print("\n" + "=" * 60)
    print("🎉 Product variant reseeding completed!")


def verify_results():
    """Verify the reseeding results."""
    db = SessionLocal()
    try:
        print("\n🔍 Verifying reseeding results...")

        # Count total variants
        total_variants = db.query(ProductVariant).count()
        print(f"📊 Total product variants: {total_variants}")

        # Check each family
        families = [
            "LS2000",
            "LS2100",
            "LS6000",
            "LS7000",
            "LS7000/2",
            "LS7500",
            "LS8000",
            "LS8000/2",
            "LS8500",
            "LT9000",
            "FS10000",
        ]

        for family_name in families:
            from src.core.models.product_variant import ProductFamily

            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if family:
                family_variants = (
                    db.query(ProductVariant)
                    .filter(ProductVariant.product_family_id == family.id)
                    .count()
                )
                print(f"  {family_name}: {family_variants} variants")
            else:
                print(f"  {family_name}: Family not found")

        # Check LT9000 pricing specifically
        print("\n💰 LT9000 Pricing Check:")
        lt9000 = db.query(ProductFamily).filter(ProductFamily.name == "LT9000").first()
        if lt9000:
            lt9000_variants = (
                db.query(ProductVariant)
                .filter(ProductVariant.product_family_id == lt9000.id)
                .all()
            )

            for variant in lt9000_variants:
                print(f"  {variant.model_number}: ${variant.base_price}")
        else:
            print("  LT9000 family not found")

        print("\n✅ Verification completed!")

    except Exception as e:
        print(f"❌ Error during verification: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    reseed_all_variants()
