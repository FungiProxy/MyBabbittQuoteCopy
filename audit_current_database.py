#!/usr/bin/env python3
"""
Audit script to examine current database state and identify all data
that needs to be preserved when rebuilding the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import engine, SessionLocal
from sqlalchemy import text, inspect
from src.core.models import (
    BaseModel, CableLengthOption, ConnectionOption, Customer, 
    HousingTypeOption, HousingType, MaterialAvailability,
    MaterialOption, Material, O_RingMaterialOption, Option, QuoteItemOption,
    ProductFamily, Quote, QuoteItem, SparePart, StandardLength, VoltageOption
)

def get_table_counts():
    """Get row counts for all tables"""
    session = SessionLocal()
    try:
        tables = [
            ('base_models', BaseModel),
            ('cable_length_options', CableLengthOption),
            ('connection_options', ConnectionOption),
            ('customers', Customer),
            ('housing_type_options', HousingTypeOption),
            ('housing_types', HousingType),
            ('material_availability', MaterialAvailability),
            ('material_options', MaterialOption),
            ('materials', Material),
            ('o_ring_material_options', O_RingMaterialOption),
            ('options', Option),
            ('product_families', ProductFamily),
            ('quote_item_options', QuoteItemOption),
            ('quote_items', QuoteItem),
            ('quotes', Quote),
            ('spare_parts', SparePart),
            ('standard_lengths', StandardLength),
            ('voltage_options', VoltageOption),
        ]
        
        print("=== CURRENT DATABASE STATE ===")
        print()
        
        for table_name, model in tables:
            try:
                count = session.query(model).count()
                print(f"{table_name}: {count} rows")
                
                # Show sample data for tables with data
                if count > 0 and count <= 10:
                    print(f"  Sample data:")
                    items = session.query(model).limit(3).all()
                    for item in items:
                        print(f"    {item}")
                elif count > 10:
                    print(f"  Sample data (first 3 of {count}):")
                    items = session.query(model).limit(3).all()
                    for item in items:
                        print(f"    {item}")
                print()
                
            except Exception as e:
                print(f"{table_name}: ERROR - {e}")
                print()
                
    finally:
        session.close()

def check_seeding_files():
    """Check what seeding files exist and what they cover"""
    print("=== SEEDING FILES ANALYSIS ===")
    print()
    
    seeding_files = [
        # Core configuration files
        ('src/core/config/base_models.py', 'Base models configuration'),
        ('src/core/config/connections.py', 'Connection options'),
        ('src/core/config/insulation.py', 'Insulation options'),
        ('src/core/config/materials.py', 'Materials configuration'),
        ('src/core/config/misc_options.py', 'Miscellaneous options'),
        ('src/core/config/product_families.py', 'Product families'),
        ('src/core/config/standard_lengths.py', 'Standard lengths'),
        ('src/core/config/voltages.py', 'Voltage options'),
        
        # Scripts directory seeding files
        ('scripts/data/init/init_business_config.py', 'Business configuration initialization'),
        ('scripts/data/init/init_sample_data.py', 'Sample data initialization'),
        
        # Product family specific seeding
        ('scripts/data/seeds/options/seed_options_ls2000.py', 'LS2000 options'),
        ('scripts/data/seeds/options/seed_options_ls6000.py', 'LS6000 options'),
        ('scripts/data/seeds/options/seed_options_ls7000.py', 'LS7000 options'),
        ('scripts/data/seeds/options/seed_options_ls7500.py', 'LS7500 options'),
        ('scripts/data/seeds/options/seed_options_ls8000.py', 'LS8000 options'),
        ('scripts/data/seeds/options/seed_options_ls8000_2.py', 'LS8000_2 options'),
        ('scripts/data/seeds/options/seed_options_ls8500.py', 'LS8500 options'),
        ('scripts/data/seeds/options/seed_options_lt9000.py', 'LT9000 options'),
        
        # Connection seeding
        ('scripts/data/seeds/options/seed_ls6000_connections.py', 'LS6000 connections'),
        ('scripts/data/seeds/options/seed_ls7000_2_connections.py', 'LS7000_2 connections'),
        ('scripts/data/seeds/options/seed_ls7000_connections.py', 'LS7000 connections'),
        ('scripts/data/seeds/options/seed_ls8000_2_connections.py', 'LS8000_2 connections'),
        ('scripts/data/seeds/options/seed_ls8000_connections.py', 'LS8000 connections'),
        ('scripts/data/seeds/options/seed_lt9000_connections.py', 'LT9000 connections'),
        
        # Presence/absence families
        ('scripts/data/seeds/options/seed_presence_absence_families.py', 'Presence/absence families'),
    ]
    
    for file_path, description in seeding_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
            print(f"  {description}")
        else:
            print(f"✗ {file_path} (MISSING)")
            print(f"  {description}")
        print()

def main():
    print("DATABASE AUDIT - CURRENT STATE vs SEEDING FILES")
    print("=" * 60)
    print()
    
    get_table_counts()
    check_seeding_files()
    
    print("=== RECOMMENDATIONS ===")
    print()
    print("1. Review the current database state above")
    print("2. Compare with seeding files to identify gaps")
    print("3. Create missing seeding files for any tables with data")
    print("4. Update existing seeding files to match current data")
    print("5. Test the complete seeding process before dropping database")

if __name__ == "__main__":
    main() 