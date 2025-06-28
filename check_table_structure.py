#!/usr/bin/env python3
"""
Check table structure
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.database import engine
from sqlalchemy import text

def check_table_structure():
    with engine.connect() as conn:
        # Check voltage_options structure
        result = conn.execute(text("PRAGMA table_info(voltage_options)"))
        print("voltage_options columns:")
        for row in result.fetchall():
            print(f"  {row[1]} ({row[2]})")
        
        print("\nSample data:")
        result = conn.execute(text("SELECT * FROM voltage_options LIMIT 3"))
        for row in result.fetchall():
            print(f"  {row}")

if __name__ == "__main__":
    check_table_structure() 