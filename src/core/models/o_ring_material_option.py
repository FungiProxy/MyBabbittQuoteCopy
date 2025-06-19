"""
O_RingMaterialOption model for storing available O-Ring material options for each product family.

This module defines the O_RingMaterialOption model for Babbitt International's quoting system.
It stores which O-Ring materials are available for each product family, along with any price adder.
"""

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from ..database import Base


class O_RingMaterialOption(Base):
    """
    SQLAlchemy model representing available O-Ring material options for a product family.

    Attributes:
        id (int): Primary key
        product_family_id (int): Foreign key to product family
        material_type (str): Type of O-Ring material (e.g., "Viton", "EPDM")
        price (float): Additional cost for this material
        is_available (int): 1 if available, 0 if not

    Example:
        >>> ormo = O_RingMaterialOption(product_family_id=1, material_type="Viton", price=25.0, is_available=1)
        >>> print(ormo)
    """

    __tablename__ = "o_ring_material_options"

    id = Column(Integer, primary_key=True)
    product_family_id = Column(
        Integer, ForeignKey("product_families.id"), nullable=False
    )
    material_type = Column(String, nullable=False)  # Type of O-Ring material
    price = Column(Float, default=0.0)  # Additional cost for this material
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available

    def __repr__(self):
        return f"<O_RingMaterialOption(product_family_id='{self.product_family_id}', material_type='{self.material_type}', price={self.price})>"
