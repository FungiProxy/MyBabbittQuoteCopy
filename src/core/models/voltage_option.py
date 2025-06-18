"""
VoltageOption model for storing available voltage options for each product family.

This module defines the VoltageOption model for Babbitt International's quoting system.
It stores which voltage configurations are available for each product family.

Supports:
- Voltage compatibility and filtering for products
- Voltage-specific pricing and restrictions
- Voltage validation and constraints
- Product family voltage requirements
"""

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Boolean,
    JSON,
    DateTime,
)
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel


class VoltageOption(BaseModel):
    """
    SQLAlchemy model representing available voltage options for a product family.

    Stores which voltage configurations (e.g., "24VDC", "115VAC") are available
    for each product family (e.g., "LS2000").

    Attributes:
        id (int): Primary key
        product_family_id (int): Foreign key to product family
        voltage (str): Voltage option (e.g., "24VDC")
        is_available (bool): Whether this voltage is available
        created_at (datetime): Timestamp of creation
        updated_at (datetime): Timestamp of last update
        description (str): Detailed description of the voltage option
        base_price_adder (float): Additional base price for this voltage
        restrictions (Dict): Usage restrictions and limitations
        validation_rules (Dict): Additional validation rules
        properties (Dict): Voltage-specific properties
        sort_order (int): Display order in UI
        is_active (bool): Whether the voltage option is currently active
        product_family (ProductFamily): Related product family object
    """

    __tablename__ = "voltage_options"

    # Core fields
    product_family_id = Column(
        Integer, ForeignKey("product_families.id"), nullable=False, index=True
    )
    voltage = Column(String(20), nullable=False, index=True)
    description = Column(String(200))
    is_available = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # Pricing and properties
    base_price_adder = Column(Float, default=0.0)
    restrictions = Column(JSON, nullable=True)
    validation_rules = Column(JSON, nullable=True)
    properties = Column(JSON, nullable=True)

    # Relationships
    product_family = relationship("ProductFamily", back_populates="voltage_options")

    @validator("voltage")
    def validate_voltage(cls, v):
        """Validate voltage format."""
        if not v or len(v) > 20:
            raise ValueError("Voltage must be between 1 and 20 characters")

        # Basic format validation (e.g., "24VDC", "115VAC")
        if not any(v.endswith(suffix) for suffix in ["VDC", "VAC"]):
            raise ValueError("Voltage must end with VDC or VAC")

        # Extract numeric part and validate
        try:
            value = float(v[:-3])
            if value <= 0:
                raise ValueError("Voltage value must be positive")
        except ValueError:
            raise ValueError("Invalid voltage value")

        return v

    @validator("base_price_adder")
    def validate_price(cls, v):
        """Ensure price adder is non-negative."""
        if v < 0:
            raise ValueError("Price adder cannot be negative")
        return v

    def is_compatible_with_product(self, product_id: str) -> bool:
        """Check if this voltage is compatible with a given product."""
        if not self.restrictions:
            return True

        # Implement compatibility checking logic here
        # This is a placeholder for actual implementation
        return True

    def get_voltage_value(self) -> float:
        """Extract the numeric voltage value."""
        return float(self.voltage[:-3])

    def get_voltage_type(self) -> str:
        """Get the voltage type (DC or AC)."""
        return self.voltage[-3:]

    def calculate_price(self, base_price: float) -> float:
        """Calculate the total price including voltage-specific adder."""
        return base_price + self.base_price_adder

    def __repr__(self):
        """Return a string representation of the VoltageOption."""
        return f"<VoltageOption(product_family_id={self.product_family_id}, voltage='{self.voltage}', available={self.is_available})>"
