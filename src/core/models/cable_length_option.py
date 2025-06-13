"""
CableLengthOption model for storing available cable length options for each product family.

This module defines the CableLengthOption model for Babbitt International's quoting system.
It stores which cable lengths are available for each product family, along with any price adder.
"""

from sqlalchemy import Column, Integer, Float, ForeignKey
from src.core.database import Base


class CableLengthOption(Base):
    """
    SQLAlchemy model representing available cable length options for a product family.

    Attributes:
        id (int): Primary key
        product_family_id (int): Foreign key to product family
        length (float): Cable length in feet
        price (float): Additional cost for this length
        is_available (int): 1 if available, 0 if not

    Example:
        >>> clo = CableLengthOption(product_family_id=1, length=10.0, price=15.0, is_available=1)
        >>> print(clo)
    """

    __tablename__ = "cable_length_options"

    id = Column(Integer, primary_key=True)
    product_family_id = Column(
        Integer, ForeignKey("product_families.id"), nullable=False
    )
    length = Column(Float, nullable=False)  # Cable length in feet
    price = Column(Float, default=0.0)  # Additional cost for this length
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available

    def __repr__(self):
        return f"<CableLengthOption(product_family_id='{self.product_family_id}', length={self.length}, price={self.price})>"
