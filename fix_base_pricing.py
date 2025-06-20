#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily, ProductVariant


def fix_base_pricing():
    db = SessionLocal()
    try:
        print("Fixing base pricing for specific models...")

        # Fix base prices for specific models (update all variants for each family)
        pricing_fixes = {
            "LS7000/2": 770,  # Should be 770, not 850
            "LS8000/2": 850,  # Should be 850, not 1030
            "LS9000": 855,  # Should be 855, not 1280
            "FS10000": 1885,  # Should be 1885, not 1580
        }

        for family_name, correct_price in pricing_fixes.items():
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if family:
                # Update all variants for this family
                variants = (
                    db.query(ProductVariant)
                    .filter(ProductVariant.product_family_id == family.id)
                    .all()
                )
                for variant in variants:
                    variant.base_price = correct_price
                print(
                    f"  Updated {len(variants)} variants for {family_name} to base price ${correct_price}"
                )

        # Set factory pricing for LS7500 and LS8500 (set base_price to None)
        factory_pricing_families = ["LS7500", "LS8500"]
        for family_name in factory_pricing_families:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if family:
                variants = (
                    db.query(ProductVariant)
                    .filter(ProductVariant.product_family_id == family.id)
                    .all()
                )
                for variant in variants:
                    variant.base_price = None  # No price shown - consult factory
                print(
                    f"  Set {len(variants)} variants for {family_name} to factory pricing"
                )

        db.commit()
        print("Base pricing fixes completed!")

        # Fix material assignments that got lost
        print("\nFixing material assignments...")
        families_to_fix = ["LS2000", "LS2100", "LS6000", "LS7000"]
        correct_order = ["S", "H", "TS", "U", "T", "C"]

        for family_name in families_to_fix:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if family:
                # Check if material assignments exist
                existing_assignments = (
                    db.query(ProductFamilyOption)
                    .filter(ProductFamilyOption.product_family_id == family.id)
                    .join(Option)
                    .filter(Option.category == "Material")
                    .count()
                )

                if existing_assignments == 0:
                    print(
                        f"  No material assignments found for {family_name}, adding them..."
                    )
                    # Add material assignments
                    for material_code in correct_order:
                        material_option = (
                            db.query(Option)
                            .filter(
                                Option.category == "Material",
                                Option.choices.contains([{"code": material_code}]),
                            )
                            .first()
                        )
                        if material_option:
                            db.add(
                                ProductFamilyOption(
                                    product_family_id=family.id,
                                    option_id=material_option.id,
                                    is_available=1,
                                )
                            )
                            print(f"    Added {material_code} to {family_name}")
                else:
                    print(
                        f"  {family_name} already has {existing_assignments} material assignments"
                    )

        db.commit()
        print("Material assignments fixed!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_base_pricing()
