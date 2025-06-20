"""
Voltage options configuration.
Defines voltage options for all product families.
"""

from src.core.models.option import Option


def init_voltage_options(db):
    """Initialize voltage options for all product families."""
    options = [
        # Voltage Options for LS2000
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
