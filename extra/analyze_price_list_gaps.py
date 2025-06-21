#!/usr/bin/env python3
"""
Analyze price list to identify database gaps and required updates.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.material import Material
from src.core.models.option import Option
from src.core.models.product_variant import ProductFamily


def analyze_price_list_requirements():
    """Analyze the price list to identify database requirements."""
    print("PRICE LIST ANALYSIS - DATABASE REQUIREMENTS")
    print("=" * 60)

    # Based on price list analysis, here are the key findings:

    print("\n1. MATERIAL CODES AND PRICING")
    print("-" * 30)
    print("Current materials in database vs price list:")
    print("  Database: S, H, TS, U, T, C, CPVC, A, HB, HC, TT")
    print("  Price List: S, H, TS, U, T, C, CPVC")
    print("  ✅ Exotic metals (A, HB, HC, TT) already added")

    print("\n2. VOLTAGE OPTIONS")
    print("-" * 30)
    print("Price list shows these voltage options:")
    print("  - 115VAC (standard)")
    print("  - 12VDC (some models)")
    print("  - 24VDC (most models)")
    print("  - 230VAC/240VAC (most models)")
    print("  - 220VAC (some models)")

    print("\n3. CONNECTION TYPES")
    print("-" * 30)
    print("Price list shows these connection options:")
    print('  - 3/4" NPT (standard)')
    print('  - 1" NPT (some models)')
    print("  - Flange connections (various sizes)")
    print("  - Tri-clamp connections")

    print("\n4. PROBE LENGTHS")
    print("-" * 30)
    print("Price list shows:")
    print(
        '  - Standard lengths: 4", 6", 8", 10", 12", 18", 24", 36", 48", 60", 72", 84"'
    )
    print("  - Length adders: $45/foot for SS, $110/foot for Halar")
    print("  - Non-standard length surcharge: $300")

    print("\n5. SPECIAL OPTIONS")
    print("-" * 30)
    print("Price list shows these options:")
    print("  - Teflon Insulator (instead of UHMWPE/Delrin): +$40")
    print('  - 3/4" Diameter Probe: +$175')
    print("  - Cable Probe: +$80")
    print("  - Bent Probe: +$50")
    print("  - Stainless Steel Tag: +$30")
    print("  - Extra Static Protection: +$30")
    print("  - Flanged Mounting: Consult Factory")
    print("  - Tri-clamp Mounting: Consult Factory")

    print("\n6. O-RING MATERIALS")
    print("-" * 30)
    print("Price list shows:")
    print("  - Viton (standard)")
    print("  - Silicon (no extra charge)")
    print("  - Buna-N (no extra charge)")
    print("  - EPDM (no extra charge)")
    print("  - Kalrez: +$295 per probe")

    print("\n7. INSULATORS")
    print("-" * 30)
    print("Price list shows insulator options:")
    print("  - Delrin (standard for SS probes)")
    print("  - Teflon (standard for Halar/TS probes)")
    print("  - PEEK: +$340")
    print("  - Ceramic (1400F, dry materials only): +$470")
    print('  - Teflon Insulator lengths: 6", 8", 10", 12" with varying prices')

    print("\n8. HOUSING TYPES")
    print("-" * 30)
    print("Price list shows:")
    print("  - Standard housing")
    print("  - Stainless Steel Housing (NEMA 4X): +$285")
    print("  - Various enclosures for remote mounting")

    print("\n9. PRODUCT FAMILY SPECIFIC REQUIREMENTS")
    print("-" * 30)
    print("LS2000:")
    print("  - 24VDC at no extra charge")
    print("  - 12VDC and 240VAC not available")
    print("  - Limited static protection")

    print("\nLS2100:")
    print("  - Loop powered (8mA to 16mA)")
    print("  - 24VDC only")

    print("\nLS6000/LS7000:")
    print("  - 12VDC, 24VDC, 240VAC at no extra charge")
    print("  - CPVC Blind End Probe with Integrated NPT Nipple")
    print('  - 3/4" NPT max 300 psi @ 75F')

    print("\nLS7000/2:")
    print("  - Dual point level switch")
    print("  - Only Halar coated probes")
    print("  - Auto fill/empty applications only")

    print("\nLS8000:")
    print("  - Remote mounted")
    print("  - Cable options: 22 AWG twisted shielded pair")
    print("  - Various enclosures available")

    print("\nLT9000:")
    print("  - Continuous level transmitter")
    print("  - Only Halar coated probes")
    print("  - 24VDC and 230VAC available")

    print("\nLS7500/LS8500:")
    print("  - Presence/Absence switches")
    print("  - Flange sensors: PR (Partial Ring), FR (Full Ring)")
    print('  - Various flange sizes: 2", 2.5", 3", 4", 6", 8", 10"')

    print("\nFS10000:")
    print("  - Dry material flow switch")
    print('  - 1.5", 3", 6" probes same price')
    print("  - 230VAC available")
    print("  - Additional coaxial cable: +$6/foot")


def check_current_database_state():
    """Check current database state against price list requirements."""
    print("\n\nCURRENT DATABASE STATE ANALYSIS")
    print("=" * 60)

    db = SessionLocal()
    try:
        # Check materials
        materials = db.query(Material).all()
        print(f"\nMaterials in database: {len(materials)}")
        for material in materials:
            print(f"  {material.code} - {material.name}")

        # Check options by category
        options = db.query(Option).all()
        categories = {}
        for option in options:
            cat = option.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(option)

        print("\nOptions by category:")
        for category, opts in categories.items():
            print(f"  {category}: {len(opts)} options")
            for opt in opts[:3]:  # Show first 3
                print(f"    - {opt.name} ({opt.product_families})")
            if len(opts) > 3:
                print(f"    ... and {len(opts) - 3} more")

        # Check product families
        families = db.query(ProductFamily).all()
        print(f"\nProduct families: {len(families)}")
        for family in families:
            print(f"  {family.name} - {family.description}")

    finally:
        db.close()


def identify_missing_components():
    """Identify what's missing from the database."""
    print("\n\nMISSING COMPONENTS ANALYSIS")
    print("=" * 60)

    print("\n1. VOLTAGE OPTIONS - NEED TO ADD/UPDATE")
    print("-" * 40)
    print("Current voltage options may not include all from price list:")
    print("  Need to verify: 12VDC, 24VDC, 115VAC, 230VAC, 240VAC, 220VAC")

    print("\n2. CONNECTION TYPES - NEED TO ADD")
    print("-" * 40)
    print("Missing connection options:")
    print("  - Flange connections (various sizes)")
    print("  - Tri-clamp connections")
    print('  - 1" NPT process connection')

    print("\n3. SPECIAL OPTIONS - NEED TO ADD")
    print("-" * 40)
    print("Missing option categories:")
    print("  - Teflon Insulator option")
    print('  - 3/4" Diameter Probe option')
    print("  - Cable Probe option")
    print("  - Bent Probe option")
    print("  - Stainless Steel Tag option")
    print("  - Extra Static Protection option")
    print("  - Housing options (Stainless Steel, etc.)")

    print("\n4. O-RING MATERIALS - NEED TO UPDATE")
    print("-" * 40)
    print("Current O-ring options may not include:")
    print("  - Kalrez O-rings (+$295)")
    print("  - Silicon, Buna-N, EPDM (no extra charge)")

    print("\n5. INSULATOR OPTIONS - NEED TO ADD")
    print("-" * 40)
    print("Missing insulator options:")
    print("  - PEEK Insulator (+$340)")
    print("  - Ceramic Insulator (+$470)")
    print("  - Teflon Insulator length options")

    print("\n6. PRODUCT FAMILY SPECIFIC RULES - NEED TO ADD")
    print("-" * 40)
    print("Missing business rules:")
    print("  - Voltage restrictions (e.g., LS2000 no 12VDC/240VAC)")
    print("  - Material restrictions (e.g., LS7000/2 only Halar)")
    print('  - Probe length restrictions (e.g., Halar max 72")')
    print("  - Application-specific requirements")

    print("\n7. PRICING LOGIC - NEED TO UPDATE")
    print("-" * 40)
    print("Missing pricing rules:")
    print("  - Length adders ($45/foot SS, $110/foot Halar)")
    print("  - Non-standard length surcharge ($300)")
    print("  - CPVC pricing (base + $50 per additional inch)")
    print("  - Cable pricing ($6/foot additional)")

    print("\n8. SPARE PARTS - NEED TO ADD")
    print("-" * 40)
    print("Missing spare parts categories:")
    print("  - Electronics (various models)")
    print("  - Probe assemblies")
    print("  - Housings")
    print("  - Power supplies")
    print("  - Sensing cards")


def main():
    """Run the complete price list analysis."""
    analyze_price_list_requirements()
    check_current_database_state()
    identify_missing_components()

    print("\n\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    print("1. Add missing voltage options")
    print("2. Add connection type options (flanges, tri-clamp)")
    print("3. Add special options category")
    print("4. Update O-ring materials")
    print("5. Add insulator options")
    print("6. Add product family specific rules")
    print("7. Update pricing logic for length adders")
    print("8. Add spare parts system")
    print("9. Add business rules for material/voltage restrictions")


if __name__ == "__main__":
    main()
