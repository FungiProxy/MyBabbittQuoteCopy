"""
Spare parts model for storing spare part information.

This module defines the SparePart model for Babbitt International's quoting system.
It stores information about spare parts, their pricing, and their relationship to
product families.

Supports:
- Spare part cataloging and pricing
- Categorization by type (electronics, probe assembly, housing, etc.)
- Relationship to product families
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Base


class SparePart(Base):
    """
    SQLAlchemy model representing a spare part and its pricing.
    
    Stores information about a spare part, including part number, name, description,
    price, category, and its relationship to a product family.
    
    Attributes:
        id (int): Primary key
        part_number (str): Unique part number
        name (str): Spare part name
        description (str): Description of the spare part
        price (float): Price of the spare part
        product_family_id (int): Foreign key to the product family
        category (str): Category of the spare part (e.g., "electronics")
        product_family (ProductFamily): Related product family object
    
    Example:
        >>> sp = SparePart(part_number="SP-1001", name="Probe Assembly", price=150.0)
        >>> print(sp)
    """
    
    __tablename__ = "spare_parts"
    
    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Pricing information
    price = Column(Float, nullable=False, default=0.0)
    
    # Related product family
    product_family_id = Column(Integer, ForeignKey("product_families.id"))
    
    # Categorization
    category = Column(String, index=True)  # e.g., "electronics", "probe_assembly", "housing"
    
    # Relationships
    product_family = relationship("ProductFamily", back_populates="spare_parts")
    
    def __repr__(self):
        """
        Return a string representation of the SparePart.
        Returns:
            str: A string showing the spare part ID, part number, name, and price
        """
        return f"<SparePart(id={self.id}, part_number='{self.part_number}', name='{self.name}', price={self.price})>" 