#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductVariant, ProductFamily


def fix_variant_pricing():
    db = SessionLocal()
    try:
        print(
            "Fixing product variant base prices by removing baked-in material adders..."
        )

        # Define the base prices for each family (without material adders)
        base_prices = {
            "LS2000": 425.0,
            "LS2100": 460.0,
            "LS6000": 550.0,
            "LS7000": 680.0,
            "LS7000/2": 770.0,
            "LS7500": 800.0,
            "LS8000": 715.0,
            "LS8000/2": 850.0,  # Updated from 950.0
            "LS8500": 1050.0,
            "LT9000": 1200.0,
            "FS10000": 1885.0,  # Updated from 1500.0
        }

        # Material adders that were baked into the base prices
        material_adders = {
            "S": 0.0,
            "H": 110.0,
            "U": 20.0,
            "T": 60.0,
            "TS": 110.0,
            "CPVC": 400.0,
            "C": 80.0,
        }

        # Get all variants
        variants = db.query(ProductVariant).all()
        print(f"Found {len(variants)} variants to fix")

        fixed_count = 0
        for variant in variants:
            # Get the family name
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.id == variant.product_family_id)
                .first()
            )
            if not family:
                continue

            family_name = family.name
            material = variant.material

            # Calculate what the base price should be (family base only, no material adder)
            correct_base_price = base_prices.get(family_name, 500.0)

            # Check if the current base price includes a material adder
            current_material_adder = material_adders.get(material, 0.0)
            expected_total = correct_base_price + current_material_adder

            if abs(variant.base_price - expected_total) < 1.0:  # Within $1 tolerance
                # This variant has the material adder baked in, fix it
                variant.base_price = correct_base_price
                fixed_count += 1
                print(
                    f"  Fixed {variant.model_number}: ${expected_total:.2f} -> ${correct_base_price:.2f}"
                )

        db.commit()
        print(f"\n✅ Fixed {fixed_count} variants")

        # Show some examples
        print(f"\n=== SAMPLE FIXED VARIANTS ===")
        sample_variants = db.query(ProductVariant).limit(10).all()
        for variant in sample_variants:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.id == variant.product_family_id)
                .first()
            )
            print(f"  {variant.model_number}: ${variant.base_price:.2f}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_variant_pricing()
