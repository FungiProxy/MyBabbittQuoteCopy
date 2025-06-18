"""
Voltage options configuration and initialization.
"""

from src.core.models.voltage_option import VoltageOption
from src.core.models.product_family import ProductFamily
from src.core.database import DatabaseService


def init_voltage_options(db: DatabaseService):
    """Initialize voltage options in the database."""

    # Get all product families
    product_families = db.get_all(ProductFamily)

    # Define voltage options
    voltage_options = [
        {
            "name": "24V DC",
            "description": "24 Volt DC power supply",
            "price": 0.00,
            "is_available": True,
        },
        {
            "name": "120V AC",
            "description": "120 Volt AC power supply",
            "price": 0.00,
            "is_available": True,
        },
        {
            "name": "240V AC",
            "description": "240 Volt AC power supply",
            "price": 25.00,
            "is_available": True,
        },
        {
            "name": "480V AC",
            "description": "480 Volt AC power supply",
            "price": 35.00,
            "is_available": True,
        },
    ]

    # Create voltage options for each product family
    for family in product_families:
        for voltage in voltage_options:
            voltage_option = VoltageOption(
                product_family_id=family.id,
                name=voltage["name"],
                description=voltage["description"],
                price=voltage["price"],
                is_available=voltage["is_available"],
            )
            db.add(voltage_option)

    db.commit()
