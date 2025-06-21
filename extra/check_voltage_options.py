#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models import Option, ProductFamily


def check_voltage_options():
    db = SessionLocal()
    try:
        # Check all options
        all_options = db.query(Option).all()
        print(f"Found {len(all_options)} total options:")
        for opt in all_options:
            print(
                f"  {opt.name} ({opt.category}): {opt.choices} for {opt.product_families}"
            )

        # Check electrical options specifically
        electrical_options = (
            db.query(Option).filter(Option.category == "Electrical").all()
        )
        print(f"\nFound {len(electrical_options)} electrical options:")
        for opt in electrical_options:
            print(f"  {opt.name}: {opt.choices} for {opt.product_families}")

        # Check voltage options specifically
        voltage_options = db.query(Option).filter(Option.name == "Voltage").all()
        print(f"\nFound {len(voltage_options)} voltage options:")
        for opt in voltage_options:
            print(f"  {opt.name}: {opt.choices} for {opt.product_families}")

        # Check product families
        families = db.query(ProductFamily).all()
        print(f"\nFound {len(families)} product families:")
        for family in families:
            print(f"  {family.name} (ID: {family.id})")

    finally:
        db.close()


if __name__ == "__main__":
    check_voltage_options()
