#!/usr/bin/env python3
"""
Clear product_variants table to enable dynamic configuration.
This script removes the static variants and keeps only the essential
base information needed for the dynamic configuration system.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductVariant, ProductFamily


def clear_variants_for_dynamic_config():
    """Clear product_variants and keep only essential base information."""
    db = SessionLocal()
    try:
        print("🔄 Clearing product_variants for dynamic configuration...")

        # Count existing variants
        existing_count = db.query(ProductVariant).count()
        print(f"📊 Found {existing_count} existing product variants")

        # Clear all variants
        db.query(ProductVariant).delete()
        db.commit()
        print(f"✅ Cleared all {existing_count} product variants")

        # Verify product families are still intact
        families = db.query(ProductFamily).all()
        print(f"📋 Product families remain intact: {len(families)} families")
        for family in families:
            print(f"  - {family.name}: {family.description}")

        # Verify options are still intact
        from src.core.models.option import Option

        options_count = db.query(Option).count()
        print(f"🔧 Unified options remain intact: {options_count} options")

        print("\n🎯 Ready for dynamic configuration!")
        print("   - Product families: ✅")
        print("   - Unified options: ✅")
        print("   - Static variants: ❌ (cleared for dynamic approach)")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    clear_variants_for_dynamic_config()
