#!/usr/bin/env python3
"""
Detailed database analysis script.
This will examine the database more thoroughly to understand what we actually have.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from sqlalchemy import inspect

from src.core.database import SessionLocal, engine
from src.core.models.material import Material
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def analyze_options_in_detail():
    """Analyze the options table in detail."""
    print("=== DETAILED OPTIONS ANALYSIS ===")

    db = SessionLocal()
    try:
        # Get all options
        options = db.query(Option).all()
        print(f"Total options: {len(options)}")

        # Analyze by category
        categories = db.query(Option.category).distinct().all()
        print(f"\nCategories found: {len(categories)}")

        for cat in categories:
            category_options = db.query(Option).filter_by(category=cat[0]).all()
            print(f"\n--- {cat[0]} ({len(category_options)} options) ---")

            for opt in category_options:
                print(f"  ID: {opt.id}")
                print(f"  Name: {opt.name}")
                print(f"  Product Families: {opt.product_families}")
                print(f"  Choices: {opt.choices}")
                print(f"  Adders: {opt.adders}")
                print(f"  Price: {opt.price}")
                print(f"  Price Type: {opt.price_type}")
                print("  ---")

    finally:
        db.close()


def analyze_product_families():
    """Analyze product families in detail."""
    print("\n=== DETAILED PRODUCT FAMILIES ANALYSIS ===")

    db = SessionLocal()
    try:
        families = db.query(ProductFamily).all()
        print(f"Total product families: {len(families)}")

        for family in families:
            print(f"\n--- {family.name} ---")
            print(f"  ID: {family.id}")
            print(f"  Category: {family.category}")
            print(f"  Description: {family.description}")

    finally:
        db.close()


def analyze_materials():
    """Analyze materials in detail."""
    print("\n=== DETAILED MATERIALS ANALYSIS ===")

    db = SessionLocal()
    try:
        materials = db.query(Material).all()
        print(f"Total materials: {len(materials)}")

        for material in materials:
            print(f"\n--- {material.code} ---")
            print(f"  ID: {material.id}")
            print(f"  Name: {material.name}")
            print(f"  Description: {material.description}")
            print(f"  Base Length: {material.base_length}")
            print(f"  Length Adder Per Inch: {material.length_adder_per_inch}")
            print(f"  Length Adder Per Foot: {material.length_adder_per_foot}")
            print(f"  Base Price Adder: {material.base_price_adder}")

    finally:
        db.close()


def analyze_relationships():
    """Analyze relationships in detail."""
    print("\n=== DETAILED RELATIONSHIPS ANALYSIS ===")

    db = SessionLocal()
    try:
        # Check product_family_options table
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if "product_family_options" in tables:
            relationships = db.query(ProductFamilyOption).all()
            print(
                f"Total relationships in product_family_options: {len(relationships)}"
            )

            if relationships:
                print("\nSample relationships:")
                for rel in relationships[:10]:
                    family = (
                        db.query(ProductFamily)
                        .filter_by(id=rel.product_family_id)
                        .first()
                    )
                    option = db.query(Option).filter_by(id=rel.option_id).first()
                    if family and option:
                        print(f"  {family.name} ↔ {option.name} ({option.category})")
            else:
                print("  No relationships found")
        else:
            print("product_family_options table not found")

    finally:
        db.close()


def analyze_table_structure():
    """Analyze the structure of key tables."""
    print("\n=== TABLE STRUCTURE ANALYSIS ===")

    inspector = inspect(engine)
    key_tables = ["options", "product_families", "materials", "product_family_options"]

    for table in key_tables:
        if table in inspector.get_table_names():
            columns = inspector.get_columns(table)
            print(f"\n--- {table} table structure ---")
            for col in columns:
                print(f"  {col['name']}: {col['type']} (nullable: {col['nullable']})")
        else:
            print(f"\n--- {table} table not found ---")


def check_for_voltage_options():
    """Check if voltage options exist but are categorized differently."""
    print("\n=== VOLTAGE OPTIONS SEARCH ===")

    db = SessionLocal()
    try:
        # Search for voltage-related options
        voltage_options = (
            db.query(Option)
            .filter(
                Option.name.contains("Voltage")
                | Option.name.contains("voltage")
                | Option.category.contains("Electrical")
            )
            .all()
        )

        print(f"Found {len(voltage_options)} voltage-related options:")
        for opt in voltage_options:
            print(f"  ID: {opt.id}, Name: {opt.name}, Category: {opt.category}")
            print(f"  Choices: {opt.choices}")
            print(f"  Product Families: {opt.product_families}")
            print("  ---")

    finally:
        db.close()


def check_for_connection_options():
    """Check if connection options exist but are categorized differently."""
    print("\n=== CONNECTION OPTIONS SEARCH ===")

    db = SessionLocal()
    try:
        # Search for connection-related options
        connection_options = (
            db.query(Option)
            .filter(
                Option.name.contains("Connection")
                | Option.name.contains("connection")
                | Option.name.contains("NPT")
                | Option.name.contains("Flange")
                | Option.name.contains("Tri-clamp")
            )
            .all()
        )

        print(f"Found {len(connection_options)} connection-related options:")
        for opt in connection_options:
            print(f"  ID: {opt.id}, Name: {opt.name}, Category: {opt.category}")
            print(f"  Choices: {opt.choices}")
            print(f"  Product Families: {opt.product_families}")
            print("  ---")

    finally:
        db.close()


def main():
    """Run all detailed analyses."""
    print("DETAILED DATABASE ANALYSIS")
    print("=" * 60)

    analyze_table_structure()
    analyze_options_in_detail()
    analyze_product_families()
    analyze_materials()
    analyze_relationships()
    check_for_voltage_options()
    check_for_connection_options()

    print("\n" + "=" * 60)
    print("DETAILED ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
