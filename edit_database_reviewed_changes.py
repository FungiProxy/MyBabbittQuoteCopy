#!/usr/bin/env python3
"""
Script to apply the database edits we've reviewed so far.
This script will be updated as we continue the review process.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models import Option, StandardLength


def fix_standard_lengths():
    """Fix standard lengths: only material 'H' with specific lengths"""
    session = SessionLocal()
    try:
        print('Fixing standard lengths...')

        # Remove all standard lengths for material 'S'
        deleted_s = (
            session.query(StandardLength)
            .filter(StandardLength.material_code == 'S')
            .delete()
        )
        print(f"  Removed {deleted_s} standard lengths for material 'S'")

        # Remove any standard lengths for material 'H' that are not in the allowed list
        allowed_lengths = [6.0, 12.0, 18.0, 24.0, 36.0, 48.0, 60.0, 72.0]
        existing_h_lengths = (
            session.query(StandardLength)
            .filter(StandardLength.material_code == 'H')
            .all()
        )

        for sl in existing_h_lengths:
            if sl.length not in allowed_lengths:
                session.delete(sl)
                print(f"  Removed standard length {sl.length} for material 'H'")

        # Ensure all allowed lengths exist for material 'H'
        existing_lengths = [
            sl.length
            for sl in session.query(StandardLength)
            .filter(StandardLength.material_code == 'H')
            .all()
        ]

        for length in allowed_lengths:
            if length not in existing_lengths:
                new_sl = StandardLength(material_code='H', length=length)
                session.add(new_sl)
                print(f"  Added standard length {length} for material 'H'")

        session.commit()
        print('  Standard lengths fixed successfully')

    except Exception as e:
        session.rollback()
        print(f'  Error fixing standard lengths: {e}')
        raise
    finally:
        session.close()


def zero_out_option_prices():
    """Set all option price fields to 0.0 since we're using adders for pricing"""
    session = SessionLocal()
    try:
        print('Zeroing out option prices...')

        # Get all options with non-zero prices
        options_with_prices = session.query(Option).filter(Option.price != 0.0).all()

        for option in options_with_prices:
            old_price = option.price
            option.price = 0.0
            print(f"  Option '{option.name}' (ID {option.id}): {old_price} -> 0.0")

        session.commit()
        print(f'  Zeroed out prices for {len(options_with_prices)} options')

    except Exception as e:
        session.rollback()
        print(f'  Error zeroing option prices: {e}')
        raise
    finally:
        session.close()


def main():
    """Apply all reviewed changes to the database"""
    print('APPLYING REVIEWED DATABASE CHANGES')
    print('=' * 40)
    print()

    try:
        fix_standard_lengths()
        print()
        zero_out_option_prices()
        print()

        print('All reviewed changes applied successfully!')
        print()
        print('Next steps:')
        print('1. Continue reviewing remaining tables')
        print('2. Update this script with additional changes')
        print('3. Create proper seeding files for production')

    except Exception as e:
        print(f'Error applying changes: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
