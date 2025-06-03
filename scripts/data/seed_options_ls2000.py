import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal, init_db
from src.core.models.option import Option

FAMILY_NAME = "LS2000"

EXAMPLE_OPTIONS = [
    Option(
        name="Voltage",
        description="Supply voltage for the product",
        product_families=FAMILY_NAME,
        price=0.0,
        price_type="fixed",
        category="Electrical",
        choices=["24VDC", "115VAC", "230VAC"],
        adders={"24VDC": 0, "115VAC": 0, "230VAC": 25},
        rules=None,
        excluded_products=""
    ),
    Option(
        name="Material",
        description="Probe material",
        product_families=FAMILY_NAME,
        price=0.0,
        price_type="fixed",
        category="Mechanical",
        choices=["316SS", "Halar", "UHMWPE", "Teflon"],
        adders={"316SS": 0, "Halar": 50, "UHMWPE": 30, "Teflon": 40},
        rules=None,
        excluded_products=""
    ),
    Option(
        name="Probe Length",
        description="Length of the probe in inches",
        product_families=FAMILY_NAME,
        price=0.0,
        price_type="per_inch",
        category="Mechanical",
        choices=["10", "20", "30", "40"],
        adders={"10": 0, "20": 20, "30": 40, "40": 60},
        rules=None,
        excluded_products=""
    ),
    Option(
        name="Housing",
        description="Type of housing",
        product_families=FAMILY_NAME,
        price=0.0,
        price_type="fixed",
        category="Enclosure",
        choices=["Standard", "Explosion-Proof", "Stainless Steel"],
        adders={"Standard": 0, "Explosion-Proof": 100, "Stainless Steel": 200},
        rules=None,
        excluded_products=""
    ),
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

def main():
    init_db()
    db = SessionLocal()
    try:
        print_options(db)
        options = db.query(Option).filter(Option.product_families.like(f"%{FAMILY_NAME}%")).all()
        if not options:
            seed_options(db)
            print_options(db)
    finally:
        db.close()

if __name__ == "__main__":
    main() 