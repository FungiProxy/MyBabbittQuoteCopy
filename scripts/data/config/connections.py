"""
Connections configuration and initialization.
"""

from src.core.models.connection_option import ConnectionOption
from src.core.models.product_family import ProductFamily
from src.core.database import DatabaseService


def init_connection_options(db: DatabaseService):
    """Initialize connection options in the database."""

    # Get all product families
    product_families = db.get_all(ProductFamily)

    # Define connection types
    connection_types = [
        {
            "name": '1/2" NPT',
            "description": "1/2 inch NPT connection",
            "price": 0.00,
            "is_available": True,
        },
        {
            "name": '3/4" NPT',
            "description": "3/4 inch NPT connection",
            "price": 25.00,
            "is_available": True,
        },
        {
            "name": '1" NPT',
            "description": "1 inch NPT connection",
            "price": 35.00,
            "is_available": True,
        },
        {
            "name": '1-1/2" NPT',
            "description": "1-1/2 inch NPT connection",
            "price": 45.00,
            "is_available": True,
        },
        {
            "name": '2" NPT',
            "description": "2 inch NPT connection",
            "price": 55.00,
            "is_available": True,
        },
        {
            "name": '1/2" BSP',
            "description": "1/2 inch BSP connection",
            "price": 25.00,
            "is_available": True,
        },
        {
            "name": '3/4" BSP',
            "description": "3/4 inch BSP connection",
            "price": 35.00,
            "is_available": True,
        },
        {
            "name": '1" BSP',
            "description": "1 inch BSP connection",
            "price": 45.00,
            "is_available": True,
        },
        {
            "name": '1-1/2" BSP',
            "description": "1-1/2 inch BSP connection",
            "price": 55.00,
            "is_available": True,
        },
        {
            "name": '2" BSP',
            "description": "2 inch BSP connection",
            "price": 65.00,
            "is_available": True,
        },
        {
            "name": '1/2" Tri-Clamp',
            "description": "1/2 inch Tri-Clamp connection",
            "price": 75.00,
            "is_available": True,
        },
        {
            "name": '3/4" Tri-Clamp',
            "description": "3/4 inch Tri-Clamp connection",
            "price": 85.00,
            "is_available": True,
        },
        {
            "name": '1" Tri-Clamp',
            "description": "1 inch Tri-Clamp connection",
            "price": 95.00,
            "is_available": True,
        },
        {
            "name": '1-1/2" Tri-Clamp',
            "description": "1-1/2 inch Tri-Clamp connection",
            "price": 105.00,
            "is_available": True,
        },
        {
            "name": '2" Tri-Clamp',
            "description": "2 inch Tri-Clamp connection",
            "price": 115.00,
            "is_available": True,
        },
    ]

    # Create connection options for each product family
    for family in product_families:
        for connection in connection_types:
            connection_option = ConnectionOption(
                product_family_id=family.id,
                name=connection["name"],
                description=connection["description"],
                price=connection["price"],
                is_available=connection["is_available"],
            )
            db.add(connection_option)

    db.commit()
