#!/usr/bin/env python3
"""
Detailed Database Analysis Script
Focuses on specific data patterns, pricing consistency, and identifies missing or problematic data
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))


from src.core.database import SessionLocal


def detailed_analysis():
    """Detailed database analysis focusing on specific issues"""

    print("=" * 80)
    print("DETAILED DATABASE ANALYSIS")
    print("=" * 80)

    # Get database session and raw connection
    db = SessionLocal()
    engine = db.get_bind()
    raw_conn = engine.raw_connection()
    cursor = raw_conn.cursor()

    # 1. PRICING DATA CONSISTENCY ANALYSIS
    print("\n1. PRICING DATA CONSISTENCY ANALYSIS")
    print("-" * 50)

    # Check material pricing consistency between materials and material_options
    print("Material Pricing Consistency:")
    cursor.execute(
        """
        SELECT
            m.code,
            m.name as material_name,
            m.base_price_adder as materials_price,
            COUNT(mo.id) as option_count,
            GROUP_CONCAT(DISTINCT mo.base_price) as option_prices,
            GROUP_CONCAT(DISTINCT pf.name) as product_families
        FROM materials m
        LEFT JOIN material_options mo ON m.code = mo.material_code
        LEFT JOIN product_families pf ON mo.product_family_id = pf.id
        GROUP BY m.code, m.name, m.base_price_adder
        ORDER BY m.code
    """
    )
    material_pricing = cursor.fetchall()

    for row in material_pricing:
        code, name, base_price, count, option_prices, families = row
        print(f"  {code} ({name}):")
        print(f"    Base price: ${base_price}")
        print(f"    Option prices: {option_prices}")
        print(f"    Used in {count} product families: {families}")
        if option_prices and str(base_price) not in option_prices.split(","):
            print("    ⚠️  PRICING INCONSISTENCY DETECTED!")
        print()

    # 2. MISSING OPTION COVERAGE ANALYSIS
    print("\n2. MISSING OPTION COVERAGE ANALYSIS")
    print("-" * 50)

    # Check which product families are missing various option types
    print("Option Coverage by Product Family:")
    cursor.execute(
        """
        SELECT
            pf.id,
            pf.name,
            COUNT(DISTINCT mo.id) as material_options,
            COUNT(DISTINCT vo.id) as voltage_options,
            COUNT(DISTINCT co.id) as connection_options,
            COUNT(DISTINCT hto.id) as housing_options,
            COUNT(DISTINCT oro.id) as oring_options
        FROM product_families pf
        LEFT JOIN material_options mo ON pf.id = mo.product_family_id
        LEFT JOIN voltage_options vo ON pf.id = vo.product_family_id
        LEFT JOIN connection_options co ON pf.id = co.product_family_id
        LEFT JOIN housing_type_options hto ON pf.id = hto.product_family_id
        LEFT JOIN o_ring_material_options oro ON pf.id = oro.product_family_id
        GROUP BY pf.id, pf.name
        ORDER BY pf.name
    """
    )
    coverage_data = cursor.fetchall()

    for row in coverage_data:
        family_id, name, materials, voltages, connections, housing, orings = row
        print(f"  {name} (ID: {family_id}):")
        print(
            f"    Materials: {materials}, Voltages: {voltages}, Connections: {connections}"
        )
        print(f"    Housing: {housing}, O-rings: {orings}")

        # Flag missing coverage
        missing = []
        if materials == 0:
            missing.append("Materials")
        if voltages == 0:
            missing.append("Voltages")
        if connections == 0:
            missing.append("Connections")
        if housing == 0:
            missing.append("Housing")
        if orings == 0:
            missing.append("O-rings")

        if missing:
            print(f"    ⚠️  MISSING: {', '.join(missing)}")
        print()

    # 3. PRODUCT VARIANT ANALYSIS
    print("\n3. PRODUCT VARIANT ANALYSIS")
    print("-" * 50)

    # Check product variant distribution and pricing
    cursor.execute(
        """
        SELECT
            pf.name as family,
            COUNT(*) as variant_count,
            MIN(pv.base_price) as min_price,
            MAX(pv.base_price) as max_price,
            AVG(pv.base_price) as avg_price,
            COUNT(DISTINCT pv.voltage) as voltage_count,
            COUNT(DISTINCT pv.material) as material_count
        FROM product_variants pv
        JOIN product_families pf ON pv.product_family_id = pf.id
        GROUP BY pf.name
        ORDER BY variant_count DESC
    """
    )
    variant_analysis = cursor.fetchall()

    print("Product Variant Distribution:")
    for row in variant_analysis:
        family, count, min_p, max_p, avg_p, v_count, m_count = row
        print(f"  {family}: {count} variants")
        print(f"    Price range: ${min_p:.2f} - ${max_p:.2f} (avg: ${avg_p:.2f})")
        print(f"    Voltages: {v_count}, Materials: {m_count}")
        print()

    # 4. DATA QUALITY ISSUES
    print("\n4. DATA QUALITY ISSUES")
    print("-" * 50)

    # Check for null/empty critical fields
    print("Missing Critical Data:")

    # Product families without descriptions
    cursor.execute(
        "SELECT COUNT(*) FROM product_families WHERE description IS NULL OR description = ''"
    )
    missing_pf_desc = cursor.fetchone()[0]
    if missing_pf_desc > 0:
        print(f"  ⚠️  {missing_pf_desc} product families missing descriptions")

    # Product variants without descriptions
    cursor.execute(
        "SELECT COUNT(*) FROM product_variants WHERE description IS NULL OR description = ''"
    )
    missing_pv_desc = cursor.fetchone()[0]
    if missing_pv_desc > 0:
        print(f"  ⚠️  {missing_pv_desc} product variants missing descriptions")

    # Materials without proper pricing
    cursor.execute("SELECT COUNT(*) FROM materials WHERE base_price_adder IS NULL")
    missing_material_price = cursor.fetchone()[0]
    if missing_material_price > 0:
        print(f"  ⚠️  {missing_material_price} materials missing base price adders")

    # 5. UNUSED/ORPHANED DATA
    print("\n5. UNUSED/ORPHANED DATA ANALYSIS")
    print("-" * 50)

    # Check for unused base tables
    cursor.execute(
        """
        SELECT
            'materials' as table_name,
            m.code,
            m.name,
            CASE WHEN mo.material_code IS NULL THEN 'UNUSED' ELSE 'USED' END as status
        FROM materials m
        LEFT JOIN material_options mo ON m.code = mo.material_code
        WHERE mo.material_code IS NULL

        UNION ALL

        SELECT
            'voltages' as table_name,
            CAST(v.id AS TEXT) as code,
            v.name,
            CASE WHEN vo.voltage_id IS NULL THEN 'UNUSED' ELSE 'USED' END as status
        FROM voltages v
        LEFT JOIN voltage_options vo ON v.id = vo.voltage_id
        WHERE vo.voltage_id IS NULL

        UNION ALL

        SELECT
            'housing_types' as table_name,
            CAST(ht.id AS TEXT) as code,
            ht.name,
            CASE WHEN hto.housing_type_id IS NULL THEN 'UNUSED' ELSE 'USED' END as status
        FROM housing_types ht
        LEFT JOIN housing_type_options hto ON ht.id = hto.housing_type_id
        WHERE hto.housing_type_id IS NULL

        UNION ALL

        SELECT
            'o_ring_materials' as table_name,
            CAST(orm.id AS TEXT) as code,
            orm.name,
            CASE WHEN oro.o_ring_material_id IS NULL THEN 'UNUSED' ELSE 'USED' END as status
        FROM o_ring_materials orm
        LEFT JOIN o_ring_material_options oro ON orm.id = oro.o_ring_material_id
        WHERE oro.o_ring_material_id IS NULL
    """
    )
    unused_data = cursor.fetchall()

    if unused_data:
        print("Unused Base Table Entries:")
        for table, code, name, status in unused_data:
            print(f"  ⚠️  {table}: {name} ({code}) - {status}")
    else:
        print("✓ No unused base table entries found")

    # 6. CABLE LENGTH OPTIONS ANALYSIS
    print("\n6. CABLE LENGTH OPTIONS ANALYSIS")
    print("-" * 50)

    cursor.execute("SELECT COUNT(*) FROM cable_length_options")
    cable_count = cursor.fetchone()[0]
    if cable_count == 0:
        print("⚠️  CABLE LENGTH OPTIONS TABLE IS EMPTY")
        print("   Based on price list, some products have cable probe options (+$80)")
    else:
        print(f"✓ Cable length options: {cable_count} entries")

    # 7. SPECIFIC OPTION PRICING FROM PRICE LIST
    print("\n7. MISSING OPTIONS FROM PRICE LIST ANALYSIS")
    print("-" * 50)

    # Check for specific options mentioned in price list that might be missing
    print("Known options from price list that should be in database:")

    missing_options = []

    # Check for cable probe option
    cursor.execute(
        "SELECT COUNT(*) FROM options WHERE name LIKE '%cable%' OR name LIKE '%Cable%'"
    )
    cable_option_count = cursor.fetchone()[0]
    if cable_option_count == 0:
        missing_options.append("Cable Probe (+$80)")

    # Check for bent probe option
    cursor.execute(
        "SELECT COUNT(*) FROM options WHERE name LIKE '%bent%' OR name LIKE '%Bent%'"
    )
    bent_option_count = cursor.fetchone()[0]
    if bent_option_count == 0:
        missing_options.append("Bent Probe (+$50)")

    # Check for stainless steel tag option
    cursor.execute(
        "SELECT COUNT(*) FROM options WHERE name LIKE '%tag%' OR name LIKE '%Tag%'"
    )
    tag_option_count = cursor.fetchone()[0]
    if tag_option_count == 0:
        missing_options.append("Stainless Steel Tag (+$30)")

    # Check for teflon insulator option
    cursor.execute(
        "SELECT COUNT(*) FROM options WHERE name LIKE '%teflon%insulator%' OR name LIKE '%Teflon%Insulator%'"
    )
    teflon_insulator_count = cursor.fetchone()[0]
    if teflon_insulator_count == 0:
        missing_options.append("Teflon Insulator (+$40)")

    if missing_options:
        print("⚠️  Missing options that should be added:")
        for option in missing_options:
            print(f"    - {option}")
    else:
        print("✓ All major options appear to be present")

    # 8. EXOTIC METALS ANALYSIS
    print("\n8. EXOTIC METALS ANALYSIS")
    print("-" * 50)

    # Check if exotic metals table exists or if they're handled differently
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%exotic%'"
    )
    exotic_tables = cursor.fetchall()

    if not exotic_tables:
        print("⚠️  NO EXOTIC METALS TABLE FOUND")
        print(
            "   Price list mentions: Alloy 20, Hastelloy C-276, Hastelloy B, Titanium"
        )
        print("   These should be available as material options")
    else:
        print(f"✓ Exotic metals tables found: {[t[0] for t in exotic_tables]}")

    # Close connections
    cursor.close()
    raw_conn.close()
    db.close()

    print("\n" + "=" * 80)
    print("DETAILED ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    detailed_analysis()
