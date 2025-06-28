#!/usr/bin/env python3
"""
Restore database from db6.27.sql
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.database import engine
from sqlalchemy import text

def restore_database():
    """Restore database from the SQL file."""
    print("=== RESTORING DATABASE FROM db6.27.sql ===")
    
    # Read the SQL file
    sql_file_path = Path(__file__).parent / "data" / "db6.27.sql"
    
    if not sql_file_path.exists():
        print(f"Error: SQL file not found at {sql_file_path}")
        return
    
    print(f"Reading SQL file: {sql_file_path}")
    
    with open(sql_file_path, 'r') as f:
        sql_content = f.read()
    
    # Split into individual statements
    statements = sql_content.split(';')
    
    print("Executing SQL statements...")
    
    with engine.connect() as conn:
        for i, statement in enumerate(statements):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    conn.execute(text(statement))
                    if i % 10 == 0:  # Progress indicator
                        print(f"  Executed {i+1}/{len(statements)} statements")
                except Exception as e:
                    print(f"Error executing statement {i+1}: {e}")
                    print(f"Statement: {statement[:100]}...")
        
        conn.commit()
    
    print("Database restoration complete!")
    
    # Verify the restoration
    print("\n=== VERIFICATION ===")
    with engine.connect() as conn:
        # Check tables
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Tables found: {len(tables)}")
        for table in sorted(tables):
            print(f"  - {table}")
        
        # Check options
        result = conn.execute(text("SELECT COUNT(*) FROM options"))
        options_count = result.scalar()
        print(f"\nOptions table: {options_count} rows")
        
        # Check product families
        result = conn.execute(text("SELECT COUNT(*) FROM product_families"))
        families_count = result.scalar()
        print(f"Product families: {families_count} rows")
        
        # Check product family options
        result = conn.execute(text("SELECT COUNT(*) FROM product_family_options"))
        pfo_count = result.scalar()
        print(f"Product family options: {pfo_count} relationships")

if __name__ == "__main__":
    restore_database() 