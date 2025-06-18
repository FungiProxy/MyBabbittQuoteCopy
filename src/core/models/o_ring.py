"""
O-Ring configuration for all product families.

This module defines O-Ring types, their materials, and application notes
for all product families. It consolidates all O-Ring-related configurations into
a single source of truth.

Supports:
- O-Ring types and materials
- Temperature and chemical resistance ratings
- Application notes and restrictions
- Material-specific configurations
"""

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlalchemy import Column, String, Float, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel


class O_Ring(BaseModel):
    """
    SQLAlchemy model representing O-Ring configurations.

    This model stores all O-Ring-related configurations including types,
    materials, temperature limits, and application notes. It serves as a single
    source of truth for O-Ring data across all product families.

    Attributes:
        id (int): Primary key
        code (str): Unique O-Ring code (e.g., "VIT", "EPD", "NIT")
        name (str): Full O-Ring name (e.g., "Viton", "EPDM", "Nitrile")
        description (str): Detailed description
        temperature_limit (float): Maximum temperature in Fahrenheit
        price (float): Standard price adjustment for this O-Ring type
        material_dependencies (List[str]): List of compatible material codes
        product_families (List[str]): List of compatible product families
        application_notes (str): Important notes about usage and restrictions
        is_active (bool): Whether this O-Ring type is currently active
        sort_order (int): Display order in UI
        validation_rules (Dict): Additional validation rules
        properties (Dict): O-Ring-specific properties
        restrictions (Dict): Usage restrictions and limitations
        chemical_resistance (Dict): Chemical resistance ratings
    """

    __tablename__ = "o_rings"

    # Core fields
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    temperature_limit = Column(Float, nullable=False)
    price = Column(Float, default=0.0)  # Standard price adjustment
    material_dependencies = Column(JSON, nullable=True)
    product_families = Column(JSON, nullable=True)
    application_notes = Column(String(500))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # Additional properties
    validation_rules = Column(JSON, nullable=True)
    properties = Column(JSON, nullable=True)
    restrictions = Column(JSON, nullable=True)
    chemical_resistance = Column(JSON, nullable=True)

    @validator("code")
    def validate_code(cls, v):
        """Validate O-Ring code format."""
        if not v or len(v) > 10:
            raise ValueError("O-Ring code must be between 1 and 10 characters")
        return v.upper()

    @validator("temperature_limit")
    def validate_temperature(cls, v):
        """Ensure temperature limit is positive and reasonable."""
        if v <= 0 or v > 500:  # 500°F as maximum reasonable limit for O-Rings
            raise ValueError("Temperature limit must be between 0 and 500°F")
        return v

    @validator("price")
    def validate_price(cls, v):
        """Ensure price is non-negative."""
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    def is_compatible_with_material(self, material_code: str) -> bool:
        """Check if this O-Ring is compatible with a given material."""
        if not self.material_dependencies:
            return True
        return material_code in self.material_dependencies

    def is_compatible_with_product_family(self, family_code: str) -> bool:
        """Check if this O-Ring is compatible with a given product family."""
        if not self.product_families:
            return True
        return family_code in self.product_families

    def get_chemical_resistance(self, chemical: str) -> Optional[str]:
        """Get the chemical resistance rating for a specific chemical."""
        if not self.chemical_resistance:
            return None
        return self.chemical_resistance.get(chemical)

    def __repr__(self):
        """Return a string representation of the O-Ring."""
        return f"<O_Ring(code='{self.code}', name='{self.name}')>"


def init_o_ring_options(db):
    """Initialize all O-Ring-related options in the database."""
    o_rings = [
        O_Ring(
            code="VIT",
            name="Viton",
            description="Standard Viton O-Ring",
            temperature_limit=400.0,
            price=25.0,  # Standard price adjustment for Viton
            material_dependencies=["S", "H", "TS"],
            product_families=[
                "LS2000",
                "LS2100",
                "LS6000",
                "LS7000",
                "LS7000/2",
                "LS8000",
                "LS8000/2",
                "LT9000",
                "FS10000",
            ],
            application_notes="Standard O-Ring material. Good chemical resistance and temperature range.",
            is_active=True,
            sort_order=1,
            chemical_resistance={
                "acids": "Good",
                "alkalis": "Good",
                "hydrocarbons": "Excellent",
                "water": "Good",
            },
        ),
        O_Ring(
            code="EPD",
            name="EPDM",
            description="EPDM O-Ring",
            temperature_limit=300.0,
            price=15.0,  # Standard price adjustment for EPDM
            material_dependencies=["S", "H", "TS"],
            product_families=[
                "LS2000",
                "LS2100",
                "LS6000",
                "LS7000",
                "LS7000/2",
                "LS8000",
                "LS8000/2",
                "LT9000",
                "FS10000",
            ],
            application_notes="Good for water and steam applications. Not recommended for petroleum products.",
            is_active=True,
            sort_order=2,
            chemical_resistance={
                "acids": "Good",
                "alkalis": "Excellent",
                "hydrocarbons": "Poor",
                "water": "Excellent",
            },
        ),
        O_Ring(
            code="NIT",
            name="Nitrile",
            description="Nitrile O-Ring",
            temperature_limit=250.0,
            price=10.0,  # Standard price adjustment for Nitrile
            material_dependencies=["S", "H", "TS"],
            product_families=[
                "LS2000",
                "LS2100",
                "LS6000",
                "LS7000",
                "LS7000/2",
                "LS8000",
                "LS8000/2",
                "LT9000",
                "FS10000",
            ],
            application_notes="Good general purpose O-Ring. Not recommended for high temperatures.",
            is_active=True,
            sort_order=3,
            chemical_resistance={
                "acids": "Fair",
                "alkalis": "Good",
                "hydrocarbons": "Good",
                "water": "Good",
            },
        ),
    ]

    for o_ring in o_rings:
        exists = db.query(O_Ring).filter_by(code=o_ring.code).first()
        if not exists:
            db.add(o_ring)
