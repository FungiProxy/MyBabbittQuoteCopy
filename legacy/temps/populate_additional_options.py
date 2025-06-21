"""
Script to populate the Option table with additional options (add-ons/features) not already present.
Run this script to ensure all additional options are available for quoting.
"""

import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.database import SessionLocal
from src.core.models import Option

# List of additional options to add
ADDITIONAL_OPTIONS = [
    # name, description, price, price_type, category, product_families
    (
        "Teflon Insulator",
        "Teflon insulator instead of UHMWPE/Delrin",
        40.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Flanged Mounting",
        "Flange connection for mounting",
        None,
        "fixed",
        "additional",
        None,
    ),
    (
        "Tri-Clamp Mounting",
        "Tri-Clamp connection for mounting",
        None,
        "fixed",
        "additional",
        None,
    ),
    (
        "Extra Static Protection",
        "Adds static protection",
        30.0,
        "fixed",
        "additional",
        None,
    ),
    ("Cable Probe", "Cable probe option", 80.0, "fixed", "additional", None),
    ("Bent Probe", "Bent probe option", 50.0, "fixed", "additional", None),
    ("Stainless Steel Tag", "Stainless steel tag", 30.0, "fixed", "additional", None),
    (
        '3/4" Diameter Probe',
        "3/4 inch diameter probe",
        175.0,
        "per_foot",
        "additional",
        None,
    ),
    (
        "CPVC Blind End Probe w/ Integrated Nipple",
        "CPVC blind end probe with integrated nipple (plus $50 per additional inch)",
        400.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "22 AWG, Twisted Shielded Pair",
        "Twisted shielded pair cable (per foot)",
        0.70,
        "per_foot",
        "additional",
        None,
    ),
    (
        "NEMA 4 Metal Enclosure for Receiver",
        "NEMA 4 metal enclosure for receiver",
        245.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Explosion Proof Housing/Enclosure for Receiver",
        "Explosion proof housing/enclosure for receiver",
        590.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Big Housing for High Vibration Applications",
        "Big housing for high vibration applications",
        None,
        "fixed",
        "additional",
        None,
    ),
    (
        "Additional Coaxial Cable",
        "Additional coaxial cable (per foot)",
        6.0,
        "per_foot",
        "additional",
        None,
    ),
    (
        "Ultrasonic Sanitary / High Pressure",
        "Ultrasonic sanitary or high pressure option",
        580.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Ultrasonic High Temperature w/ Teflon Transducer",
        "Ultrasonic high temperature with Teflon transducer",
        556.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Stainless Steel Enclosure (Ultrasonic)",
        "Stainless steel enclosure for ultrasonic transmitter",
        450.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Aluminum Enclosure (Ultrasonic)",
        "Aluminum enclosure for ultrasonic transmitter",
        100.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Sanitary Teflon Antenna (Radar)",
        "Sanitary Teflon antenna for radar transmitter",
        665.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Teflon De-Coupler (Radar)",
        "Teflon de-coupler for radar transmitter",
        350.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "High Pressure Teflon Antenna (Radar)",
        "High pressure Teflon antenna for radar transmitter",
        705.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "SS Housing & Process Connection (Radar)",
        "Stainless steel housing and process connection for radar transmitter",
        695.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Extended Teflon Antenna (Radar)",
        "Extended Teflon antenna for radar transmitter",
        510.0,
        "fixed",
        "additional",
        None,
    ),
    (
        '6" Antenna Extension (Radar)',
        "6 inch antenna extension for radar transmitter",
        310.0,
        "fixed",
        "additional",
        None,
    ),
    (
        '8" Antenna Extension (Radar)',
        "8 inch antenna extension for radar transmitter",
        405.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Aluminum Explosion Proof Enclosure (Radar)",
        "Aluminum explosion proof enclosure for radar transmitter",
        880.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "316 SS Explosion Proof Enclosure (Radar)",
        "316 stainless steel explosion proof enclosure for radar transmitter",
        1385.0,
        "fixed",
        "additional",
        None,
    ),
    (
        '6" 316SS Horn Antenna (Radar)',
        "6 inch 316SS horn antenna for radar transmitter",
        625.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "3 Relay Controller with Display (Radar)",
        "3 relay controller with display for radar transmitter",
        880.0,
        "fixed",
        "additional",
        None,
    ),
    (
        "Loop Powered NEMA 4X LED Display (Radar)",
        "Loop powered NEMA 4X LED display for radar transmitter",
        556.0,
        "fixed",
        "additional",
        None,
    ),
    ('6" Insulator', "6 inch insulator", 150.0, "fixed", "additional", None),
    ('8" Insulator', "8 inch insulator", 200.0, "fixed", "additional", None),
    ('10" Insulator', "10 inch insulator", 250.0, "fixed", "additional", None),
    ('12" Insulator', "12 inch insulator", 300.0, "fixed", "additional", None),
    ("PEEK Insulator", "PEEK insulator", 340.0, "fixed", "additional", None),
    (
        "Ceramic Insulator",
        "Ceramic insulator (1400F - dry materials only)",
        470.0,
        "fixed",
        "additional",
        None,
    ),
]


def main():
    db = SessionLocal()
    added = 0
    for (
        name,
        description,
        price,
        price_type,
        category,
        product_families,
    ) in ADDITIONAL_OPTIONS:
        # Check if option already exists by name (case-insensitive)
        exists = db.query(Option).filter(Option.name.ilike(name)).first()
        if not exists:
            option = Option(
                name=name,
                description=description,
                price=price if price is not None else 0.0,
                price_type=price_type,
                category=category,
                product_families=product_families or "",
            )
            db.add(option)
            added += 1
    db.commit()
    print(f"Added {added} additional options.")
    if added == 0:
        print("No new options were added (all already present).")


if __name__ == "__main__":
    main()
