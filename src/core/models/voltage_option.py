"""
VoltageOption model for storing available voltage options for each product family.

This module defines the VoltageOption model for Babbitt International's quoting system.
It stores which voltage configurations are available for each product family.

Supports:
- Voltage compatibility and filtering for products
"""

from sqlalchemy import Column, ForeignKey, Integer, String

from src.core.database import Base


class VoltageOption(Base):
    """
    SQLAlchemy model representing available voltage options for a product family.

    Stores which voltage configurations (e.g., "24VDC", "115VAC") are available
    for each product family (e.g., "LS2000").

    Attributes:
        id (int): Primary key
        product_family_id (int): Foreign key to product family
        voltage (str): Voltage option (e.g., "24VDC")
        is_available (int): 1 if available, 0 if not

    Example:
        >>> vo = VoltageOption(product_family_id=1, voltage="24VDC", is_available=1)
        >>> print(vo)
    """

    __tablename__ = "voltage_options"

    id = Column(Integer, primary_key=True)
    product_family_id = Column(
        Integer, ForeignKey("product_families.id"), nullable=False
    )
    voltage = Column(String, nullable=False)  # e.g., "24VDC", "115VAC"
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available

    def __repr__(self):
        """
        Return a string representation of the VoltageOption.
        Returns:
            str: A string showing the product family and voltage
        """
        return f"<VoltageOption(product_family_id='{self.product_family_id}', voltage='{self.voltage}')>"
