#!/usr/bin/env python3
"""
Verification script to check the results of the migration to unified options table.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from sqlalchemy import text

from core.database import SessionLocal
from core.models.option import Option


def verify_migration():
    """Verify the migration results."""
    db = SessionLocal()

    try:
        # Get total count
        total_options = db.query(Option).count()
        print(f"Total options in unified table: {total_options}")

        # Get categories
        categories_result = db.execute(
            text("SELECT DISTINCT category FROM options ORDER BY category")
        ).fetchall()

        print("\nCategories found:")
        for row in categories_result:
            category = row[0]
            count = db.query(Option).filter_by(category=category).count()
            print(f"  - {category}: {count} options")

        # Show some sample options
        print("\nSample options by category:")
        for row in categories_result:
            category = row[0]
            sample_options = (
                db.query(Option).filter_by(category=category).limit(3).all()
            )
            print(f"\n{category}:")
            for opt in sample_options:
                families = opt.product_families or "None"
                print(f"  - {opt.name}: {families}")

        # Check for any options with choices
        options_with_choices = (
            db.query(Option).filter(Option.choices.isnot(None)).count()
        )
        print(f"\nOptions with choices data: {options_with_choices}")

        # Check for any options with adders
        options_with_adders = db.query(Option).filter(Option.adders.isnot(None)).count()
        print(f"Options with adders data: {options_with_adders}")

    finally:
        db.close()


if __name__ == "__main__":
    verify_migration()
