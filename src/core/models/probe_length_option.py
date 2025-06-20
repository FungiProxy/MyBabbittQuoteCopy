"""
ProbeLengthOption model for storing available probe lengths for each product family.

This module defines the ProbeLengthOption model for Babbitt International's quoting system.
It stores which probe lengths are available for each product family, along with any price adder.
"""

from sqlalchemy import Column, Float, ForeignKey, Integer

from ..database import Base


class ProbeLengthOption(Base):
    """
    SQLAlchemy model representing available probe length options for a product family.

    Attributes:
        id (int): Primary key
        product_family_id (int): Foreign key to product family
        length (float): Probe length in inches
        price (float): Additional cost for this length
        is_available (int): 1 if available, 0 if not

    Example:
        >>> plo = ProbeLengthOption(product_family_id=1, length=10.0, price=0.0, is_available=1)
        >>> print(plo)
    """

    __tablename__ = 'probe_length_options'

    id = Column(Integer, primary_key=True)
    product_family_id = Column(
        Integer, ForeignKey('product_families.id'), nullable=False
    )
    length = Column(Float, nullable=False)  # Probe length in inches
    price = Column(Float, default=0.0)  # Additional cost for this length
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available

    def __repr__(self):
        return f"<ProbeLengthOption(product_family_id='{self.product_family_id}', length={self.length}, price={self.price})>"
