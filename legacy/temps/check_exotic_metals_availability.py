#!/usr/bin/env python3
"""
Check and update exotic metals availability across all product families.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.option import Option
from src.core.models.product_variant import ProductFamily


def check_current_availability():
    """Check current exotic metals availability across product families."""
    print("=== CHECKING EXOTIC METALS AVAILABILITY ===")

    db = SessionLocal()
    try:
        # Get all product families
        product_families = db.query(ProductFamily).all()
        print(f"Total product families: {len(product_families)}")

        # Get all material options
        material_options = db.query(Option).filter_by(category="Materials").all()

        exotic_codes = ["A", "HB", "HC", "TT"]

        print("\nCurrent exotic metals availability:")
        print(f"Exotic codes: {exotic_codes}")

        for family in product_families:
            # Find material option for this family
            material_option = None
            for option in material_options:
                if family.name in option.product_families:
                    material_option = option
                    break

            if material_option:
                choices = material_option.choices or []
                exotic_available = all(code in choices for code in exotic_codes)
                missing_exotic = [code for code in exotic_codes if code not in choices]

                print(f"  {family.name}: {'✅' if exotic_available else '❌'}")
                if missing_exotic:
                    print(f"    Missing: {missing_exotic}")
            else:
                print(f"  {family.name}: ❌ (No material option found)")

    finally:
        db.close()


def update_exotic_metals_availability():
    """Update exotic metals availability for all product families."""
    print("\n=== UPDATING EXOTIC METALS AVAILABILITY ===")

    db = SessionLocal()
    try:
        # Get all product families
        product_families = db.query(ProductFamily).all()

        # Get all material options
        material_options = db.query(Option).filter_by(category="Materials").all()

        exotic_codes = ["A", "HB", "HC", "TT"]
        exotic_adders = {
            "A": 250,  # Alloy 20
            "HB": 350,  # Hastelloy-B
            "HC": 350,  # Hastelloy-C-276
            "TT": 400,  # Titanium
        }

        print("Updating exotic metals availability for all families:")

        for family in product_families:
            # Find material option for this family
            material_option = None
            for option in material_options:
                if family.name in option.product_families:
                    material_option = option
                    break

            if material_option:
                current_choices = material_option.choices or []
                current_adders = material_option.adders or {}

                # Add exotic metals if not already present
                updated_choices = current_choices.copy()
                updated_adders = current_adders.copy()

                changes_made = False
                for code in exotic_codes:
                    if code not in updated_choices:
                        updated_choices.append(code)
                        updated_adders[code] = exotic_adders[code]
                        changes_made = True

                if changes_made:
                    material_option.choices = updated_choices
                    material_option.adders = updated_adders
                    print(
                        f"  ✅ Updated {family.name}: {len(current_choices)} → {len(updated_choices)} choices"
                    )
                else:
                    print(f"  ⚠️  {family.name}: Already has all exotic metals")
            else:
                print(f"  ❌ {family.name}: No material option found")

        db.commit()
        print("\n✅ Exotic metals availability updated successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error updating exotic metals availability: {e}")
        raise
    finally:
        db.close()


def verify_updated_availability():
    """Verify that exotic metals are now available for all families."""
    print("\n=== VERIFYING UPDATED AVAILABILITY ===")

    db = SessionLocal()
    try:
        # Get all product families
        product_families = db.query(ProductFamily).all()

        # Get all material options
        material_options = db.query(Option).filter_by(category="Materials").all()

        exotic_codes = ["A", "HB", "HC", "TT"]

        print("Verifying exotic metals availability:")

        all_families_have_exotic = True

        for family in product_families:
            # Find material option for this family
            material_option = None
            for option in material_options:
                if family.name in option.product_families:
                    material_option = option
                    break

            if material_option:
                choices = material_option.choices or []
                exotic_available = all(code in choices for code in exotic_codes)
                missing_exotic = [code for code in exotic_codes if code not in choices]

                if exotic_available:
                    print(f"  ✅ {family.name}: All exotic metals available")
                else:
                    print(f"  ❌ {family.name}: Missing {missing_exotic}")
                    all_families_have_exotic = False
            else:
                print(f"  ❌ {family.name}: No material option found")
                all_families_have_exotic = False

        print("\n" + "=" * 50)
        if all_families_have_exotic:
            print("✅ ALL PRODUCT FAMILIES HAVE EXOTIC METALS AVAILABLE")
        else:
            print("❌ SOME PRODUCT FAMILIES MISSING EXOTIC METALS")
        print("=" * 50)

    finally:
        db.close()


def main():
    """Run the complete exotic metals availability check and update."""
    print("EXOTIC METALS AVAILABILITY UPDATE")
    print("=" * 50)

    check_current_availability()

    # Confirm before proceeding
    response = (
        input("\nUpdate exotic metals availability for all families? (y/N): ")
        .strip()
        .lower()
    )
    if response != "y":
        print("Update cancelled.")
        return

    update_exotic_metals_availability()
    verify_updated_availability()

    print("\n" + "=" * 50)
    print("EXOTIC METALS AVAILABILITY UPDATE COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()
