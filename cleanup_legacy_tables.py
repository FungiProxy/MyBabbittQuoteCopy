#!/usr/bin/env python3
"""
Cleanup script to remove legacy option tables.
This removes all the old option tables that are no longer needed after the refactor.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from sqlalchemy import inspect, text

from src.core.database import engine


def cleanup_legacy_tables():
    """Remove all legacy option tables."""
    print("=== LEGACY TABLE CLEANUP ===")

    # Tables to remove (legacy option tables)
    legacy_tables = [
        "material_options",
        "connection_options",
        "voltage_options",
        "housing_type_options",
        "o_ring_material_options",
        "exotic_metal_options",
        "probe_length_options",
        "cable_length_options",
        "material_availability",
        "products",  # This was also mentioned in the refactor plan as redundant
    ]

    # Tables to keep (core application tables)
    keep_tables = [
        "alembic_version",
        "product_families",
        "product_variants",
        "options",
        "product_family_options",
        "materials",
        "standard_lengths",
        "housing_types",
        "customers",
        "quotes",
        "quote_items",
        "quote_item_options",
        "spare_parts",
    ]

    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    print(f"Found {len(existing_tables)} tables in database")
    print(f"Will remove {len(legacy_tables)} legacy tables")
    print(f"Will keep {len(keep_tables)} core tables")

    # Check which legacy tables exist
    tables_to_remove = []
    for table in legacy_tables:
        if table in existing_tables:
            tables_to_remove.append(table)
            print(f"  ✅ Will remove: {table}")
        else:
            print(f"  ⚠️  Not found: {table}")

    if not tables_to_remove:
        print("\nNo legacy tables found to remove!")
        return

    # Confirm before proceeding
    print(f"\nAbout to remove {len(tables_to_remove)} tables:")
    for table in tables_to_remove:
        print(f"  - {table}")

    response = input("\nProceed with cleanup? (y/N): ").strip().lower()
    if response != "y":
        print("Cleanup cancelled.")
        return

    # Remove the tables
    print("\nRemoving legacy tables...")
    with engine.connect() as conn:
        for table in tables_to_remove:
            try:
                conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                print(f"  ✅ Removed: {table}")
            except Exception as e:
                print(f"  ❌ Error removing {table}: {e}")

        conn.commit()

    # Verify cleanup
    print("\n=== CLEANUP VERIFICATION ===")
    inspector = inspect(engine)
    remaining_tables = inspector.get_table_names()

    print(f"Tables remaining: {len(remaining_tables)}")
    print("\nRemaining tables:")
    for table in sorted(remaining_tables):
        status = "✅" if table in keep_tables else "⚠️"
        print(f"  {status} {table}")

    # Check for any unexpected tables
    unexpected = set(remaining_tables) - set(keep_tables)
    if unexpected:
        print(f"\n⚠️  Unexpected tables found: {unexpected}")
    else:
        print("\n✅ All legacy tables successfully removed!")
        print("Database is now clean and ready for the unified structure.")


if __name__ == "__main__":
    cleanup_legacy_tables()
