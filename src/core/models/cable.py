"""
Cable configuration for all product families.

This module defines cable types, specifications, and application notes
for all product families. It consolidates all cable-related configurations into
a single source of truth.

Supports:
- Cable types and specifications
- Length options
- Connection types
- Pricing rules
- Application notes and restrictions
- Product-specific configurations
"""

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlalchemy import Column, String, Float, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel


class Cable(BaseModel):
    """
    SQLAlchemy model representing cable configurations.

    This model stores all cable-related configurations including types,
    specifications, length options, connection types, and application notes.
    It serves as a single source of truth for cable data across all product families.

    Attributes:
        id (int): Primary key
        code (str): Unique cable code (e.g., "CBL18AWG", "CBL22AWG")
        name (str): Full cable name (e.g., "18 AWG PVC Cable")
        description (str): Detailed description
        cable_type (str): Cable type (e.g., "PVC", "Teflon")
        specification (str): Specification (e.g., "18 AWG 3C")
        length_options (List[float]): Available lengths in feet
        connection_type (str): Connection type (e.g., "Flying Leads", "Connector")
        base_price (float): Base price for this cable type
        price_per_foot (float): Price per foot
        material_dependencies (List[str]): List of compatible material codes
        product_families (List[str]): List of compatible product families
        application_notes (str): Important notes about usage and restrictions
        is_active (bool): Whether this cable type is currently active
        sort_order (int): Display order in UI
        validation_rules (Dict): Additional validation rules
        properties (Dict): Cable-specific properties
        restrictions (Dict): Usage restrictions and limitations
    """

    __tablename__ = "cables"

    # Core fields
    code = Column(String(20), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200))
    cable_type = Column(String(20), nullable=False)
    specification = Column(String(50), nullable=False)
    length_options = Column(JSON, nullable=True)  # List of available lengths (feet)
    connection_type = Column(String(30), nullable=False)
    base_price = Column(Float, default=0.0)
    price_per_foot = Column(Float, default=0.0)
    material_dependencies = Column(JSON, nullable=True)
    product_families = Column(JSON, nullable=True)
    application_notes = Column(String(500))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # Additional properties
    validation_rules = Column(JSON, nullable=True)
    properties = Column(JSON, nullable=True)
    restrictions = Column(JSON, nullable=True)

    @validator("code")
    def validate_code(cls, v):
        """Validate cable code format."""
        if not v or len(v) > 20:
            raise ValueError("Cable code must be between 1 and 20 characters")
        return v.upper()

    @validator("base_price", "price_per_foot")
    def validate_price(cls, v):
        """Ensure price is non-negative."""
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    def is_compatible_with_material(self, material_code: str) -> bool:
        """Check if this cable is compatible with a given material."""
        if not self.material_dependencies:
            return True
        return material_code in self.material_dependencies

    def is_compatible_with_product_family(self, family_code: str) -> bool:
        """Check if this cable is compatible with a given product family."""
        if not self.product_families:
            return True
        return family_code in self.product_families

    def calculate_price(self, length: float) -> float:
        """Calculate the total price for a given cable length (in feet)."""
        return self.base_price + (self.price_per_foot * length)

    def __repr__(self):
        """Return a string representation of the Cable."""
        return f"<Cable(code='{self.code}', name='{self.name}')>"


def init_cable_options(db):
    """Initialize all cable-related options in the database."""
    cables = [
        Cable(
            code="CBL18AWG",
            name="18 AWG PVC Cable",
            description="Standard 18 AWG 3-conductor PVC cable",
            cable_type="PVC",
            specification="18 AWG 3C",
            length_options=[10, 25, 50, 100],
            connection_type="Flying Leads",
            base_price=10.0,
            price_per_foot=0.5,
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
            application_notes="Standard cable for most applications.",
            is_active=True,
            sort_order=1,
        ),
        Cable(
            code="CBL22AWG",
            name="22 AWG Teflon Cable",
            description="High-temp 22 AWG 4-conductor Teflon cable",
            cable_type="Teflon",
            specification="22 AWG 4C",
            length_options=[10, 25, 50, 100],
            connection_type="Connector",
            base_price=20.0,
            price_per_foot=1.0,
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
            application_notes="High temperature and chemical resistance.",
            is_active=True,
            sort_order=2,
        ),
    ]

    for cable in cables:
        exists = db.query(Cable).filter_by(code=cable.code).first()
        if not exists:
            db.add(cable)
