"""
Database initialization script for business configuration data.
This includes essential business rules, materials, standard lengths, and pricing configurations.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal, init_db
from src.core.models.material import StandardLength
from src.core.models.product_variant import ProductFamily
from src.core.models.option import Option


def init_business_config():
    """Initialize the database with essential business configuration data."""
    # Initialize database
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Add product families
        product_families = [
            ProductFamily(
                name="LS2000",
                description="LS2000 Level Switch",
                category="Point Level Switch",
            ),
            ProductFamily(
                name="LS2100",
                description="LS2100 Level Switch",
                category="Point Level Switch",
            ),
            ProductFamily(
                name="LS6000",
                description="LS6000 Level Switch",
                category="Point Level Switch",
            ),
            ProductFamily(
                name="LS7000",
                description="LS7000 Level Switch",
                category="Point Level Switch",
            ),
            ProductFamily(
                name="LS7000/2",
                description="LS7000/2 Level Switch",
                category="Multi-Point Level Switch",
            ),
            ProductFamily(
                name="LS8000",
                description="LS8000 Level Switch",
                category="Point Level Switch",
            ),
            ProductFamily(
                name="LS8000/2",
                description="LS8000/2 Level Switch",
                category="Multi-Point Level Switch",
            ),
            ProductFamily(
                name="LT9000",
                description="LT9000 Level Switch",
                category="Continuous Level Transmitter",
            ),
            ProductFamily(
                name="FS10000",
                description="FS10000 Level Switch",
                category="Flow Switch",
            ),
            ProductFamily(
                name="LS7500",
                description="LS7500 Integral Flange Sensor",
                category="Presence/Absence Switch",
            ),
            ProductFamily(
                name="LS8500",
                description="LS8500 Remote Mount Flange Sensor",
                category="Presence/Absence Switch",
            ),
        ]
        db.add_all(product_families)

        # Add product options
        options = [
            # Material Options for LS2000
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["S", "H", "TS", "U", "T", "C"],
                adders={
                    "S": 0,  # 316 Stainless Steel
                    "H": 110,  # Halar Coated
                    "TS": 110,  # Teflon Sleeve
                    "U": 20,  # UHMWPE Blind End
                    "T": 60,  # Teflon Blind End
                    "C": 80,  # Cable
                },
                product_families="LS2000",
            ),
            # Material Options for LS2100
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["S", "H", "TS", "U", "T", "C"],
                adders={
                    "S": 0,  # 316 Stainless Steel
                    "H": 110,  # Halar Coated
                    "TS": 110,  # Teflon Sleeve
                    "U": 20,  # UHMWPE Blind End
                    "T": 60,  # Teflon Blind End
                    "C": 80,  # Cable
                },
                product_families="LS2100",
            ),
            # Material Options for LS6000
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["S", "H", "TS", "U", "T", "C", "CPVC"],
                adders={
                    "S": 0,  # 316 Stainless Steel
                    "H": 110,  # Halar Coated
                    "TS": 110,  # Teflon Sleeve
                    "U": 20,  # UHMWPE Blind End
                    "T": 60,  # Teflon Blind End
                    "C": 80,  # Cable
                    "CPVC": 400,  # CPVC Blind End
                },
                product_families="LS6000",
            ),
            # Material Options for LS7000
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["S", "H", "TS", "T", "U", "CPVC"],
                adders={
                    "S": 0,  # 316 Stainless Steel
                    "H": 110,  # Halar Coated
                    "TS": 110,  # Teflon Sleeve
                    "U": 20,  # UHMWPE Blind End
                    "T": 60,  # Teflon Blind End
                    "C": 80,  # Cable
                    "CPVC": 400,  # CPVC Blind End
                },
                product_families="LS7000",
            ),
            # Material Options for LS7000/2
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["H", "TS"],
                adders={
                    "H": 0,  # Halar Coated
                    "TS": 0,  # Teflon Sleeve
                },
                product_families="LS7000/2",
            ),
            # Material Options for LS8000
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["S", "H", "TS", "C"],
                adders={
                    "S": 0,  # 316 Stainless Steel
                    "H": 110,  # Halar Coated
                    "TS": 110,  # Teflon Sleeve
                    "C": 80,  # Cable
                },
                product_families="LS8000",
            ),
            # Material Options for LS8000/2
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["H", "TS"],
                adders={
                    "H": 110,  # Halar Coated
                    "TS": 110,  # Teflon Sleeve
                },
                product_families="LS8000/2",
            ),
            # Material Options for LT9000
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["H", "TS"],
                adders={
                    "H": 0,  # Halar Coated
                    "TS": 0,  # Teflon Sleeve
                },
                product_families="LT9000",
            ),
            # Material Options for FS10000
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["S"],
                adders={
                    "S": 0,  # 316 Stainless Steel
                },
                product_families="FS10000",
            ),
            # Material Options for Presence/Absence Switches
            Option(
                name="Material",
                description="Probe material selection",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["S"],
                adders={
                    "S": 0,  # 316 Stainless Steel
                },
                product_families="LS7500,LS8500",
            ),
            # O-Ring Materials
            Option(
                name="O-Rings",
                description="O-Ring material selection",
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
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            # Exotic Metals
            Option(
                name="Exotic Metal",
                description="Exotic metal material selection",
                price=0.0,
                price_type="fixed",
                category="Exotic Metal",
                choices=[
                    "None",
                    "Alloy 20",
                    "Hastelloy-C-276",
                    "Hastelloy-B",
                    "Titanium",
                ],
                adders={
                    "None": 0,
                    "Alloy 20": 0,
                    "Hastelloy-C-276": 0,
                    "Hastelloy-B": 0,
                    "Titanium": 0,
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            # Voltage Options for LS2000,
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["115VAC", "24VDC"],
                adders={
                    "115VAC": 0,
                    "24VDC": 0,
                },
                product_families="LS2000",
            ),
            # Voltage Options for LS2100
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["24VDC"],
                adders={
                    "24VDC": 0,
                },
                product_families="LS2100",
            ),
            # Voltage Options for LS6000
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["115VAC", "230VAC", "12VDC", "24VDC"],
                adders={
                    "115VAC": 0,
                    "230VAC": 0,
                    "12VDC": 0,
                    "24VDC": 0,
                },
                product_families="LS6000",
            ),
            # Voltage Options for LS7000
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["115VAC", "230VAC", "12VDC", "24VDC"],
                adders={
                    "115VAC": 0,
                    "230VAC": 0,
                    "12VDC": 0,
                    "24VDC": 0,
                },
                product_families="LS7000",
            ),
            # Voltage Options for LS7000/2
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["115VAC", "230VAC", "12VDC", "24VDC"],
                adders={
                    "115VAC": 0,
                    "230VAC": 0,
                    "12VDC": 0,
                    "24VDC": 0,
                },
                product_families="LS7000/2",
            ),
            # Voltage Options for LS8000
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["115VAC", "230VAC", "12VDC", "24VDC"],
                adders={
                    "115VAC": 0,
                    "230VAC": 0,
                    "12VDC": 0,
                    "24VDC": 0,
                },
                product_families="LS8000",
            ),
            # Voltage Options for LS8000/2
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["115VAC", "230VAC", "12VDC", "24VDC"],
                adders={
                    "115VAC": 0,
                    "230VAC": 0,
                    "12VDC": 0,
                    "24VDC": 0,
                },
                product_families="LS8000/2",
            ),
            # Voltage Options for LT9000
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["115VAC", "230VAC", "24VDC"],
                adders={
                    "115VAC": 0,
                    "230VAC": 0,
                    "24VDC": 0,
                },
                product_families="LT9000",
            ),
            # Voltage Options for FS10000
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["115VAC", "230VAC"],
                adders={
                    "115VAC": 0,
                    "230VAC": 0,
                },
                product_families="FS10000",
            ),
            # Voltage Options for LS7500, LS8500
            Option(
                name="Voltage",
                description="Supply voltage selection",
                price=0.0,
                price_type="fixed",
                category="Electrical",
                choices=["115VAC", "230VAC", "12VDC", "24VDC"],
                adders={
                    "115VAC": 0,
                    "230VAC": 0,
                    "12VDC": 0,
                    "24VDC": 0,
                },
                product_families="LS7500, LS8500",
            ),
            # Connection Types
            Option(
                name="Connection Type",
                description="Primary connection type selection",
                price=0.0,
                price_type="fixed",
                category="Mechanical",
                choices=["NPT", "Flange", "Tri-clamp"],
                adders={
                    "NPT": 0,  # Standard
                    "Flange": 0,  # Base price for flange
                    "Tri-clamp": 0,  # Base price for tri-clamp
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            # NPT Sizes for LS2000, LS2100
            Option(
                name="NPT Size",
                description="NPT connection size selection",
                price=0.0,
                price_type="fixed",
                category="Mechanical",
                choices=['3/4"'],
                adders={
                    '3/4"': 0,
                },
                product_families="LS2000,LS2100",
            ),
            # NPT Sizes for LS6000, LS7000
            Option(
                name="NPT Size",
                description="NPT connection size selection",
                price=0.0,
                price_type="fixed",
                category="Mechanical",
                choices=['1"', '3/4"'],
                adders={
                    '1"': 0,
                    '3/4"': 0,
                },
                product_families="LS6000,LS7000",
            ),
            # Flange Types
            Option(
                name="Flange Type",
                description="Flange type selection",
                price=0.0,
                price_type="fixed",
                category="Mechanical",
                choices=["150#", "300#"],
                adders={
                    "150#": 0,
                    "300#": 0,
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            # Flange Sizes
            Option(
                name="Flange Size",
                description="Flange size selection",
                price=0.0,
                price_type="fixed",
                category="Mechanical",
                choices=['1"', '1-1/2"', '2"', '3"', '4"'],
                adders={
                    '1"': 0,
                    '1-1/2"': 0,
                    '2"': 0,
                    '3"': 0,
                    '4"': 0,
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            # Tri-clamp
            Option(
                name="Tri-clamp",
                description="Tri-clamp selection",
                price=0.0,
                price_type="fixed",
                category="Mechanical",
                choices=[
                    '1-1/2" Tri-clamp Process Connection',
                    '1-1/2" Tri-clamp Spud',
                    '2" Tri-clamp Process Connection',
                    '2" Tri-clamp Spud',
                ],
                adders={
                    '1-1/2" Tri-clamp Process Connection': 280.0,
                    '1-1/2" Tri-clamp Spud': 170.0,
                    '2" Tri-clamp Process Connection': 330.0,
                    '2" Tri-clamp Spud': 220.0,
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            # Insulator Options
            Option(
                name="Insulator",
                description="Insulator material selection",
                price=0.0,
                price_type="fixed",
                category="Mechanical",
                choices=["Delrin", "Teflon", "PEEK", "Ceramic"],
                adders={
                    "Delrin": 0,  # Standard for SS probes
                    "Teflon": 40,  # Standard for Halar and Teflon Sleeve
                    "PEEK": 340,  # High temperature option
                    "Ceramic": 470,  # High temperature option for dry materials
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            # Probe Length Pricing
            Option(
                name="Probe Length",
                description="Probe length pricing rules",
                price=0.0,
                price_type="per_unit",
                category="Pricing",
                choices=["Standard", "Non-Standard"],
                adders={
                    "Standard": 0,  # No adder for standard lengths
                    "Non-Standard": 300,  # $300 adder for non-standard lengths
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            # Material-specific Length Adders
            Option(
                name="Length Adder",
                description="Per-foot length adder by material",
                price=0.0,
                price_type="per_unit",
                category="Pricing",
                choices=["S", "H", "CPVC"],
                adders={
                    "S": 45,  # $45 per foot for 316SS
                    "H": 110,  # $110 per foot for Halar
                    "CPVC": 50,  # $50 per inch for CPVC
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            # Miscellaneous Options
            Option(
                name="Extra Static Protection",
                description="Additional static protection for plastic pellets and resins",
                price=30.0,
                price_type="fixed",
                category="Electrical",
                choices=["Yes", "No"],
                adders={
                    "Yes": 30,
                    "No": 0,
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            Option(
                name="Bent Probe",
                description="Bent probe configuration",
                price=50.0,
                price_type="fixed",
                category="Mechanical",
                choices=["Yes", "No"],
                adders={
                    "Yes": 50,
                    "No": 0,
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            Option(
                name="Stainless Steel Tag",
                description="Stainless steel identification tag",
                price=30.0,
                price_type="fixed",
                category="Mechanical",
                choices=["Yes", "No"],
                adders={
                    "Yes": 30,
                    "No": 0,
                },
                product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
            ),
            Option(
                name='3/4" Diameter Probe',
                description='3/4" diameter probe x 10"',
                price=175.0,
                price_type="fixed",
                category="Mechanical",
                choices=["Yes", "No"],
                adders={
                    "Yes": 175,
                    "No": 0,
                },
                product_families="LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000",
            ),
            Option(
                name="Twisted Shielded Pair",
                description="22 AWG, twisted shielded pair",
                price=0.0,
                price_type="per_unit",
                category="Electrical",
                choices=["Yes", "No"],
                adders={
                    "Yes": 0.70,  # $0.70 per foot
                    "No": 0,
                },
                product_families="LS8000,LS8000/2",
            ),
            Option(
                name="NEMA 4 Enclosure",
                description='8" x 6" x 3.5" NEMA 4 metal enclosure for receiver',
                price=245.0,
                price_type="fixed",
                category="Mechanical",
                choices=["Yes", "No"],
                adders={
                    "Yes": 245,
                    "No": 0,
                },
                product_families="LS8000,LS8000/2",
            ),
            Option(
                name="Additional Coaxial Cable",
                description="Additional coaxial cable",
                price=0.0,
                price_type="per_unit",
                category="Electrical",
                choices=["Yes", "No"],
                adders={
                    "Yes": 6.0,  # $6 per foot
                    "No": 0,
                },
                product_families="FS10000",
            ),
            Option(
                name="GRK Exp Proof Enclosure",
                description="GRK explosion proof enclosure for receiver",
                price=1030.0,
                price_type="fixed",
                category="Mechanical",
                choices=["Yes", "No"],
                adders={
                    "Yes": 1030,
                    "No": 0,
                },
                product_families="LS8000,LS8000/2,FS10000",
            ),
        ]

        # Add all options
        for option in options:
            # Check if option already exists
            exists = (
                db.query(Option)
                .filter_by(name=option.name, category=option.category)
                .first()
            )
            if not exists:
                db.add(option)

        # Add standard lengths for H material
        standard_lengths = [
            StandardLength(material_code="H", length=6.0),
            StandardLength(material_code="H", length=12.0),
            StandardLength(material_code="H", length=18.0),
            StandardLength(material_code="H", length=24.0),
            StandardLength(material_code="H", length=36.0),
            StandardLength(material_code="H", length=48.0),
            StandardLength(material_code="H", length=60.0),
            StandardLength(material_code="H", length=72.0),
            StandardLength(material_code="H", length=84.0),
        ]
        db.add_all(standard_lengths)

        # Commit all changes
        db.commit()
        print("Business configuration data initialized successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error initializing business configuration data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_business_config()
