"""
Material options configuration.
Defines material options and pricing for all product families.
"""

from src.core.models.option import Option


def init_material_options(db):
    """Initialize material options for all product families."""
    options = [
        # Material Options for LS2000
        Option(
            name="Material",
            description="Probe material selection",
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=[
                "S",
                "H",
                "TS",
                "U",
                "T",
                "C",
                "Alloy 20",
                "Hastelloy-C-276",
                "Hastelloy-B",
                "Titanium",
            ],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "U": 20,  # UHMWPE Blind End
                "T": 60,  # Teflon Blind End
                "C": 80,  # Cable
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
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
            choices=[
                "S",
                "H",
                "TS",
                "U",
                "T",
                "C",
                "Alloy 20",
                "Hastelloy-C-276",
                "Hastelloy-B",
                "Titanium",
            ],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "U": 20,  # UHMWPE Blind End
                "T": 60,  # Teflon Blind End
                "C": 80,  # Cable
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
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
            choices=[
                "S",
                "H",
                "TS",
                "U",
                "T",
                "C",
                "CPVC",
                "Alloy 20",
                "Hastelloy-C-276",
                "Hastelloy-B",
                "Titanium",
            ],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "U": 20,  # UHMWPE Blind End
                "T": 60,  # Teflon Blind End
                "C": 80,  # Cable
                "CPVC": 400,  # CPVC Blind End
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
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
            choices=[
                "S",
                "H",
                "TS",
                "T",
                "U",
                "CPVC",
                "Alloy 20",
                "Hastelloy-C-276",
                "Hastelloy-B",
                "Titanium",
            ],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "U": 20,  # UHMWPE Blind End
                "T": 60,  # Teflon Blind End
                "C": 80,  # Cable
                "CPVC": 400,  # CPVC Blind End
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
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
            choices=[
                "H",
                "TS",
                "Alloy 20",
                "Hastelloy-C-276",
                "Hastelloy-B",
                "Titanium",
            ],
            adders={
                "H": 0,  # Halar Coated
                "TS": 0,  # Teflon Sleeve
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
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
            choices=[
                "S",
                "H",
                "TS",
                "C",
                "Alloy 20",
                "Hastelloy-C-276",
                "Hastelloy-B",
                "Titanium",
            ],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "C": 80,  # Cable
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
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
            choices=[
                "H",
                "TS",
                "Alloy 20",
                "Hastelloy-C-276",
                "Hastelloy-B",
                "Titanium",
            ],
            adders={
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
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
            choices=[
                "H",
                "TS",
                "Alloy 20",
                "Hastelloy-C-276",
                "Hastelloy-B",
                "Titanium",
            ],
            adders={
                "H": 0,  # Halar Coated
                "TS": 0,  # Teflon Sleeve
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
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
            choices=["S", "Alloy 20", "Hastelloy-C-276", "Hastelloy-B", "Titanium"],
            adders={
                "S": 0,  # 316 Stainless Steel
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
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
            choices=["S", "Alloy 20", "Hastelloy-C-276", "Hastelloy-B", "Titanium"],
            adders={
                "S": 0,  # 316 Stainless Steel
                "Alloy 20": 0,  # Exotic Metal - Manual Override
                "Hastelloy-C-276": 0,  # Exotic Metal - Manual Override
                "Hastelloy-B": 0,  # Exotic Metal - Manual Override
                "Titanium": 0,  # Exotic Metal - Manual Override
            },
            product_families="LS7500,LS8500",
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
        else:
            # Update existing option with exotic metals
            existing = (
                db.query(Option)
                .filter_by(
                    name=option.name,
                    category=option.category,
                    product_families=option.product_families,
                )
                .first()
            )
            if existing:
                existing.choices = option.choices
                existing.adders = option.adders
                existing.description = option.description
