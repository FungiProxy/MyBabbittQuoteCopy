"""
ExoticMetalOption model for storing available exotic metal options for each product family.

This module defines the ExoticMetalOption model for Babbitt International's quoting system.
It stores which exotic metals are available for each product family, along with any price adder.
"""

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from ..database import Base


class ExoticMetalOption(Base):
    """
    SQLAlchemy model representing available exotic metal options for a product family.

    Attributes:
        id (int): Primary key
        product_family_id (int): Foreign key to product family
        metal_type (str): Type of exotic metal (e.g., "Monel", "Hastelloy")
        price (float): Additional cost for this metal
        is_available (int): 1 if available, 0 if not

    Example:
        >>> emo = ExoticMetalOption(product_family_id=1, metal_type="Monel", price=250.0, is_available=1)
        >>> print(emo)
    """

    __tablename__ = "exotic_metal_options"

    id = Column(Integer, primary_key=True)
    product_family_id = Column(
        Integer, ForeignKey("product_families.id"), nullable=False
    )
    metal_type = Column(String, nullable=False)  # Type of exotic metal
    price = Column(Float, default=0.0)  # Additional cost for this metal
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available

    def __repr__(self):
        return f"<ExoticMetalOption(product_family_id='{self.product_family_id}', metal_type='{self.metal_type}', price={self.price})>"
