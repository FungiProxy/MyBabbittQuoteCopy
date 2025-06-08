"""
Script to seed the database with LS8500 options (Presence/Absence Switches).
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal, init_db
from src.core.models.option import Option

FAMILY_NAME = "LS8500"

EXAMPLE_OPTIONS = [
    Option(
        name="Flange Size",
        description="Size of the flange (inches)",
        product_families=FAMILY_NAME,
        price=None,
        price_type="fixed",
        category="Mechanical",
        choices=["2\"", "2.5\"", "3\"", "4\"", "6\"", "8\"", "10\""],
        adders={},
        rules="Standard flanges are 316SS Flat Face Flanges. For other flange sizes, consult factory.",
        excluded_products=""
    ),
    Option(
        name="Flange Type",
        description="Type of flange sensor",
        product_families=FAMILY_NAME,
        price=None,
        price_type="fixed",
        category="Mechanical",
        choices=["PR", "FR"],
        adders={},
        rules="PR = Partial Ring (Conductive Media), FR = Full Ring (Non-Conductive Media)",
        excluded_products=""
    ),
    Option(
        name="Voltage",
        description="Supply voltage for the product",
        product_families=FAMILY_NAME,
        price=None,
        price_type="fixed",
        category="Electrical",
        choices=["115VAC", "24VDC", "220VAC", "12VDC"],
        adders={},
        rules=None,
        excluded_products=""
    ),
    Option(
        name="Teflon Insulator",
        description="Teflon insulator option (only for 6-10\" flanges)",
        product_families=FAMILY_NAME,
        price=400.0,
        price_type="fixed",
        category="Mechanical",
        choices=["No", "Yes"],
        adders={"Yes": 400.00},
        rules="Only available for 6\" and larger flanges.",
        excluded_products=""
    ),
    Option(
        name="Stainless Steel Tag",
        description="Stainless steel tag option",
        product_families=FAMILY_NAME,
        price=30.0,
        price_type="fixed",
        category="Mechanical",
        choices=["No", "Yes"],
        adders={"Yes": 30.00},
        rules=None,
        excluded_products=""
    )
]

def print_options(db):
    options = db.query(Option).filter(Option.product_families.like(f"%{FAMILY_NAME}%")).all()
    if not options:
        print(f"No options found for {FAMILY_NAME}.")
    else:
        print(f"Options for {FAMILY_NAME}:")
        for opt in options:
            print(f"- {opt.name}: {opt.choices} (Adders: {opt.adders})")

def seed_options(db):
    print(f"Seeding options for {FAMILY_NAME}...")
    for opt in EXAMPLE_OPTIONS:
        db.add(opt)
    db.commit()
    print("Seeding complete.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db()
        print_options(db)
        seed_options(db)
    finally:
        db.close() 