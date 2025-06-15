"""
Standard length configurations.
Defines standard lengths for different materials.
"""

from src.core.models.standard_length import StandardLength

def init_standard_lengths(db):
    """Initialize standard lengths in the database."""
    standard_lengths = [
        StandardLength(material_code="H", length=6.0),
        StandardLength(material_code="H", length=12.0),
        StandardLength(material_code="H", length=18.0),
        StandardLength(material_code="H", length=24.0),
        StandardLength(material_code="H", length=36.0),
        StandardLength(material_code="H", length=48.0),
        StandardLength(material_code="H", length=60.0),
        StandardLength(material_code="H", length=72.0),
        StandardLength(material_code="H", length=84.0),
    ]
    db.add_all(standard_lengths)
