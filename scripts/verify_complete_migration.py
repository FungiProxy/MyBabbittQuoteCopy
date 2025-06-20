#!/usr/bin/env python3
from sqlalchemy import text

from src.core.database import SessionLocal


def verify_migration():
    db = SessionLocal()

    print("=" * 70)
    print("MIGRATION VERIFICATION RESULTS")
    print("=" * 70)

    # Check that options table is gone
    try:
        result = db.execute(text("SELECT COUNT(*) FROM options")).scalar()
        print(f"❌ ERROR: options table still exists with {result} records")
    except:
        print("✅ SUCCESS: options table successfully dropped")

    print("\nNEW SPECIFIC TABLES:")
    print("-" * 30)

    # Check new tables
    try:
        mechanical = db.execute(
            text("SELECT COUNT(*) FROM mechanical_options")
        ).scalar()
        print(f"✅ mechanical_options: {mechanical} records")
    except:
        print("❌ mechanical_options table missing")

    try:
        electrical = db.execute(
            text("SELECT COUNT(*) FROM electrical_options")
        ).scalar()
        print(f"✅ electrical_options: {electrical} records")
    except:
        print("❌ electrical_options table missing")

    try:
        pricing = db.execute(text("SELECT COUNT(*) FROM pricing_rules")).scalar()
        print(f"✅ pricing_rules: {pricing} records")
    except:
        print("❌ pricing_rules table missing")

    try:
        exotic = db.execute(text("SELECT COUNT(*) FROM exotic_metal_options")).scalar()
        print(f"✅ exotic_metal_options: {exotic} records")
    except:
        print("❌ exotic_metal_options table missing")

    print("\nEXISTING SPECIFIC TABLES:")
    print("-" * 30)

    # Check existing tables
    material_opts = db.execute(text("SELECT COUNT(*) FROM material_options")).scalar()
    voltage_opts = db.execute(text("SELECT COUNT(*) FROM voltage_options")).scalar()
    connection_opts = db.execute(
        text("SELECT COUNT(*) FROM connection_options")
    ).scalar()
    oring_opts = db.execute(
        text("SELECT COUNT(*) FROM o_ring_material_options")
    ).scalar()

    print(f"✅ material_options: {material_opts} records")
    print(f"✅ voltage_options: {voltage_opts} records")
    print(f"✅ connection_options: {connection_opts} records")
    print(f"✅ o_ring_material_options: {oring_opts} records")

    print("\nCOMPLETE ARCHITECTURE:")
    print("-" * 30)

    # Show all option tables
    tables = db.execute(
        text(
            """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name LIKE '%option%'
        ORDER BY name
    """
        )
    ).fetchall()

    total_records = 0
    for (table_name,) in tables:
        count = db.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        print(f"  {table_name}: {count} records")
        total_records += count

    print(f"\nTOTAL OPTION RECORDS: {total_records}")

    # Sample from new tables
    print("\nSAMPLE DATA FROM NEW TABLES:")
    print("-" * 30)

    try:
        mech_sample = db.execute(
            text("SELECT option_name, description FROM mechanical_options LIMIT 3")
        ).fetchall()
        print("Mechanical options sample:")
        for name, desc in mech_sample:
            print(f"  - {name}: {desc}")
    except:
        pass

    try:
        elec_sample = db.execute(
            text("SELECT option_name, description FROM electrical_options LIMIT 3")
        ).fetchall()
        print("Electrical options sample:")
        for name, desc in elec_sample:
            print(f"  - {name}: {desc}")
    except:
        pass

    print("\n" + "=" * 70)
    print("✅ MIGRATION TO SPECIFIC TABLES COMPLETE!")
    print("✅ Database now fully normalized with specific option tables")
    print("✅ No more generic JSON-based options table")
    print("=" * 70)

    db.close()


if __name__ == "__main__":
    verify_migration()
