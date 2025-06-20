#!/usr/bin/env python3
"""
Comprehensive database verification script.
This will check the current schema and data to see what's present and what needs to be restored.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal, engine
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily
from src.core.models.material import Material, StandardLength
from src.core.models.housing_type import HousingType
from sqlalchemy import text, inspect


def check_database_schema():
    """Check what tables exist in the database."""
    print("=== DATABASE SCHEMA VERIFICATION ===")
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"Total tables found: {len(tables)}")
    print("\nTables present:")
    for table in sorted(tables):
        print(f"  - {table}")
    
    # Check for legacy tables that should be removed
    legacy_tables = [
        'material_options', 'connection_options', 'voltage_options', 
        'housing_type_options', 'o_ring_material_options', 'exotic_metal_options',
        'probe_length_options', 'cable_length_options', 'material_availability'
    ]
    
    print("\nLegacy tables check:")
    for legacy_table in legacy_tables:
        if legacy_table in tables:
            print(f"  ⚠️  {legacy_table} - SHOULD BE REMOVED")
        else:
            print(f"  ✅ {legacy_table} - NOT PRESENT (GOOD)")
    
    # Check for required tables
    required_tables = [
        'product_families', 'options', 'product_family_options', 
        'materials', 'standard_lengths', 'housing_types'
    ]
    
    print("\nRequired tables check:")
    for required_table in required_tables:
        if required_table in tables:
            print(f"  ✅ {required_table} - PRESENT")
        else:
            print(f"  ❌ {required_table} - MISSING")
    
    return tables


def check_options_table():
    """Check the options table structure and data."""
    print("\n=== OPTIONS TABLE VERIFICATION ===")
    
    db = SessionLocal()
    try:
        # Check table structure
        inspector = inspect(engine)
        columns = inspector.get_columns('options')
        
        print("Options table columns:")
        required_columns = ['id', 'name', 'description', 'price', 'price_type', 'category', 'choices', 'adders', 'rules', 'product_families']
        
        for col in columns:
            status = "✅" if col['name'] in required_columns else "⚠️"
            print(f"  {status} {col['name']} ({col['type']})")
        
        # Check data
        options = db.query(Option).all()
        print(f"\nTotal options: {len(options)}")
        
        if options:
            print("\nSample options:")
            for option in options[:5]:
                print(f"  ID: {option.id}")
                print(f"  Name: {option.name}")
                print(f"  Category: {option.category}")
                print(f"  Product Families: {option.product_families}")
                print(f"  Choices: {option.choices}")
                print(f"  Adders: {option.adders}")
                print("  ---")
        
        # Check by category
        categories = db.query(Option.category).distinct().all()
        print(f"\nOption categories found: {len(categories)}")
        for cat in categories:
            count = db.query(Option).filter_by(category=cat[0]).count()
            print(f"  {cat[0]}: {count} options")
            
    finally:
        db.close()


def check_product_families():
    """Check product families data."""
    print("\n=== PRODUCT FAMILIES VERIFICATION ===")
    
    db = SessionLocal()
    try:
        families = db.query(ProductFamily).all()
        print(f"Total product families: {len(families)}")
        
        expected_families = [
            'LS2000', 'LS2100', 'LS6000', 'LS7000', 'LS7000/2', 
            'LS8000', 'LS8000/2', 'LT9000', 'FS10000', 'LS7500', 'LS8500'
        ]
        
        print("\nProduct families check:")
        for family in families:
            status = "✅" if family.name in expected_families else "⚠️"
            print(f"  {status} {family.name} - {family.category}")
        
        missing = set(expected_families) - {f.name for f in families}
        if missing:
            print(f"\n❌ Missing families: {missing}")
            
    finally:
        db.close()


def check_materials():
    """Check materials data."""
    print("\n=== MATERIALS VERIFICATION ===")
    
    db = SessionLocal()
    try:
        materials = db.query(Material).all()
        print(f"Total materials: {len(materials)}")
        
        expected_materials = ['S', 'H', 'TS', 'U', 'T', 'C', 'CPVC']
        
        print("\nMaterials check:")
        for material in materials:
            status = "✅" if material.code in expected_materials else "⚠️"
            print(f"  {status} {material.code} - {material.name}")
        
        missing = set(expected_materials) - {m.code for m in materials}
        if missing:
            print(f"\n❌ Missing materials: {missing}")
            
    finally:
        db.close()


def check_relationships():
    """Check product family options relationships."""
    print("\n=== RELATIONSHIPS VERIFICATION ===")
    
    db = SessionLocal()
    try:
        # Check if product_family_options table exists
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'product_family_options' in tables:
            relationships = db.query(ProductFamilyOption).all()
            print(f"Total product family ↔ option relationships: {len(relationships)}")
            
            if relationships:
                print("\nSample relationships:")
                for rel in relationships[:5]:
                    family = db.query(ProductFamily).filter_by(id=rel.product_family_id).first()
                    option = db.query(Option).filter_by(id=rel.option_id).first()
                    if family and option:
                        print(f"  {family.name} ↔ {option.name} ({option.category})")
        else:
            print("❌ product_family_options table not found")
            
    finally:
        db.close()


def check_data_completeness():
    """Check if the data is complete for the unified structure."""
    print("\n=== DATA COMPLETENESS CHECK ===")
    
    db = SessionLocal()
    try:
        # Check if options have choices and adders
        options_without_choices = db.query(Option).filter(Option.choices.is_(None)).count()
        options_without_adders = db.query(Option).filter(Option.adders.is_(None)).count()
        
        print(f"Options without choices: {options_without_choices}")
        print(f"Options without adders: {options_without_adders}")
        
        # Check if options have product_families
        options_without_families = db.query(Option).filter(Option.product_families.is_(None)).count()
        print(f"Options without product_families: {options_without_families}")
        
        # Check for key option categories
        key_categories = ['Material', 'Voltage', 'Connection Type', 'O-Rings', 'Exotic Metal']
        print("\nKey option categories check:")
        for category in key_categories:
            count = db.query(Option).filter_by(category=category).count()
            status = "✅" if count > 0 else "❌"
            print(f"  {status} {category}: {count} options")
            
    finally:
        db.close()


def main():
    """Run all verification checks."""
    print("DATABASE VERIFICATION REPORT")
    print("=" * 50)
    
    tables = check_database_schema()
    check_options_table()
    check_product_families()
    check_materials()
    check_relationships()
    check_data_completeness()
    
    print("\n" + "=" * 50)
    print("VERIFICATION COMPLETE")
    print("=" * 50)


if __name__ == '__main__':
    main() 