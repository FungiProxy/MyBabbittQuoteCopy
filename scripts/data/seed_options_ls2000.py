import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

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
        choices=["115VAC", "24VDC"],
        adders={"24VDC": 0},
        rules="12VDC and 240VAC not available for LS2000. 24VDC is no extra charge.",
        excluded_products="",
    ),
    Option(
        name="Material",
        description="Probe material",
        product_families=FAMILY_NAME,
        price=0.0,
        price_type="fixed",
        category="Mechanical",
        choices=["S", "H", "U", "T"],
        adders={"S": 0, "H": 50, "U": 30, "T": 40},
        rules="S=316SS, H=Halar, U=UHMWPE, T=Teflon",
        excluded_products="",
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
        excluded_products="",
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
        excluded_products="",
    ),
    Option(
        name="O-Rings",
        description="O-Ring material selection",
        product_families=FAMILY_NAME,
        price=0.0,
        price_type="fixed",
        category="O-ring Material",
        choices=["Viton", "Silicon", "Buna-N", "EPDM", "PTFE", "Kalrez"],
        adders={
            "Viton": 0,
            "Silicon": 0,
            "Buna-N": 0,
            "EPDM": 0,
            "PTFE": 0,
            "Kalrez": 295,
        },
        rules=None,
        excluded_products="",
    ),
    Option(
        name="Exotic Metals",
        description="Exotic metal selection",
        product_families=FAMILY_NAME,
        price=0.0,
        price_type="fixed",
        category="Mechanical",
        choices=["Alloy 20", "Hastelloy C", "Hastelloy B", "Titanium"],
        adders={"Alloy 20": 0, "Hastelloy C": 0, "Hastelloy B": 0, "Titanium": 0},
        rules=None,
        excluded_products="",
    ),
]


def print_options(db):
    options = (
        db.query(Option).filter(Option.product_families.like(f"%{FAMILY_NAME}%")).all()
    )
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
        options = (
            db.query(Option)
            .filter(Option.product_families.like(f"%{FAMILY_NAME}%"))
            .all()
        )
        if not options:
            seed_options(db)
            print_options(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
