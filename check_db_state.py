#!/usr/bin/env python3
"""
Check current database state
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.database import engine
from sqlalchemy import text

def check_database():
    print("=== DATABASE STATE CHECK ===")
    
    with engine.connect() as conn:
        # Check tables
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Tables found: {len(tables)}")
        for table in sorted(tables):
            print(f"  - {table}")
        
        print("\n=== TABLE CONTENTS ===")
        
        # Check options table
        if 'options' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM options"))
            count = result.scalar()
            print(f"Options table: {count} rows")
            
            if count > 0:
                result = conn.execute(text("SELECT name, category FROM options LIMIT 5"))
                for row in result.fetchall():
                    print(f"  - {row[0]} ({row[1]})")
        
        # Check product_families
        if 'product_families' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM product_families"))
            count = result.scalar()
            print(f"Product families: {count} rows")
        
        # Check if product_family_options exists
        if 'product_family_options' in tables:
            result = conn.execute(text("SELECT COUNT(*) FROM product_family_options"))
            count = result.scalar()
            print(f"Product family options: {count} relationships")
        
        # Check legacy tables
        legacy_tables = ['materials', 'material_options', 'voltage_options', 'connection_options']
        print("\n=== LEGACY TABLES ===")
        for table in legacy_tables:
            if table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f"{table}: {count} rows")

if __name__ == "__main__":
    check_database() 