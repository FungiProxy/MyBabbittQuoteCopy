"""
Material model for storing material configurations.

This module defines the model for materials used in product configurations.
It supports storing material properties, pricing rules, and standard lengths.
"""

from sqlalchemy import Column, Float, Integer, String, Boolean, JSON, ForeignKey, event
from sqlalchemy.orm import relationship, validates
from sqlalchemy.exc import IntegrityError

from src.core.database import Base
from src.core.models.standard_length import StandardLength


class Material(Base):
    """
    SQLAlchemy model representing a material configuration.

    Stores information about materials, including their properties,
    pricing rules, and standard lengths.

    Attributes:
        id (int): Primary key
        code (str): Material code (e.g., "S", "H", "U", "T", "TS")
        name (str): Material name (e.g., "316SS", "Halar", "UHMW", "Teflon", "Teflon Sleeve")
        description (str): Description of the material
        base_length (float): Base length in inches
        length_adder_per_inch (float): Price adder per inch
        length_adder_per_foot (float): Price adder per foot
        has_nonstandard_length_surcharge (bool): Whether non-standard lengths have a surcharge
        nonstandard_length_surcharge (float): Surcharge amount for non-standard lengths
        base_price_adder (float): Base price adder for the material
        validation_rules (dict): Material-specific validation rules
        properties (dict): Additional material properties
        restrictions (dict): Material-specific restrictions
    """

    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    base_length = Column(Float, default=10.0)  # Default base length of 10 inches
    length_adder_per_inch = Column(Float, default=0.0)
    length_adder_per_foot = Column(Float, default=0.0)

    # Special pricing rules
    has_nonstandard_length_surcharge = Column(Boolean, default=False)
    nonstandard_length_surcharge = Column(Float, default=0.0)
    base_price_adder = Column(Float, default=0.0)

    # Additional properties
    validation_rules = Column(JSON, nullable=True)
    properties = Column(JSON, nullable=True)
    restrictions = Column(JSON, nullable=True)

    # Relationships
    product_types = relationship(
        "MaterialAvailability", back_populates="material", cascade="all, delete-orphan"
    )
    standard_lengths = relationship(
        "StandardLength", back_populates="material", cascade="all, delete-orphan"
    )

    @validates("code")
    def validate_code(self, key, code):
        """Validate material code format."""
        if not code:
            raise IntegrityError(None, None, "Material code is required")
        if len(code) > 10:
            raise IntegrityError(
                None, None, "Material code must be 10 characters or less"
            )
        if not code.isalnum():
            raise IntegrityError(
                None, None, "Material code must contain only alphanumeric characters"
            )
        return code.upper()

    @validates(
        "base_length",
        "length_adder_per_inch",
        "length_adder_per_foot",
        "nonstandard_length_surcharge",
        "base_price_adder",
    )
    def validate_pricing(self, key, value):
        """Ensure pricing values are non-negative."""
        if value is None:
            return 0.0
        if value < 0:
            raise IntegrityError(None, None, "Pricing values cannot be negative")
        return value

    def calculate_price(self, length: float) -> float:
        """Calculate the total price for a given length."""
        if length <= 0:
            raise ValueError("Length must be greater than 0")

        # Start with base price adder
        price = self.base_price_adder

        # Add length-based pricing
        if self.length_adder_per_inch:
            price += length * self.length_adder_per_inch
        elif self.length_adder_per_foot:
            price += (length / 12) * self.length_adder_per_foot

        # Add non-standard length surcharge if applicable
        if self.has_nonstandard_length_surcharge and not self.is_standard_length(
            length
        ):
            price += self.nonstandard_length_surcharge

        return price

    def is_standard_length(self, length: float) -> bool:
        """Check if a given length is standard for this material."""
        if not self.standard_lengths:
            return False
        return any(abs(sl.length - length) < 0.001 for sl in self.standard_lengths)

    def is_available_for_product(self, product_type: str) -> bool:
        """Check if this material is available for a given product type."""
        return any(
            pt.product_type == product_type and pt.is_available
            for pt in self.product_types
        )

    def __repr__(self):
        """Return a string representation of the Material."""
        return f"<Material(code='{self.code}', name='{self.name}')>"


class MaterialAvailability(Base):
    """Model for tracking material availability by product type."""

    __tablename__ = "material_availability"

    id = Column(Integer, primary_key=True)
    material_code = Column(String(10), ForeignKey("materials.code"), nullable=False)
    product_type = Column(String(50), nullable=False)
    is_available = Column(Boolean, default=True)

    # Relationships
    material = relationship("Material", back_populates="product_types")

    def __repr__(self):
        return f"<MaterialAvailability(material_code='{self.material_code}', product_type='{self.product_type}', is_available={self.is_available})>"
