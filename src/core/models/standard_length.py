"""
Standard length model for storing standard length configurations.

This module defines the model for standard lengths used in product configurations.
It supports storing standard length values and their associated metadata.
"""

from sqlalchemy import Column, Float, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.core.database import Base


class StandardLength(Base):
    """
    SQLAlchemy model representing a standard length configuration.

    Stores information about standard lengths, including their value,
    description, and any associated metadata. Can be associated with a specific
    material or used as a general standard length.

    Attributes:
        id (int): Primary key
        material_code (str): Foreign key to material
        length (float): Length value in inches
        tolerance (float): Acceptable deviation from standard length
        description (str): Description of the length
        category (str): Category of the length (e.g., "Standard", "Custom")
        notes (str): Additional notes about the length
        price (float): Optional price for this length
        is_available (bool): Whether this length is currently available

    Example:
        >>> sl = StandardLength(length=10.0, category="Standard")
        >>> print(sl)
    """

    __tablename__ = "standard_lengths"

    id = Column(Integer, primary_key=True)
    material_code = Column(String(10), ForeignKey("materials.code"), nullable=False)
    length = Column(Float, nullable=False)
    tolerance = Column(Float, default=0.001)  # Default tolerance of 0.001 inches
    description = Column(Text)
    category = Column(String, index=True)  # e.g., "Standard", "Custom"
    notes = Column(Text)
    price = Column(Float, nullable=True)
    is_available = Column(Boolean, default=True)

    # Relationships
    material = relationship("Material", back_populates="standard_lengths")

    def __repr__(self):
        """
        Return a string representation of the StandardLength.
        Returns:
            str: A string showing the material code and length
        """
        return f"<StandardLength(material_code='{self.material_code}', length={self.length})>"

    def is_within_tolerance(self, length: float) -> bool:
        """Check if a given length is within tolerance of this standard length."""
        return abs(self.length - length) <= self.tolerance
