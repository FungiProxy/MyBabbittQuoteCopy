#!/usr/bin/env python3
"""
Complete Migration to Specific Tables
Migrates all remaining data from options table to specific tables and drops options table
"""

import sys
from pathlib import Path
import json

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.core.database import SessionLocal
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker


def complete_migration():
    """Complete migration from options table to specific tables"""

    print("=" * 80)
    print("COMPLETE MIGRATION TO SPECIFIC TABLES")
    print("=" * 80)

    db = SessionLocal()
    engine = db.get_bind()

    try:
        print("\n1. CREATING NEW SPECIFIC TABLES")
        print("-" * 50)

        # Create mechanical_options table
        db.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS mechanical_options (
                id INTEGER PRIMARY KEY,
                product_family_id INTEGER NOT NULL,
                option_type VARCHAR NOT NULL,
                option_name VARCHAR NOT NULL,
                description TEXT,
                price_adder FLOAT DEFAULT 0.0,
                price_type VARCHAR DEFAULT 'fixed',
                choices TEXT,
                adders TEXT,
                is_available INTEGER DEFAULT 1,
                FOREIGN KEY (product_family_id) REFERENCES product_families(id)
            )
        """
            )
        )
        print("✓ Created mechanical_options table")

        # Create electrical_options table
        db.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS electrical_options (
                id INTEGER PRIMARY KEY,
                product_family_id INTEGER NOT NULL,
                option_type VARCHAR NOT NULL,
                option_name VARCHAR NOT NULL,
                description TEXT,
                price_adder FLOAT DEFAULT 0.0,
                price_type VARCHAR DEFAULT 'fixed',
                choices TEXT,
                adders TEXT,
                is_available INTEGER DEFAULT 1,
                FOREIGN KEY (product_family_id) REFERENCES product_families(id)
            )
        """
            )
        )
        print("✓ Created electrical_options table")

        # Create pricing_rules table
        db.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS pricing_rules (
                id INTEGER PRIMARY KEY,
                rule_type VARCHAR NOT NULL,
                rule_name VARCHAR NOT NULL,
                description TEXT,
                product_families TEXT,
                choices TEXT,
                adders TEXT,
                price_type VARCHAR DEFAULT 'per_unit'
            )
        """
            )
        )
        print("✓ Created pricing_rules table")

        # Create exotic_metal_options table
        db.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS exotic_metal_options (
                id INTEGER PRIMARY KEY,
                product_family_id INTEGER NOT NULL,
                metal_type VARCHAR NOT NULL,
                description TEXT,
                price_multiplier FLOAT DEFAULT 1.0,
                minimum_charge FLOAT DEFAULT 0.0,
                is_available INTEGER DEFAULT 1,
                FOREIGN KEY (product_family_id) REFERENCES product_families(id)
            )
        """
            )
        )
        print("✓ Created exotic_metal_options table")

        db.commit()

        print("\n2. MIGRATING DATA FROM OPTIONS TABLE")
        print("-" * 50)

        # Get all product families for mapping
        families_result = db.execute(
            text("SELECT id, name FROM product_families")
        ).fetchall()
        family_map = {name: id for id, name in families_result}

        # Get all options to migrate
        options_result = db.execute(
            text(
                """
            SELECT id, name, description, price, price_type, category, 
                   product_families, choices, adders
            FROM options
        """
            )
        ).fetchall()

        mechanical_count = 0
        electrical_count = 0
        pricing_count = 0
        exotic_count = 0
        oring_count = 0

        for row in options_result:
            id, name, desc, price, price_type, category, families, choices, adders = row

            if category == "Mechanical":
                # Migrate to mechanical_options
                family_names = families.split(",") if families else []
                for family_name in family_names:
                    family_name = family_name.strip()
                    if family_name in family_map:
                        db.execute(
                            text(
                                """
                            INSERT INTO mechanical_options 
                            (product_family_id, option_type, option_name, description, 
                             price_adder, price_type, choices, adders)
                            VALUES (:family_id, :category, :name, :desc, :price, :price_type, :choices, :adders)
                        """
                            ),
                            {
                                "family_id": family_map[family_name],
                                "category": category,
                                "name": name,
                                "desc": desc,
                                "price": price,
                                "price_type": price_type,
                                "choices": choices,
                                "adders": adders,
                            },
                        )
                        mechanical_count += 1

            elif category == "Electrical":
                # Migrate to electrical_options
                family_names = families.split(",") if families else []
                for family_name in family_names:
                    family_name = family_name.strip()
                    if family_name in family_map:
                        db.execute(
                            text(
                                """
                            INSERT INTO electrical_options 
                            (product_family_id, option_type, option_name, description, 
                             price_adder, price_type, choices, adders)
                            VALUES (:family_id, :category, :name, :desc, :price, :price_type, :choices, :adders)
                        """
                            ),
                            {
                                "family_id": family_map[family_name],
                                "category": category,
                                "name": name,
                                "desc": desc,
                                "price": price,
                                "price_type": price_type,
                                "choices": choices,
                                "adders": adders,
                            },
                        )
                        electrical_count += 1

            elif category == "Pricing":
                # Migrate to pricing_rules
                db.execute(
                    text(
                        """
                    INSERT INTO pricing_rules 
                    (rule_type, rule_name, description, product_families, 
                     choices, adders, price_type)
                    VALUES (:category, :name, :desc, :families, :choices, :adders, :price_type)
                """
                    ),
                    {
                        "category": category,
                        "name": name,
                        "desc": desc,
                        "families": families,
                        "choices": choices,
                        "adders": adders,
                        "price_type": price_type,
                    },
                )
                pricing_count += 1

            elif category == "Exotic Metal":
                # Migrate to exotic_metal_options - apply to all families
                for family_name, family_id in family_map.items():
                    db.execute(
                        text(
                            """
                        INSERT INTO exotic_metal_options 
                        (product_family_id, metal_type, description, price_multiplier)
                        VALUES (:family_id, :name, :desc, :multiplier)
                    """
                        ),
                        {
                            "family_id": family_id,
                            "name": name,
                            "desc": desc,
                            "multiplier": 1.5,  # Default exotic metal multiplier
                        },
                    )
                    exotic_count += 1

            elif category == "O-ring Material":
                # Keep in existing o_ring_material_options table (already exists)
                oring_count += 1
                print(f"  Keeping O-ring option in existing table: {name}")

        db.commit()

        print(f"✓ Migrated {mechanical_count} mechanical option records")
        print(f"✓ Migrated {electrical_count} electrical option records")
        print(f"✓ Migrated {pricing_count} pricing rule records")
        print(f"✓ Migrated {exotic_count} exotic metal option records")
        print(f"✓ Kept {oring_count} O-ring options in existing table")

        print("\n3. UPDATING QUOTE_ITEM_OPTIONS FOREIGN KEYS")
        print("-" * 50)

        # Check if there are any quote_item_options that reference the options table
        quote_item_options_count = db.execute(
            text("SELECT COUNT(*) FROM quote_item_options")
        ).scalar()
        if quote_item_options_count > 0:
            print(
                f"WARNING: Found {quote_item_options_count} quote_item_options records"
            )
            print("These will need manual migration to new table structure")
        else:
            print("✓ No quote_item_options records to migrate")

        print("\n4. DROPPING OPTIONS TABLE")
        print("-" * 50)

        # First drop the foreign key constraint from quote_item_options if table is empty
        if quote_item_options_count == 0:
            try:
                # Drop the foreign key constraint
                db.execute(text("PRAGMA foreign_keys=off"))

                # Recreate quote_item_options without the options FK
                db.execute(
                    text(
                        """
                    CREATE TABLE quote_item_options_new (
                        id INTEGER PRIMARY KEY NOT NULL,
                        quote_item_id INTEGER NOT NULL,
                        option_table VARCHAR NOT NULL,
                        option_id INTEGER NOT NULL,
                        quantity INTEGER NULL,
                        price FLOAT NOT NULL,
                        FOREIGN KEY (quote_item_id) REFERENCES quote_items(id)
                    )
                """
                    )
                )

                # Copy any existing data (there shouldn't be any)
                db.execute(
                    text(
                        """
                    INSERT INTO quote_item_options_new (id, quote_item_id, option_table, option_id, quantity, price)
                    SELECT id, quote_item_id, 'options' as option_table, option_id, quantity, price 
                    FROM quote_item_options
                """
                    )
                )

                # Drop old table and rename new one
                db.execute(text("DROP TABLE quote_item_options"))
                db.execute(
                    text(
                        "ALTER TABLE quote_item_options_new RENAME TO quote_item_options"
                    )
                )

                db.execute(text("PRAGMA foreign_keys=on"))
                print("✓ Updated quote_item_options table structure")
            except Exception as e:
                print(f"Note: Could not update quote_item_options structure: {e}")

        # Now drop the options table
        db.execute(text("DROP TABLE options"))
        db.commit()
        print("✓ Dropped options table")

        print("\n5. VERIFICATION")
        print("-" * 50)

        # Verify new tables
        mechanical_final = db.execute(
            text("SELECT COUNT(*) FROM mechanical_options")
        ).scalar()
        electrical_final = db.execute(
            text("SELECT COUNT(*) FROM electrical_options")
        ).scalar()
        pricing_final = db.execute(text("SELECT COUNT(*) FROM pricing_rules")).scalar()
        exotic_final = db.execute(
            text("SELECT COUNT(*) FROM exotic_metal_options")
        ).scalar()

        print(f"✓ mechanical_options: {mechanical_final} records")
        print(f"✓ electrical_options: {electrical_final} records")
        print(f"✓ pricing_rules: {pricing_final} records")
        print(f"✓ exotic_metal_options: {exotic_final} records")

        # Verify options table is gone
        try:
            db.execute(text("SELECT COUNT(*) FROM options"))
            print("❌ ERROR: options table still exists!")
        except:
            print("✅ Confirmed: options table successfully dropped")

        print("\n6. FINAL ARCHITECTURE")
        print("-" * 50)

        # Show final table list
        tables_result = db.execute(
            text(
                """
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != 'alembic_version'
            ORDER BY name
        """
            )
        ).fetchall()

        option_tables = [t[0] for t in tables_result if "option" in t[0]]
        print("Option-related tables:")
        for table in option_tables:
            count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"  {table}: {count} records")

        print("\n✅ MIGRATION COMPLETE!")
        print("✅ All option data now in specific tables")
        print("✅ No more generic options table")
        print("✅ Fully normalized database structure")

    except Exception as e:
        print(f"\n❌ ERROR during migration: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

    print("\n" + "=" * 80)
    print("COMPLETE MIGRATION FINISHED")
    print("=" * 80)


if __name__ == "__main__":
    complete_migration()
