"""
Insulation configuration for all product families.

This module defines insulation types, their temperature limits, and application notes
for all product families. It consolidates all insulation-related configurations into
a single source of truth.

Supports:
- Insulation types and pricing
- Temperature limits for each type
- Application notes and restrictions
- Material-specific configurations
"""

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlalchemy import Column, String, Float, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel


class Insulation(BaseModel):
    """
    SQLAlchemy model representing insulation configurations.

    This model stores all insulation-related configurations including types,
    temperature limits, and application notes. It serves as a single source
    of truth for insulation data across all product families.

    Attributes:
        id (int): Primary key
        code (str): Unique insulation code (e.g., "DEL", "TEF", "PEEK", "CER")
        name (str): Full insulation name (e.g., "Standard Delrin", "Standard Teflon")
        description (str): Detailed description
        temperature_limit (float): Maximum temperature in Fahrenheit
        base_price (float): Base price for this insulation type
        material_dependencies (List[str]): List of compatible material codes
        product_families (List[str]): List of compatible product families
        application_notes (str): Important notes about usage and restrictions
        is_active (bool): Whether this insulation type is currently active
        sort_order (int): Display order in UI
        validation_rules (Dict): Additional validation rules
        properties (Dict): Insulation-specific properties
        restrictions (Dict): Usage restrictions and limitations
    """

    __tablename__ = "insulations"

    # Core fields
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    temperature_limit = Column(Float, nullable=False)
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

    @validator("code")
    def validate_code(cls, v):
        """Validate insulation code format."""
        if not v or len(v) > 10:
            raise ValueError("Insulation code must be between 1 and 10 characters")
        return v.upper()

    @validator("temperature_limit")
    def validate_temperature(cls, v):
        """Ensure temperature limit is positive and reasonable."""
        if v <= 0 or v > 2000:  # 2000°F as maximum reasonable limit
            raise ValueError("Temperature limit must be between 0 and 2000°F")
        return v

    @validator("base_price")
    def validate_price(cls, v):
        """Ensure price is non-negative."""
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    def is_compatible_with_material(self, material_code: str) -> bool:
        """Check if this insulation is compatible with a given material."""
        if not self.material_dependencies:
            return True
        return material_code in self.material_dependencies

    def is_compatible_with_product_family(self, family_code: str) -> bool:
        """Check if this insulation is compatible with a given product family."""
        if not self.product_families:
            return True
        return family_code in self.product_families

    def __repr__(self):
        """Return a string representation of the Insulation."""
        return f"<Insulation(code='{self.code}', name='{self.name}')>"


def init_insulation_options(db):
    """Initialize all insulation-related options in the database."""
    insulations = [
        Insulation(
            code="DEL",
            name="Standard Delrin",
            description="Standard insulator for SS probes",
            temperature_limit=250.0,
            base_price=0.0,
            material_dependencies=["S"],
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
            application_notes="Standard insulator for SS probes. Not recommended for high temperatures.",
            is_active=True,
            sort_order=1,
        ),
        Insulation(
            code="TEF",
            name="Standard Teflon",
            description="Standard insulator for Halar and TS probes",
            temperature_limit=450.0,
            base_price=40.0,
            material_dependencies=["H", "TS"],
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
            application_notes="Standard insulator for Halar and TS probes. Good chemical resistance.",
            is_active=True,
            sort_order=2,
        ),
        Insulation(
            code="PEEK",
            name="PEEK",
            description="High temperature option",
            temperature_limit=550.0,
            base_price=340.0,
            material_dependencies=["S", "H", "TS", "U", "T", "C", "CPVC"],
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
            application_notes="High temperature option. Excellent chemical resistance.",
            is_active=True,
            sort_order=3,
        ),
        Insulation(
            code="CER",
            name="Ceramic",
            description="Highest temperature option",
            temperature_limit=1400.0,
            base_price=470.0,
            material_dependencies=["S", "H", "TS", "U", "T", "C", "CPVC"],
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
            application_notes="Highest temperature option. For dry materials only. Not suitable for wet applications.",
            is_active=True,
            sort_order=4,
        ),
    ]

    for insulation in insulations:
        exists = db.query(Insulation).filter_by(code=insulation.code).first()
        if not exists:
            db.add(insulation)
