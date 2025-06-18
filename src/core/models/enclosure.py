"""
Enclosure configuration for all product families.

This module defines enclosure types, their specifications, and application notes
for all product families. It consolidates all enclosure-related configurations into
a single source of truth.

Supports:
- Enclosure types and ratings (NEMA, IP)
- Material and mounting options
- Application notes and restrictions
- Product-specific configurations
"""

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlalchemy import Column, String, Float, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel


class Enclosure(BaseModel):
    """
    SQLAlchemy model representing enclosure configurations.

    This model stores all enclosure-related configurations including types,
    ratings, materials, and application notes. It serves as a single source
    of truth for enclosure data across all product families.

    Attributes:
        id (int): Primary key
        code (str): Unique enclosure code (e.g., "N4X", "IP67")
        name (str): Full enclosure name (e.g., "NEMA 4X", "IP67")
        description (str): Detailed description
        rating_type (str): Rating type ("NEMA" or "IP")
        rating_value (str): Rating value (e.g., "4X", "67")
        material (str): Enclosure material (e.g., "SS", "PC")
        mounting_type (str): Mounting type (e.g., "Wall", "Pipe")
        base_price (float): Base price for this enclosure type
        material_dependencies (List[str]): List of compatible material codes
        product_families (List[str]): List of compatible product families
        application_notes (str): Important notes about usage and restrictions
        is_active (bool): Whether this enclosure type is currently active
        sort_order (int): Display order in UI
        validation_rules (Dict): Additional validation rules
        properties (Dict): Enclosure-specific properties
        restrictions (Dict): Usage restrictions and limitations
        dimensions (Dict): Physical dimensions
    """

    __tablename__ = "enclosures"

    # Core fields
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    rating_type = Column(String(10), nullable=False)  # "NEMA" or "IP"
    rating_value = Column(String(10), nullable=False)
    material = Column(String(20), nullable=False)
    mounting_type = Column(String(20), nullable=False)
    base_price = Column(Float, default=0.0)
    material_dependencies = Column(JSON, nullable=True)
    product_families = Column(JSON, nullable=True)
    application_notes = Column(String(500))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # Additional properties
    validation_rules = Column(JSON, nullable=True)
    properties = Column(JSON, nullable=True)
    restrictions = Column(JSON, nullable=True)
    dimensions = Column(JSON, nullable=True)

    @validator("code")
    def validate_code(cls, v):
        """Validate enclosure code format."""
        if not v or len(v) > 10:
            raise ValueError("Enclosure code must be between 1 and 10 characters")
        return v.upper()

    @validator("rating_type")
    def validate_rating_type(cls, v):
        """Validate rating type."""
        allowed_types = {"NEMA", "IP"}
        if v not in allowed_types:
            raise ValueError(f"Rating type must be one of {allowed_types}")
        return v

    @validator("base_price")
    def validate_price(cls, v):
        """Ensure price is non-negative."""
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    def is_compatible_with_material(self, material_code: str) -> bool:
        """Check if this enclosure is compatible with a given material."""
        if not self.material_dependencies:
            return True
        return material_code in self.material_dependencies

    def is_compatible_with_product_family(self, family_code: str) -> bool:
        """Check if this enclosure is compatible with a given product family."""
        if not self.product_families:
            return True
        return family_code in self.product_families

    def get_dimensions(self) -> Dict[str, float]:
        """Get the physical dimensions of the enclosure."""
        return self.dimensions or {}

    def __repr__(self):
        """Return a string representation of the Enclosure."""
        return f"<Enclosure(code='{self.code}', name='{self.name}')>"


def init_enclosure_options(db):
    """Initialize all enclosure-related options in the database."""
    enclosures = [
        Enclosure(
            code="N4X",
            name="NEMA 4X",
            description="Stainless Steel NEMA 4X Enclosure",
            rating_type="NEMA",
            rating_value="4X",
            material="SS",
            mounting_type="Wall",
            base_price=150.0,
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
            application_notes="Suitable for harsh environments. Corrosion resistant.",
            is_active=True,
            sort_order=1,
            dimensions={
                "width": 6.0,
                "height": 8.0,
                "depth": 4.0,
            },
        ),
        Enclosure(
            code="IP67",
            name="IP67",
            description="Polycarbonate IP67 Enclosure",
            rating_type="IP",
            rating_value="67",
            material="PC",
            mounting_type="Pipe",
            base_price=100.0,
            material_dependencies=["S", "H", "TS", "U", "T"],
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
            application_notes="Water and dust tight. Suitable for outdoor use.",
            is_active=True,
            sort_order=2,
            dimensions={
                "width": 5.0,
                "height": 7.0,
                "depth": 3.0,
            },
        ),
    ]

    for enclosure in enclosures:
        exists = db.query(Enclosure).filter_by(code=enclosure.code).first()
        if not exists:
            db.add(enclosure)
