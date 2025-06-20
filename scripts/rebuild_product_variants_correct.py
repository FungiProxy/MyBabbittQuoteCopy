#!/usr/bin/env python3
"""
Rebuild Product Variants Table - Corrected Approach

This script rebuilds the product_variants table following the original design:
- Only create base variants with standard lengths (10" for most, 4" for blind-end)
- Let the application handle length customization with price adders
- Follow the original price list structure
"""

import os
import sys
from typing import List

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.core.models.option import Option
from src.core.models.product_variant import ProductFamily, ProductVariant


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

    return sorted(material_codes)


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

    return sorted(voltage_values)


def get_base_length_for_material(material: str) -> float:
    """Get the standard base length for a material based on the price list."""
    # Cable material uses 12" base length
    if material == "C":
        return 12.0
    # Blind-end materials use 4" base length
    blind_end_materials = ["U", "T", "CPVC"]
    if material in blind_end_materials:
        return 4.0
    else:
        return 10.0  # Standard length for S, H, TS


def generate_model_number(
    family_name: str, voltage: str, material: str, length: float
) -> str:
    """Generate a model number for a variant."""
    length_str = f'{int(length)}"' if length.is_integer() else f'{length}"'
    return f"{family_name}-{voltage}-{material}-{length_str}"


def get_base_price_for_family(family_name: str) -> float:
    """Get base price for a product family."""
    # Base prices from the original price list
    base_prices = {
        "LS2000": 425.0,
        "LS2100": 460.0,
        "LS6000": 550.0,
        "LS7000": 680.0,
        "LS7000/2": 770.0,
        "LS7500": 800.0,
        "LS8000": 715.0,
        "LS8000/2": 950.0,
        "LS8500": 1050.0,
        "LT9000": 1200.0,
        "FS10000": 1500.0,
    }
    return base_prices.get(family_name, 500.0)


def get_material_adder(material: str) -> float:
    """Get the material adder based on the price list."""
    # Material adders from the price list
    material_adders = {
        "S": 0.0,  # 316SS is base material
        "H": 110.0,  # Halar coated
        "U": 20.0,  # UHMWPE blind end
        "T": 60.0,  # Teflon blind end
        "TS": 110.0,  # Teflon sleeve
        "CPVC": 400.0,  # CPVC blind end
        "C": 80.0,  # Cable probe
    }
    return material_adders.get(material, 0.0)


def rebuild_product_variants_correct():
    """Rebuild the product variants table with correct base configurations only."""
    print("Starting product variants rebuild (corrected approach)...")

    db = SessionLocal()
    try:
        # Get all product families
        families = db.query(ProductFamily).all()
        print(f"Found {len(families)} product families")

        # Get available materials and voltages
        materials = get_available_materials(db)
        voltages = get_available_voltages(db)

        print(f"Available materials: {materials}")
        print(f"Available voltages: {voltages}")

        # Clear existing variants
        print("Clearing existing variants...")
        db.query(ProductVariant).delete()
        db.commit()

        # Create base variants only
        total_variants = 0

        for family in families:
            print(f"\nProcessing family: {family.name}")
            base_price = get_base_price_for_family(family.name)

            # Create variants for each material and voltage combination
            for material in materials:
                for voltage in voltages:
                    # Get the standard base length for this material
                    base_length = get_base_length_for_material(material)

                    # Calculate the total base price (family base + material adder)
                    material_adder = get_material_adder(material)
                    total_base_price = base_price + material_adder

                    # Generate model number
                    model_number = generate_model_number(
                        family.name, voltage, material, base_length
                    )

                    # Create variant
                    variant = ProductVariant(
                        product_family_id=family.id,
                        model_number=model_number,
                        description=f'{family.name} {voltage} {material} {base_length}"',
                        base_price=total_base_price,
                        base_length=base_length,
                        voltage=voltage,
                        material=material,
                    )

                    db.add(variant)
                    total_variants += 1

        # Commit all changes
        db.commit()
        print(f"\n✅ Successfully created {total_variants} base product variants")

        # Verify the results
        final_count = db.query(ProductVariant).count()
        print(f"Total variants in database: {final_count}")

        # Show sample of new variants
        print("\nSample of base variants:")
        sample_variants = db.query(ProductVariant).limit(15).all()
        for variant in sample_variants:
            print(
                f'  {variant.model_number} - ${variant.base_price} ({variant.base_length}")'
            )

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
    success = rebuild_product_variants_correct()
    sys.exit(0 if success else 1)
