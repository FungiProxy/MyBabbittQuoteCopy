"""
Standard lengths configuration and initialization.
"""

from src.core.models.standard_length import StandardLength
from src.core.models.material import Material
from src.core.database import DatabaseService


def init_standard_lengths(db: DatabaseService):
    """Initialize standard lengths in the database."""

    # Get all materials
    materials = db.get_all(Material)

    # Define standard lengths for each material type
    standard_lengths = {
        "316SS": [
            2,
            4,
            6,
            8,
            10,
            12,
            14,
            16,
            18,
            20,
            24,
            30,
            36,
            42,
            48,
            60,
            72,
            84,
            96,
        ],
        "Halar": [
            2,
            4,
            6,
            8,
            10,
            12,
            14,
            16,
            18,
            20,
            24,
            30,
            36,
            42,
            48,
            60,
            72,
            84,
            96,
        ],
        "CPVC": [
            2,
            4,
            6,
            8,
            10,
            12,
            14,
            16,
            18,
            20,
            24,
            30,
            36,
            42,
            48,
            60,
            72,
            84,
            96,
        ],
        "UHMW": [
            2,
            4,
            6,
            8,
            10,
            12,
            14,
            16,
            18,
            20,
            24,
            30,
            36,
            42,
            48,
            60,
            72,
            84,
            96,
        ],
        "Cable": [
            2,
            4,
            6,
            8,
            10,
            12,
            14,
            16,
            18,
            20,
            24,
            30,
            36,
            42,
            48,
            60,
            72,
            84,
            96,
        ],
    }

    # Create standard lengths for each material
    for material in materials:
        if material.name in standard_lengths:
            for length in standard_lengths[material.name]:
                # Calculate price based on material and length
                base_price = 0.00
                if material.name == "316SS":
                    base_price = length * 45.00  # $45 per foot
                elif material.name == "Halar":
                    base_price = length * 110.00  # $110 per foot
                elif material.name == "CPVC":
                    base_price = length * 50.00  # $50 per foot
                elif material.name == "UHMW":
                    base_price = length * 45.00  # $45 per foot
                elif material.name == "Cable":
                    base_price = length * 45.00  # $45 per foot

                # Create standard length record
                standard_length = StandardLength(
                    material_id=material.id,
                    length=length,
                    price=base_price,
                    is_available=True,
                )
                db.add(standard_length)

    db.commit()
