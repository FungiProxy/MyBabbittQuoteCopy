"""
Product family configurations.
Defines all product families and their basic properties.
"""

from src.core.models.product_family import ProductFamily


def init_product_families(db):
    """Initialize product families in the database."""
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
