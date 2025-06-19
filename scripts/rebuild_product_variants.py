#!/usr/bin/env python3
"""
Rebuild Product Variants Table

This script rebuilds the product_variants table to ensure all product families
have variants for all available materials, including newly added materials
like C (Cable) that were missing from the original variants.
"""

import sys
import os
from typing import List, Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal, engine
from src.core.models.product_variant import ProductFamily, ProductVariant
from src.core.models.option import Option
from sqlalchemy import text


def get_available_materials(db) -> List[str]:
    """Get all available material codes from the unified options."""
    materials = db.query(Option).filter(Option.category == "Material").all()
    material_codes = set()

    for material in materials:
        choices = material.choices
        if isinstance(choices, list):
            for choice in choices:
                if isinstance(choice, dict) and "code" in choice:
                    material_codes.add(choice["code"])
                elif isinstance(choice, str):
                    material_codes.add(choice)

    return sorted(list(material_codes))


def get_available_voltages(db) -> List[str]:
    """Get all available voltages from the unified options."""
    voltages = db.query(Option).filter(Option.category == "Voltage").all()
    voltage_values = set()

    for voltage in voltages:
        choices = voltage.choices
        if isinstance(choices, list):
            for choice in choices:
                if isinstance(choice, dict) and "code" in choice:
                    voltage_values.add(choice["code"])
                elif isinstance(choice, str):
                    voltage_values.add(choice)

    return sorted(list(voltage_values))


def get_base_lengths() -> List[float]:
    """Get standard base lengths for variants."""
    return [10.0, 12.0, 18.0, 24.0, 36.0, 48.0, 60.0, 72.0, 84.0, 96.0, 108.0, 120.0]


def generate_model_number(
    family_name: str, voltage: str, material: str, length: float
) -> str:
    """Generate a model number for a variant."""
    length_str = f'{int(length)}"' if length.is_integer() else f'{length}"'
    return f"{family_name}-{voltage}-{material}-{length_str}"


def get_base_price_for_family(family_name: str) -> float:
    """Get base price for a product family."""
    # Base prices from the original data
    base_prices = {
        "LS2000": 425.0,
        "LS2100": 450.0,
        "LS6000": 550.0,
        "LS7000": 650.0,
        "LS7000/2": 750.0,
        "LS7500": 800.0,
        "LS8000": 850.0,
        "LS8000/2": 950.0,
        "LS8500": 1050.0,
        "LT9000": 1200.0,
        "FS10000": 1500.0,
    }
    return base_prices.get(family_name, 500.0)


def rebuild_product_variants():
    """Rebuild the product variants table with all combinations."""
    print("Starting product variants rebuild...")

    db = SessionLocal()
    try:
        # Get all product families
        families = db.query(ProductFamily).all()
        print(f"Found {len(families)} product families")

        # Get available materials and voltages
        materials = get_available_materials(db)
        voltages = get_available_voltages(db)
        base_lengths = get_base_lengths()

        print(f"Available materials: {materials}")
        print(f"Available voltages: {voltages}")
        print(f"Base lengths: {base_lengths}")

        # Clear existing variants (optional - comment out if you want to keep existing)
        print("Clearing existing variants...")
        db.query(ProductVariant).delete()
        db.commit()

        # Create new variants for all combinations
        total_variants = 0

        for family in families:
            print(f"\nProcessing family: {family.name}")
            base_price = get_base_price_for_family(family.name)

            # Create variants for each material, voltage, and length combination
            for material in materials:
                for voltage in voltages:
                    for length in base_lengths:
                        # Generate model number
                        model_number = generate_model_number(
                            family.name, voltage, material, length
                        )

                        # Create variant
                        variant = ProductVariant(
                            product_family_id=family.id,
                            model_number=model_number,
                            description=f'{family.name} {voltage} {material} {length}"',
                            base_price=base_price,
                            base_length=length,
                            voltage=voltage,
                            material=material,
                        )

                        db.add(variant)
                        total_variants += 1

                        if total_variants % 100 == 0:
                            print(f"  Created {total_variants} variants...")

        # Commit all changes
        db.commit()
        print(f"\n✅ Successfully created {total_variants} product variants")

        # Verify the results
        final_count = db.query(ProductVariant).count()
        print(f"Total variants in database: {final_count}")

        # Show sample of new variants
        print("\nSample of new variants:")
        sample_variants = db.query(ProductVariant).limit(10).all()
        for variant in sample_variants:
            print(f"  {variant.model_number} - ${variant.base_price}")

        return True

    except Exception as e:
        print(f"❌ Error rebuilding product variants: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = rebuild_product_variants()
    sys.exit(0 if success else 1)
