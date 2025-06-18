"""
Miscellaneous options configuration and initialization.
"""

from src.core.models.option import Option
from src.core.models.product_family import ProductFamily
from src.core.models.standard_length import StandardLength
from src.core.database import DatabaseService


def init_misc_options(db: DatabaseService):
    """Initialize miscellaneous options in the database."""

    # Get all product families
    product_families = db.get_all(ProductFamily)

    # Define housing types
    housing_types = [
        {
            "name": "Standard Housing",
            "description": "Standard housing configuration",
            "price": 0.00,
            "is_available": True,
        },
        {
            "name": "Explosion Proof",
            "description": "Explosion proof housing configuration",
            "price": 150.00,
            "is_available": True,
        },
        {
            "name": "Weather Resistant",
            "description": "Weather resistant housing configuration",
            "price": 75.00,
            "is_available": True,
        },
    ]

    # Define cable lengths
    cable_lengths = [
        {
            "name": "3ft Cable",
            "description": "3 foot cable length",
            "price": 25.00,
            "is_available": True,
        },
        {
            "name": "6ft Cable",
            "description": "6 foot cable length",
            "price": 35.00,
            "is_available": True,
        },
        {
            "name": "10ft Cable",
            "description": "10 foot cable length",
            "price": 45.00,
            "is_available": True,
        },
        {
            "name": "15ft Cable",
            "description": "15 foot cable length",
            "price": 55.00,
            "is_available": True,
        },
        {
            "name": "20ft Cable",
            "description": "20 foot cable length",
            "price": 65.00,
            "is_available": True,
        },
    ]

    # Define standard probe lengths
    standard_probe_lengths = [
        {
            "name": "2in Probe",
            "description": "2 inch probe length",
            "price": 0.00,
            "is_available": True,
        },
        {
            "name": "4in Probe",
            "description": "4 inch probe length",
            "price": 25.00,
            "is_available": True,
        },
        {
            "name": "6in Probe",
            "description": "6 inch probe length",
            "price": 35.00,
            "is_available": True,
        },
        {
            "name": "8in Probe",
            "description": "8 inch probe length",
            "price": 45.00,
            "is_available": True,
        },
        {
            "name": "12in Probe",
            "description": "12 inch probe length",
            "price": 65.00,
            "is_available": True,
        },
    ]

    # Define warranty options
    warranty_options = [
        {
            "name": "Standard Warranty",
            "description": "1 year standard warranty",
            "price": 0.00,
            "is_available": True,
        },
        {
            "name": "Extended Warranty",
            "description": "3 year extended warranty",
            "price": 100.00,
            "is_available": True,
        },
        {
            "name": "Premium Warranty",
            "description": "5 year premium warranty",
            "price": 200.00,
            "is_available": True,
        },
    ]

    # Define shipping options
    shipping_options = [
        {
            "name": "Standard Shipping",
            "description": "5-7 business days",
            "price": 15.00,
            "is_available": True,
        },
        {
            "name": "Express Shipping",
            "description": "2-3 business days",
            "price": 35.00,
            "is_available": True,
        },
        {
            "name": "Overnight Shipping",
            "description": "Next business day",
            "price": 75.00,
            "is_available": True,
        },
    ]

    # Create options for each product family
    for family in product_families:
        # Add housing types
        for housing in housing_types:
            option = Option(
                product_family_id=family.id,
                name=housing["name"],
                description=housing["description"],
                price=housing["price"],
                is_available=housing["is_available"],
                option_type="housing_type",
            )
            db.add(option)

        # Add cable lengths
        for cable in cable_lengths:
            option = Option(
                product_family_id=family.id,
                name=cable["name"],
                description=cable["description"],
                price=cable["price"],
                is_available=cable["is_available"],
                option_type="cable_length",
            )
            db.add(option)

        # Add standard probe lengths
        for probe in standard_probe_lengths:
            option = Option(
                product_family_id=family.id,
                name=probe["name"],
                description=probe["description"],
                price=probe["price"],
                is_available=probe["is_available"],
                option_type="probe_length",
            )
            db.add(option)

        # Add warranty options
        for warranty in warranty_options:
            option = Option(
                product_family_id=family.id,
                name=warranty["name"],
                description=warranty["description"],
                price=warranty["price"],
                is_available=warranty["is_available"],
                option_type="warranty",
            )
            db.add(option)

        # Add shipping options
        for shipping in shipping_options:
            option = Option(
                product_family_id=family.id,
                name=shipping["name"],
                description=shipping["description"],
                price=shipping["price"],
                is_available=shipping["is_available"],
                option_type="shipping",
            )
            db.add(option)

    db.commit()
