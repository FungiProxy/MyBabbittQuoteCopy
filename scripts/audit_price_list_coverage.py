#!/usr/bin/env python3
"""
Audit script to verify database coverage against the price list requirements.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


from core.database import SessionLocal
from core.models.option import Option, ProductFamilyOption
from core.models.product_variant import ProductFamily, ProductVariant


def audit_price_list_coverage():
    """Audit the database against price list requirements."""
    db = SessionLocal()

    try:
        print("=" * 80)
        print("PRICE LIST COVERAGE AUDIT")
        print("=" * 80)

        # 1. Check Product Families
        print("\n1. PRODUCT FAMILIES")
        print("-" * 40)
        families = db.query(ProductFamily).all()
        print(f"Total product families in database: {len(families)}")

        expected_families = {
            "LS2000",
            "LS2100",
            "LS6000",
            "LS7000",
            "LS7000/2",
            "LS8000",
            "LS8000/2",
            "LT9000",
            "FS10000",
            "LS7500",
            "LS8500",
        }

        db_family_names = {f.name for f in families}
        missing_families = expected_families - db_family_names
        extra_families = db_family_names - expected_families

        print(f"Expected families: {len(expected_families)}")
        print(f"Found families: {len(db_family_names)}")

        if missing_families:
            print(f"❌ MISSING families: {missing_families}")
        else:
            print("✅ All expected families present")

        if extra_families:
            print(f"⚠️  EXTRA families: {extra_families}")

        # 2. Check Options by Category
        print("\n2. OPTIONS BY CATEGORY")
        print("-" * 40)

        # Get all options with their relationships
        options = db.query(Option).all()
        print(f"Total options: {len(options)}")

        # Group by category
        categories = {}
        for opt in options:
            if opt.category not in categories:
                categories[opt.category] = []
            categories[opt.category].append(opt)

        for category, opts in categories.items():
            print(f"\n{category}: {len(opts)} options")
            for opt in opts[:3]:  # Show first 3
                families_str = (
                    ", ".join([f.name for f in opt.product_families])
                    if opt.product_families
                    else "None"
                )
                print(f"  - {opt.name}: {families_str}")
            if len(opts) > 3:
                print(f"  ... and {len(opts) - 3} more")

        # 3. Check Material Options (from price list)
        print("\n3. MATERIAL OPTIONS AUDIT")
        print("-" * 40)

        material_options = db.query(Option).filter_by(category="Material").all()
        print(f"Material options found: {len(material_options)}")

        # Check for specific materials mentioned in price list
        expected_materials = {
            "S": "316 Stainless Steel",
            "H": "Halar Coated",
            "U": "UHMWPE Blind End",
            "T": "Teflon Blind End",
            "TS": "Teflon Sleeve",
            "CPVC": "CPVC Blind End",
        }

        found_materials = set()
        for opt in material_options:
            if opt.choices:
                for choice in opt.choices:
                    if isinstance(choice, dict) and "code" in choice:
                        found_materials.add(choice["code"])
                    elif isinstance(choice, str):
                        found_materials.add(choice)

        print(f"Found material codes: {found_materials}")
        missing_materials = set(expected_materials.keys()) - found_materials
        if missing_materials:
            print(f"❌ MISSING materials: {missing_materials}")
        else:
            print("✅ All expected materials present")

        # 4. Check Voltage Options
        print("\n4. VOLTAGE OPTIONS AUDIT")
        print("-" * 40)

        voltage_options = db.query(Option).filter_by(category="Voltage").all()
        print(f"Voltage options found: {len(voltage_options)}")

        expected_voltages = {"115VAC", "24VDC", "12VDC", "240VAC", "230VAC"}
        found_voltages = set()
        for opt in voltage_options:
            if opt.choices:
                for choice in opt.choices:
                    if isinstance(choice, str):
                        found_voltages.add(choice)

        print(f"Found voltages: {found_voltages}")
        missing_voltages = expected_voltages - found_voltages
        if missing_voltages:
            print(f"❌ MISSING voltages: {missing_voltages}")
        else:
            print("✅ All expected voltages present")

        # 5. Check Connection Options
        print("\n5. CONNECTION OPTIONS AUDIT")
        print("-" * 40)

        connection_options = db.query(Option).filter_by(category="Connection").all()
        print(f"Connection options found: {len(connection_options)}")

        # Check for specific connection types from price list

        found_connections = set()
        for opt in connection_options:
            if opt.choices:
                for choice in opt.choices:
                    if isinstance(choice, str):
                        found_connections.add(choice)

        print(f"Found connection types: {found_connections}")

        # 6. Check Product Variants
        print("\n6. PRODUCT VARIANTS AUDIT")
        print("-" * 40)

        variants = db.query(ProductVariant).all()
        print(f"Total product variants: {len(variants)}")

        # Check for specific variants mentioned in price list
        expected_variants = [
            'LS2000-115VAC-S-10"',
            'LS2000-115VAC-H-10"',
            'LS2000-115VAC-U-4"',
            'LS2000-115VAC-T-4"',
            'LS2100-24VDC-S-10"',
            'LS2100-24VDC-H-10"',
            'LS6000-115VAC-S-10"',
            'LS6000-115VAC-H-10"',
            'LS7000-115VAC-S-10"',
            'LS7000-115VAC-H-10"',
            'LS7000/2-115VAC-H-10"',
            'LS8000-115VAC-S-10"',
            'LS8000-115VAC-H-10"',
            'LS8000/2-115VAC-H-10"',
            'LT9000-115VAC-H-10"',
        ]

        db_variant_models = {v.model_number for v in variants}
        found_variants = []
        missing_variants = []

        for expected in expected_variants:
            # Remove quotes for comparison
            clean_expected = expected.replace('"', "")
            if clean_expected in db_variant_models:
                found_variants.append(expected)
            else:
                missing_variants.append(expected)

        print(f"Found key variants: {len(found_variants)}/{len(expected_variants)}")
        if missing_variants:
            print(f"❌ MISSING variants: {missing_variants[:5]}...")  # Show first 5
        else:
            print("✅ All expected variants present")

        # 7. Check Pricing Information
        print("\n7. PRICING INFORMATION AUDIT")
        print("-" * 40)

        # Check if options have proper pricing data
        options_with_pricing = 0
        options_with_adders = 0

        for opt in options:
            if opt.price is not None and opt.price > 0:
                options_with_pricing += 1
            if opt.adders and len(opt.adders) > 0:
                options_with_adders += 1

        print(f"Options with base pricing: {options_with_pricing}/{len(options)}")
        print(f"Options with adders: {options_with_adders}/{len(options)}")

        # 8. Check Relationships
        print("\n8. RELATIONSHIP AUDIT")
        print("-" * 40)

        relationships = db.query(ProductFamilyOption).count()
        print(f"Total product_family_options relationships: {relationships}")

        # Check coverage per family
        for family in families:
            family_relationships = (
                db.query(ProductFamilyOption)
                .filter_by(product_family_id=family.id)
                .count()
            )
            print(f"  {family.name}: {family_relationships} options")

        # 9. Summary
        print("\n9. SUMMARY")
        print("-" * 40)

        issues = []
        if missing_families:
            issues.append(f"Missing {len(missing_families)} product families")
        if missing_materials:
            issues.append(f"Missing {len(missing_materials)} material types")
        if missing_voltages:
            issues.append(f"Missing {len(missing_voltages)} voltage options")
        if missing_variants:
            issues.append(f"Missing {len(missing_variants)} key product variants")

        if issues:
            print("❌ ISSUES FOUND:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(
                "✅ Database appears to have good coverage of price list requirements"
            )

        print(f"\nTotal options: {len(options)}")
        print(f"Total relationships: {relationships}")
        print(f"Total variants: {len(variants)}")

    finally:
        db.close()


if __name__ == "__main__":
    audit_price_list_coverage()
