#!/usr/bin/env python3
"""
Clean Up Duplicate Data Script
Removes redundant material and voltage records from options table
since this data is already properly stored in specific tables.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from src.core.database import SessionLocal
from src.core.models.option import Option


def cleanup_duplicate_data():
    """Remove duplicate material and voltage data from options table"""

    print('=' * 60)
    print('CLEANING UP DUPLICATE DATA')
    print('=' * 60)

    db = SessionLocal()

    try:
        # 1. Show current state
        print('\n1. CURRENT STATE ANALYSIS')
        print('-' * 30)

        # Count all options by category
        result = db.execute(
            text(
                """
            SELECT category, COUNT(*) as count
            FROM options
            GROUP BY category
            ORDER BY category
        """
            )
        ).fetchall()

        print('Current options by category:')
        total_options = 0
        for category, count in result:
            print(f'  {category}: {count} records')
            total_options += count
        print(f'  TOTAL: {total_options} records')

        # Show specific duplicates
        material_count = db.query(Option).filter(Option.category == 'Material').count()
        voltage_count = (
            db.query(Option)
            .filter(Option.category == 'Electrical', Option.name == 'Voltage')
            .count()
        )

        print('\nDuplicate data to remove:')
        print(
            f'  Material options: {material_count} records (duplicates material_options table)'
        )
        print(
            f'  Voltage options: {voltage_count} records (duplicates voltage_options table)'
        )

        # 2. Show what will be preserved
        print('\n2. DATA TO PRESERVE')
        print('-' * 30)

        preserved_options = db.execute(
            text(
                """
            SELECT name, category, COUNT(*) as count
            FROM options
            WHERE category NOT IN ('Material')
            AND NOT (category = 'Electrical' AND name = 'Voltage')
            GROUP BY name, category
            ORDER BY category, name
        """
            )
        ).fetchall()

        print('Options that will be preserved:')
        preserved_count = 0
        for name, category, count in preserved_options:
            print(f'  {category}: {name} ({count} records)')
            preserved_count += count
        print(f'  TOTAL PRESERVED: {preserved_count} records')

        # 3. Confirm deletion
        to_delete = material_count + voltage_count
        print(f'\nWILL DELETE: {to_delete} duplicate records')
        print(f'WILL PRESERVE: {preserved_count} unique records')

        # 4. Perform cleanup
        print('\n3. PERFORMING CLEANUP')
        print('-' * 30)

        # Delete material options (duplicates of material_options table)
        material_deleted = (
            db.query(Option).filter(Option.category == 'Material').delete()
        )
        print(f'✓ Deleted {material_deleted} Material category records')

        # Delete voltage options (duplicates of voltage_options table)
        voltage_deleted = (
            db.query(Option)
            .filter(Option.category == 'Electrical', Option.name == 'Voltage')
            .delete()
        )
        print(f'✓ Deleted {voltage_deleted} Voltage records from Electrical category')

        # Commit changes
        db.commit()
        print('✓ Changes committed to database')

        # 5. Verify cleanup
        print('\n4. VERIFICATION')
        print('-' * 30)

        # Count remaining options
        remaining_result = db.execute(
            text(
                """
            SELECT category, COUNT(*) as count
            FROM options
            GROUP BY category
            ORDER BY category
        """
            )
        ).fetchall()

        print('Remaining options by category:')
        remaining_total = 0
        for category, count in remaining_result:
            print(f'  {category}: {count} records')
            remaining_total += count
        print(f'  TOTAL REMAINING: {remaining_total} records')

        # Verify no duplicates remain
        material_check = db.query(Option).filter(Option.category == 'Material').count()
        voltage_check = (
            db.query(Option)
            .filter(Option.category == 'Electrical', Option.name == 'Voltage')
            .count()
        )

        if material_check == 0 and voltage_check == 0:
            print('\n✅ SUCCESS: All duplicate data removed!')
            print('✅ Material options now only in material_options table')
            print('✅ Voltage options now only in voltage_options table')
        else:
            print(
                f'\n❌ WARNING: Still found {material_check} material + {voltage_check} voltage duplicates'
            )

        print('\nCLEANUP SUMMARY:')
        print(f'  Started with: {total_options} options')
        print(f'  Removed: {material_deleted + voltage_deleted} duplicates')
        print(f'  Remaining: {remaining_total} unique options')

    except Exception as e:
        print(f'\n❌ ERROR during cleanup: {e!s}')
        db.rollback()
        raise
    finally:
        db.close()

    print('\n' + '=' * 60)
    print('DUPLICATE DATA CLEANUP COMPLETE')
    print('=' * 60)


if __name__ == '__main__':
    cleanup_duplicate_data()
