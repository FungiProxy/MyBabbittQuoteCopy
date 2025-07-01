"""
Base Model for storing product family base configurations.

This module defines the BaseModel which represents the base configuration
for each product family. Each base model serves as the starting point
for dynamic configuration and pricing calculations.
"""

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..database import Base


class BaseModel(Base):
    """
    SQLAlchemy model representing a base model for a product family.

    This model stores the base configuration for each product family,
    serving as the starting point for dynamic configuration and pricing.
    All other configurations (materials, voltages, lengths) are handled
    as adders through the options system.

    Attributes:
        id (int): Primary key
        product_family_id (int): Foreign key to the product family
        model_number (str): Base model number (e.g., "LS2000-115VAC-S-10"")
        description (str): Description of the base configuration
        base_price (float): Base price for the family
        base_length (float): Base length in inches
        voltage (str): Base voltage configuration
        material (str): Base material code
        product_family (ProductFamily): Related product family

    Example:
        >>> base_model = BaseModel(
        ...     model_number="LS2000-115VAC-S-10"",
        ...     description="LS2000 Level Switch - Base Configuration",
        ...     base_price=425.0,
        ...     base_length=10.0,
        ...     voltage="115VAC",
        ...     material="S"
        ... )
    """

    __tablename__ = "base_models"

    id = Column(Integer, primary_key=True, index=True)
    product_family_id = Column(
        Integer, ForeignKey("product_families.id"), nullable=False
    )
    model_number = Column(
        String, nullable=False, index=True, unique=True
    )  # e.g., "LS2000-115VAC-S-10""
    description = Column(Text, nullable=False)

    # Base configuration
    base_price = Column(Float, nullable=False, default=0.0)
    base_length = Column(Float, nullable=False)  # Base length in inches
    voltage = Column(String, nullable=False)  # e.g., "115VAC", "24VDC"
    material = Column(String, nullable=False)  # e.g., "S", "H"

    # RTF template data
    insulator_material = Column(Text, nullable=True)
    insulator_length = Column(Float, nullable=True)
    insulator_temp_rating = Column(Text, nullable=True)
    process_connection = Column(Text, nullable=True)
    max_pressure = Column(Text, nullable=True)
    housing_type = Column(Text, nullable=True)
    housing_ratings = Column(Text, nullable=True)
    application_notes = Column(Text, nullable=True)
    special_notes = Column(Text, nullable=True)

    # Relationships
    product_family = relationship("ProductFamily", back_populates="base_model")

    def __repr__(self):
        return f"<BaseModel(id={self.id}, model_number='{self.model_number}', base_price={self.base_price})>"

    def __str__(self):
        return f"{self.model_number} - ${self.base_price:.2f}"
