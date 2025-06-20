#!/usr/bin/env python3
"""
Analyze Remaining Options Script
Analyzes the 19 remaining options to design specific tables
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from src.core.database import SessionLocal


def analyze_remaining_options():
    """Analyze the remaining options for table design"""

    print("=" * 70)
    print("ANALYZING REMAINING OPTIONS FOR TABLE DESIGN")
    print("=" * 70)

    db = SessionLocal()

    try:
        # Get all remaining options with full details
        result = db.execute(
            text(
                """
            SELECT id, name, description, price, price_type, category,
                   product_families, choices, adders
            FROM options
            ORDER BY category, name
        """
            )
        ).fetchall()

        print(f"Total remaining options: {len(result)}")
        print()

        # Group by category for analysis
        categories = {}
        for row in result:
            id, name, desc, price, price_type, category, families, choices, adders = row

            if category not in categories:
                categories[category] = []

            # Parse JSON strings
            try:
                choices_list = json.loads(choices) if choices else []
                adders_dict = json.loads(adders) if adders else {}
            except:
                choices_list = choices
                adders_dict = adders

            categories[category].append(
                {
                    "id": id,
                    "name": name,
                    "description": desc,
                    "price": price,
                    "price_type": price_type,
                    "product_families": families,
                    "choices": choices_list,
                    "adders": adders_dict,
                }
            )

        # Analyze each category
        for category, options in categories.items():
            print(f"CATEGORY: {category} ({len(options)} options)")
            print("=" * 50)

            for opt in options:
                print(f"  Option: {opt['name']}")
                print(f"    Description: {opt['description']}")
                print(f"    Price: ${opt['price']} ({opt['price_type']})")
                print(f"    Families: {opt['product_families']}")
                print(f"    Choices: {opt['choices']}")
                print(f"    Adders: {opt['adders']}")
                print()

        # Design recommendations
        print("\nTABLE DESIGN RECOMMENDATIONS")
        print("=" * 50)

        print("\n1. MECHANICAL OPTIONS TABLE:")
        print("   - Bent Probe")
        print("   - Stainless Steel Tag")
        print('   - 3/4" Diameter Probe')
        print("   - Connection Type")
        print("   - Flange options")
        print("   - Tri-clamp options")
        print("   - NPT Size options")
        print("   - Enclosure options (LS7000, LS8000, LS8000/2)")

        print("\n2. ELECTRICAL OPTIONS TABLE:")
        print("   - Extra Static Protection")
        print("   - Twisted Shielded Pair")

        print("\n3. PRICING RULES TABLE:")
        print("   - Probe Length (Standard/Non-Standard)")
        print("   - Length Adder")

        print("\n4. EXOTIC METAL TABLE:")
        print("   - Exotic Metal pricing")

        print("\n5. O-RING OPTIONS (already exists):")
        print("   - O-Rings material selection")

        # Show specific table structures needed
        print("\nSPECIFIC TABLE STRUCTURES NEEDED:")
        print("=" * 50)

        mechanical_count = len([o for o in result if o[5] == "Mechanical"])
        electrical_count = len([o for o in result if o[5] == "Electrical"])
        pricing_count = len([o for o in result if o[5] == "Pricing"])
        exotic_count = len([o for o in result if o[5] == "Exotic Metal"])
        oring_count = len([o for o in result if o[5] == "O-ring Material"])

        print(f"mechanical_options: {mechanical_count} records to migrate")
        print(f"electrical_options: {electrical_count} records to migrate")
        print(f"pricing_rules: {pricing_count} records to migrate")
        print(f"exotic_metal_options: {exotic_count} records to migrate")
        print(f"(o_ring_material_options already exists: {oring_count} would stay)")

    finally:
        db.close()

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    analyze_remaining_options()
