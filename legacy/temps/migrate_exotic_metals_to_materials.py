#!/usr/bin/env python3
"""
Migrate exotic metals from options to materials system.
This will:
1. Add exotic metal materials to the materials table
2. Update material options to include exotic metals
3. Remove exotic metals from the options table
4. Update any related code references
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.material import Material, StandardLength
from src.core.models.option import Option


def analyze_current_exotic_metals():
    """Analyze the current exotic metals setup."""
    print("=== ANALYZING CURRENT EXOTIC METALS ===")

    db = SessionLocal()
    try:
        # Check exotic metals in options
        exotic_options = db.query(Option).filter_by(category="Exotic Metals").all()
        print(f"Found {len(exotic_options)} exotic metal options:")

        for option in exotic_options:
            print(f"  ID: {option.id}")
            print(f"  Name: {option.name}")
            print(f"  Product Families: {option.product_families}")
            print(f"  Choices: {option.choices}")
            print(f"  Adders: {option.adders}")
            print("  ---")

        # Check current materials
        materials = db.query(Material).all()
        print(f"\nCurrent materials ({len(materials)}):")
        for material in materials:
            print(f"  {material.code} - {material.name}")

    finally:
        db.close()


def add_exotic_metal_materials():
    """Add exotic metals to the materials table."""
    print("\n=== ADDING EXOTIC METAL MATERIALS ===")

    # Define exotic metal materials
    exotic_materials = [
        {
            "code": "A",
            "name": "Alloy 20",
            "description": "Alloy 20 probe material",
            "base_length": 12.0,
            "length_adder_per_inch": 15.0,  # Higher cost than standard
            "length_adder_per_foot": 180.0,
            "has_nonstandard_length_surcharge": True,
            "nonstandard_length_surcharge": 300.0,
            "base_price_adder": 250.0,  # Base cost for exotic metal
        },
        {
            "code": "HB",
            "name": "Hastelloy-B",
            "description": "Hastelloy-B probe material",
            "base_length": 12.0,
            "length_adder_per_inch": 20.0,  # Higher cost than Alloy 20
            "length_adder_per_foot": 240.0,
            "has_nonstandard_length_surcharge": True,
            "nonstandard_length_surcharge": 300.0,
            "base_price_adder": 350.0,
        },
        {
            "code": "HC",
            "name": "Hastelloy-C-276",
            "description": "Hastelloy-C-276 probe material",
            "base_length": 12.0,
            "length_adder_per_inch": 20.0,  # Same as Hastelloy-B
            "length_adder_per_foot": 240.0,
            "has_nonstandard_length_surcharge": True,
            "nonstandard_length_surcharge": 300.0,
            "base_price_adder": 350.0,
        },
        {
            "code": "TT",
            "name": "Titanium",
            "description": "Titanium probe material",
            "base_length": 12.0,
            "length_adder_per_inch": 25.0,  # Highest cost
            "length_adder_per_foot": 300.0,
            "has_nonstandard_length_surcharge": True,
            "nonstandard_length_surcharge": 300.0,
            "base_price_adder": 400.0,
        },
    ]

    db = SessionLocal()
    try:
        # Check if exotic materials already exist
        existing_codes = [m.code for m in db.query(Material).all()]

        print("Adding exotic metal materials:")
        for material_data in exotic_materials:
            if material_data["code"] in existing_codes:
                print(
                    f"  ⚠️  {material_data['code']} - {material_data['name']} (already exists)"
                )
            else:
                material = Material(**material_data)
                db.add(material)
                print(f"  ✅ {material_data['code']} - {material_data['name']}")

        # Add standard lengths for exotic materials
        print("\nAdding standard lengths for exotic materials:")
        exotic_codes = ["A", "HB", "HC", "TT"]
        standard_lengths = [6.0, 12.0, 18.0, 24.0, 36.0, 48.0, 60.0, 72.0, 84.0]

        for code in exotic_codes:
            for length in standard_lengths:
                # Check if this standard length already exists
                existing = (
                    db.query(StandardLength)
                    .filter_by(material_code=code, length=length)
                    .first()
                )

                if not existing:
                    std_length = StandardLength(material_code=code, length=length)
                    db.add(std_length)
                    print(f'  ✅ {code} - {length}"')
                else:
                    print(f'  ⚠️  {code} - {length}" (already exists)')

        db.commit()
        print("\n✅ Exotic metal materials added successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error adding exotic materials: {e}")
        raise
    finally:
        db.close()


def update_material_options():
    """Update material options to include exotic metals."""
    print("\n=== UPDATING MATERIAL OPTIONS ===")

    db = SessionLocal()
    try:
        # Get all material options
        material_options = db.query(Option).filter_by(category="Materials").all()

        print("Updating material options to include exotic metals:")

        for option in material_options:
            current_choices = option.choices or []
            current_adders = option.adders or {}

            # Add exotic metal choices and adders
            new_choices = [*current_choices, "A", "HB", "HC", "TT"]
            new_adders = current_adders.copy()
            new_adders.update(
                {
                    "A": 250,  # Alloy 20
                    "HB": 350,  # Hastelloy-B
                    "HC": 350,  # Hastelloy-C-276
                    "TT": 400,  # Titanium
                }
            )

            option.choices = new_choices
            option.adders = new_adders

            print(
                f"  ✅ Updated {option.product_families}: {len(current_choices)} → {len(new_choices)} choices"
            )

        db.commit()
        print("\n✅ Material options updated successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error updating material options: {e}")
        raise
    finally:
        db.close()


def remove_exotic_metals_options():
    """Remove exotic metals from the options table."""
    print("\n=== REMOVING EXOTIC METALS FROM OPTIONS ===")

    db = SessionLocal()
    try:
        # Find and remove exotic metal options
        exotic_options = db.query(Option).filter_by(category="Exotic Metals").all()

        print(f"Removing {len(exotic_options)} exotic metal options:")
        for option in exotic_options:
            print(f"  🗑️  Removing: {option.name} (ID: {option.id})")
            db.delete(option)

        db.commit()
        print("✅ Exotic metal options removed successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error removing exotic metal options: {e}")
        raise
    finally:
        db.close()


def verify_migration():
    """Verify that the migration was successful."""
    print("\n=== VERIFICATION ===")

    db = SessionLocal()
    try:
        # Check materials
        materials = db.query(Material).all()
        print(f"Total materials: {len(materials)}")

        exotic_codes = ["A", "HB", "HC", "TT"]
        print("\nExotic metal materials:")
        for code in exotic_codes:
            material = db.query(Material).filter_by(code=code).first()
            if material:
                print(f"  ✅ {code} - {material.name} (${material.base_price_adder})")
            else:
                print(f"  ❌ {code} - NOT FOUND")

        # Check material options
        material_options = db.query(Option).filter_by(category="Materials").all()
        print(f"\nMaterial options: {len(material_options)}")

        if material_options:
            sample_option = material_options[0]
            print(f"Sample material option choices: {sample_option.choices}")
            print(f"Sample material option adders: {sample_option.adders}")

        # Check that exotic metals category is gone
        exotic_options = db.query(Option).filter_by(category="Exotic Metals").all()
        if exotic_options:
            print(f"\n❌ Found {len(exotic_options)} remaining exotic metal options")
        else:
            print("\n✅ No exotic metal options remaining")

    finally:
        db.close()


def main():
    """Run the complete exotic metals migration."""
    print("EXOTIC METALS MIGRATION TO MATERIALS")
    print("=" * 50)

    analyze_current_exotic_metals()

    # Confirm before proceeding
    response = input("\nProceed with migration? (y/N): ").strip().lower()
    if response != "y":
        print("Migration cancelled.")
        return

    add_exotic_metal_materials()
    update_material_options()
    remove_exotic_metals_options()
    verify_migration()

    print("\n" + "=" * 50)
    print("EXOTIC METALS MIGRATION COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()
