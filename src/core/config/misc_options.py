"""
Miscellaneous options configuration.
Defines various additional options like warranty, shipping, etc.
"""

from src.core.models.option import Option


def init_misc_options(db):
    """Initialize miscellaneous options in the database."""
    options = [
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
            choices=["None", "Alloy 20", "Hastelloy-C-276", "Hastelloy-B", "Titanium"],
            adders={
                "None": 0,
                "Alloy 20": 0,
                "Hastelloy-C-276": 0,
                "Hastelloy-B": 0,
                "Titanium": 0,
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
            choices=["S", "H", "CPVC", "U", "C"],
            adders={
                "S": 45,  # $45 per foot for 316SS
                "H": 110,  # $110 per foot for Halar
                "CPVC": 50,  # $50 per inch for CPVC
                "U": 45,  # $45 per inch for UHMW
                "C": 45,  # $45 per foot for cable
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
            product_families="LS2000",
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
            product_families="LS2000,LS2100,LS6000,LS7000,LS8000,",
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
            product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,",
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
            product_families="LS6000,LS7000",
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
        # LS7000 Enclosure
        Option(
            name="LS7000 Enclosure",
            description="Enclosure selection for LS7000",
            price=0.0,
            price_type="fixed",
            category="Mechanical",
            choices=["Standard", "Stainless Steel NEMA 4X"],
            adders={"Standard": 0, "Stainless Steel NEMA 4X": 285.0},
            product_families="LS7000",
        ),
        # LS8000 Enclosure
        Option(
            name="LS8000 Enclosure",
            description="Enclosure selection for LS8000",
            price=0.0,
            price_type="fixed",
            category="Mechanical",
            choices=["Standard", "NEMA 4 Metal 8x6x3.5", "GRE Exp Proof"],
            adders={
                "Standard": 0,
                "NEMA 4 Metal 8x6x3.5": 245.0,
                "GRE Exp Proof": 590.0,
            },
            product_families="LS8000",
        ),
        # LS8000/2 Enclosure
        Option(
            name="LS8000/2 Enclosure",
            description="Enclosure selection for LS8000/2",
            price=0.0,
            price_type="fixed",
            category="Mechanical",
            choices=["Standard", "NEMA 4 Metal 10x8x4", "GRK Exp Proof"],
            adders={
                "Standard": 0,
                "NEMA 4 Metal 10x8x4": 420.0,
                "GRK Exp Proof": 1030.0,
            },
            product_families="LS8000/2",
        ),
        # FS10000 Enclosure
        Option(
            name="FS10000 Enclosure",
            description="Enclosure selection for FS10000",
            price=0.0,
            price_type="fixed",
            category="Mechanical",
            choices=["Standard", "GRK Exp Proof"],
            adders={"Standard": 0, "GRK Exp Proof": 1030.0},
            product_families="FS10000",
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
    ]

    for option in options:
        exists = (
            db.query(Option)
            .filter_by(name=option.name, category=option.category)
            .first()
        )
        if not exists:
            db.add(option)
