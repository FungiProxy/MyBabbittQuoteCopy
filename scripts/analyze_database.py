#!/usr/bin/env python3
"""
Comprehensive Database Analysis Script
Analyzes the entire database structure, indexes, and data content
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import inspect

from src.core.database import SessionLocal


def analyze_database():
    """Comprehensive database analysis"""

    print('=' * 80)
    print('COMPREHENSIVE DATABASE ANALYSIS')
    print('=' * 80)

    # Get database session and raw connection
    db = SessionLocal()
    engine = db.get_bind()
    inspector = inspect(engine)

    # Get raw SQLite connection for detailed queries
    raw_conn = engine.raw_connection()
    cursor = raw_conn.cursor()

    # 1. DATABASE OVERVIEW
    print('\n1. DATABASE OVERVIEW')
    print('-' * 40)

    # Get all tables
    tables = inspector.get_table_names()
    print(f'Total tables: {len(tables)}')
    print(f"Tables: {', '.join(sorted(tables))}")

    # Database file info
    cursor.execute('PRAGMA database_list')
    db_info = cursor.fetchall()
    for db_entry in db_info:
        print(f'Database file: {db_entry[2]}')

    # 2. TABLE SCHEMAS AND INDEXES
    print('\n2. TABLE SCHEMAS AND INDEXES')
    print('-' * 40)

    for table_name in sorted(tables):
        print(f'\nTable: {table_name}')
        print('=' * len(f'Table: {table_name}'))

        # Get columns
        columns = inspector.get_columns(table_name)
        print('Columns:')
        for i, col in enumerate(columns):
            nullable = 'NULL' if col['nullable'] else 'NOT NULL'
            default = f" DEFAULT {col['default']}" if col['default'] is not None else ''
            primary_key = ' PRIMARY KEY' if col.get('primary_key', False) else ''
            print(
                f"  {i}: {col['name']} {col['type']}{primary_key} {nullable}{default}"
            )

        # Get indexes
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print('Indexes:')
            for idx in indexes:
                unique = 'UNIQUE ' if idx['unique'] else ''
                print(
                    f"  {unique}INDEX {idx['name']}: {', '.join(idx['column_names'])}"
                )

        # Get foreign keys
        foreign_keys = inspector.get_foreign_keys(table_name)
        if foreign_keys:
            print('Foreign Keys:')
            for fk in foreign_keys:
                print(
                    f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}"
                )

        # Get row count
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        row_count = cursor.fetchone()[0]
        print(f'Row count: {row_count}')

    # 3. DATA ANALYSIS
    print('\n3. DATA ANALYSIS')
    print('-' * 40)

    for table_name in sorted(tables):
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        row_count = cursor.fetchone()[0]

        if row_count > 0:
            print(f'\n{table_name.upper()} ({row_count} rows)')
            print('-' * (len(table_name) + 10))

            # Show sample data (first 3 rows)
            cursor.execute(f'SELECT * FROM {table_name} LIMIT 3')
            rows = cursor.fetchall()

            # Get column names
            cursor.execute(f'PRAGMA table_info({table_name})')
            column_info = cursor.fetchall()
            column_names = [col[1] for col in column_info]

            if rows:
                print('Sample data (first 3 rows):')
                for i, row in enumerate(rows, 1):
                    print(f'  Row {i}:')
                    for col_name, value in zip(column_names, row):
                        # Truncate long values
                        if isinstance(value, str) and len(value) > 100:
                            display_value = value[:100] + '...'
                        else:
                            display_value = value
                        print(f'    {col_name}: {display_value}')
                    print()
        else:
            print(f'\n{table_name.upper()}: EMPTY')

    # 4. RELATIONSHIP ANALYSIS
    print('\n4. RELATIONSHIP ANALYSIS')
    print('-' * 40)

    relationships = {}
    for table_name in tables:
        foreign_keys = inspector.get_foreign_keys(table_name)
        if foreign_keys:
            relationships[table_name] = foreign_keys

    if relationships:
        print('Foreign Key relationships:')
        for table, fks in relationships.items():
            for fk in fks:
                print(
                    f"  {table}.{fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}"
                )
    else:
        print('No foreign key relationships found')

    # 5. SPECIFIC TABLE ANALYSIS
    print('\n5. SPECIFIC ANALYSIS FOR KEY TABLES')
    print('-' * 40)

    # Analyze options table specifically
    if 'options' in tables:
        print('\nOPTIONS TABLE DETAILED ANALYSIS:')
        cursor.execute(
            'SELECT name, category, product_families, COUNT(*) as count FROM options GROUP BY category ORDER BY category'
        )
        option_categories = cursor.fetchall()

        print('Options by category:')
        for category, _cat_name, _families, count in option_categories:
            if category:
                print(f'  {category}: {count} options')

        # Check for JSON columns
        cursor.execute('SELECT name, choices, adders FROM options LIMIT 1')
        sample_option = cursor.fetchone()
        if sample_option:
            print('\nSample option structure:')
            print(f'  Name: {sample_option[0]}')
            print(f'  Choices type: {type(sample_option[1])}')
            print(f'  Adders type: {type(sample_option[2])}')

    # Analyze material_options vs options overlap
    if 'material_options' in tables and 'options' in tables:
        print('\nMATERIAL DATA OVERLAP ANALYSIS:')

        cursor.execute('SELECT COUNT(*) FROM material_options')
        material_option_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM options WHERE category = 'Material'")
        options_material_count = cursor.fetchone()[0]

        print(f'  MaterialOption table: {material_option_count} records')
        print(f'  Options table (Material): {options_material_count} records')
        print('  OVERLAP DETECTED: Both tables contain material data')

    # Analyze voltage_options vs options overlap
    if 'voltage_options' in tables and 'options' in tables:
        print('\nVOLTAGE DATA OVERLAP ANALYSIS:')

        cursor.execute('SELECT COUNT(*) FROM voltage_options')
        voltage_option_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM options WHERE category = 'Electrical' AND name = 'Voltage'"
        )
        options_voltage_count = cursor.fetchone()[0]

        print(f'  VoltageOption table: {voltage_option_count} records')
        print(f'  Options table (Voltage): {options_voltage_count} records')
        print('  OVERLAP DETECTED: Both tables contain voltage data')

    # 6. ARCHITECTURE SUMMARY
    print('\n6. ARCHITECTURE SUMMARY')
    print('-' * 40)

    print('Current system architecture:')

    # Core product tables
    core_tables = [
        t for t in tables if t in ['product_families', 'product_variants', 'products']
    ]
    if core_tables:
        print(f"✓ Core product tables: {', '.join(core_tables)}")

    # Specific option tables
    specific_option_tables = [t for t in tables if 'option' in t and t != 'options']
    if specific_option_tables:
        print(f"✓ Specific option tables: {', '.join(specific_option_tables)}")

    # Generic options table
    if 'options' in tables:
        print('✓ Generic options table: options')

    # Quote system
    quote_tables = [t for t in tables if 'quote' in t]
    if quote_tables:
        print(f"✓ Quote system tables: {', '.join(quote_tables)}")

    # Other tables
    other_tables = [
        t
        for t in tables
        if t not in core_tables + specific_option_tables + quote_tables + ['options']
    ]
    if other_tables:
        print(f"✓ Other tables: {', '.join(other_tables)}")

    # Close connections
    cursor.close()
    raw_conn.close()
    db.close()

    print('\n' + '=' * 80)
    print('DATABASE ANALYSIS COMPLETE')
    print('=' * 80)


if __name__ == '__main__':
    analyze_database()
