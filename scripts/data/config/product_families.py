"""
Product families configuration and initialization.
"""

from src.core.models.product_family import ProductFamily
from src.core.database import DatabaseService


def init_product_families(db: DatabaseService):
    """Initialize product families in the database."""

    # Define product families
    product_families = [
        {
            "name": "LS2000",
            "description": "Level Switch 2000 Series",
            "base_price": 595.00,
            "is_available": True,
        },
        {
            "name": "LS2100",
            "description": "Level Switch 2100 Series",
            "base_price": 695.00,
            "is_available": True,
        },
        {
            "name": "LS6000",
            "description": "Level Switch 6000 Series",
            "base_price": 795.00,
            "is_available": True,
        },
        {
            "name": "LS7000",
            "description": "Level Switch 7000 Series",
            "base_price": 895.00,
            "is_available": True,
        },
        {
            "name": "LS7000/2",
            "description": "Level Switch 7000/2 Series",
            "base_price": 995.00,
            "is_available": True,
        },
        {
            "name": "LS8000",
            "description": "Level Switch 8000 Series",
            "base_price": 1095.00,
            "is_available": True,
        },
        {
            "name": "LS8000/2",
            "description": "Level Switch 8000/2 Series",
            "base_price": 1195.00,
            "is_available": True,
        },
        {
            "name": "LT9000",
            "description": "Level Transmitter 9000 Series",
            "base_price": 1295.00,
            "is_available": True,
        },
        {
            "name": "FS10000",
            "description": "Flow Switch 10000 Series",
            "base_price": 1395.00,
            "is_available": True,
        },
        {
            "name": "LS7500",
            "description": "Level Switch 7500 Series",
            "base_price": 1495.00,
            "is_available": True,
        },
        {
            "name": "LS8500",
            "description": "Level Switch 8500 Series",
            "base_price": 1595.00,
            "is_available": True,
        },
    ]

    # Create product families
    for family in product_families:
        product_family = ProductFamily(
            name=family["name"],
            description=family["description"],
            base_price=family["base_price"],
            is_available=family["is_available"],
        )
        db.add(product_family)

    db.commit()
