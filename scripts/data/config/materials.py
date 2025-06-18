"""
Materials configuration and initialization.
"""

from src.core.models.material import Material
from src.core.database import DatabaseService


def init_material_options(db: DatabaseService):
    """Initialize materials in the database."""

    # Define materials
    materials = [
        {
            "name": "316SS",
            "description": "316 Stainless Steel",
            "base_price": 0.00,
            "is_available": True,
            "price_per_foot": 45.00,
        },
        {
            "name": "Halar",
            "description": "Halar Coated",
            "base_price": 0.00,
            "is_available": True,
            "price_per_foot": 110.00,
        },
        {
            "name": "CPVC",
            "description": "Chlorinated Polyvinyl Chloride",
            "base_price": 0.00,
            "is_available": True,
            "price_per_foot": 50.00,
        },
        {
            "name": "UHMW",
            "description": "Ultra High Molecular Weight Polyethylene",
            "base_price": 0.00,
            "is_available": True,
            "price_per_foot": 45.00,
        },
        {
            "name": "Cable",
            "description": "Standard Cable",
            "base_price": 0.00,
            "is_available": True,
            "price_per_foot": 45.00,
        },
        {
            "name": "Alloy 20",
            "description": "Alloy 20",
            "base_price": 295.00,
            "is_available": True,
            "price_per_foot": 75.00,
        },
        {
            "name": "Hastelloy-C-276",
            "description": "Hastelloy C-276",
            "base_price": 495.00,
            "is_available": True,
            "price_per_foot": 125.00,
        },
        {
            "name": "Hastelloy-B",
            "description": "Hastelloy B",
            "base_price": 495.00,
            "is_available": True,
            "price_per_foot": 125.00,
        },
        {
            "name": "Titanium",
            "description": "Titanium",
            "base_price": 695.00,
            "is_available": True,
            "price_per_foot": 175.00,
        },
    ]

    # Create materials
    for material in materials:
        material_obj = Material(
            name=material["name"],
            description=material["description"],
            base_price=material["base_price"],
            is_available=material["is_available"],
            price_per_foot=material["price_per_foot"],
        )
        db.add(material_obj)

    db.commit()
