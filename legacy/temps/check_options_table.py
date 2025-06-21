#!/usr/bin/env python3
"""Check the current state of the options table."""

from src.core.database import SessionLocal
from src.core.models.option import Option


def check_options_table():
    """Check what's currently in the options table."""
    db = SessionLocal()
    try:
        options = db.query(Option).all()
        print(f"Total options in table: {len(options)}")
        print("\nCurrent options:")
        print("-" * 80)

        for option in options:
            print(f"ID: {option.id}")
            print(f"Name: {option.name}")
            print(f"Category: {option.category}")
            print(f"Product Families: {option.product_families}")
            print(f"Price: {option.price}")
            print(f"Price Type: {option.price_type}")
            print(f"Choices: {option.choices}")
            print(f"Adders: {option.adders}")
            print(f"Rules: {option.rules}")
            print("-" * 80)

    finally:
        db.close()


if __name__ == "__main__":
    check_options_table()
