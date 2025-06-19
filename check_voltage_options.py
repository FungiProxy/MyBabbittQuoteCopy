#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models import Option, ProductFamily


def check_voltage_options():
    db = SessionLocal()
    try:
        # Check all voltage options
        voltage_options = db.query(Option).filter(Option.category == "Voltage").all()
        print(f"Found {len(voltage_options)} voltage options:")
        for opt in voltage_options:
            print(f"  {opt.name}: {opt.choices}")
            print(f"    Adders: {opt.adders}")

        # Check a specific product family
        ls2000 = db.query(ProductFamily).filter(ProductFamily.name == "LS2000").first()
        if ls2000:
            print(f"\nLS2000 family ID: {ls2000.id}")
            # Get voltage options for LS2000
            from src.core.services.product_service import ProductService

            additional_options = ProductService().get_additional_options(db, "LS2000")
            print(f"Additional options for LS2000: {len(additional_options)}")
            for opt in additional_options:
                if opt.get("category") == "Voltage":
                    print(f"  Voltage option: {opt}")
    finally:
        db.close()


if __name__ == "__main__":
    check_voltage_options()
