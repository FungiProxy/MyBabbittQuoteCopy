#!/usr/bin/env python3
"""
Export all relevant tables to JSON for snapshotting the current database state.
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import text
from src.core.database import engine

EXPORT_TABLES = [
    'options',
    'product_families',
    'product_family_options',
    'base_models',
    'materials',
    'length_adder_rules',
    'spare_parts',
    'standard_lengths',
]

EXPORT_DIR = Path(__file__).parent / 'db_snapshot'
EXPORT_DIR.mkdir(exist_ok=True)

def export_table(table):
    with engine.connect() as conn:
        result = conn.execute(text(f'SELECT * FROM {table}'))
        rows = [dict(row) for row in result.mappings()]
        with open(EXPORT_DIR / f'{table}.json', 'w', encoding='utf-8') as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
        print(f'Exported {len(rows)} rows from {table}')

def main():
    print(f'Exporting tables to {EXPORT_DIR}')
    for table in EXPORT_TABLES:
        export_table(table)
    print('Export complete.')

if __name__ == '__main__':
    main() 