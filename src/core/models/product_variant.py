"""
Product family and base model for storing product information.

This module defines models for product families and base models for Babbitt
International's quoting system. It supports grouping related products and storing
base configurations for dynamic pricing.

Supports:
- Product family grouping and categorization
- Base model configuration and pricing
- Relationships to spare parts and quote items
- Many-to-many relationships with options for dynamic configuration
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from ..database import Base


class ProductFamily(Base):
    """
    SQLAlchemy model representing a product family (group of related products).

    Stores information about a product family, including its name, description,
    category, and relationships to base models, spare parts, and options.

    Attributes:
        id (int): Primary key
        name (str): Product family name (e.g., "LS2000")
        description (str): Description of the product family
        category (str): Category (e.g., "Level Switch")
        base_model (BaseModel): Base model for this family
        spare_parts (List[SparePart]): List of spare parts for this family
        options (List[Option]): List of available options for this family (association_proxy)
        option_associations (List[ProductFamilyOption]): Detailed option associations

    Example:
        >>> pf = ProductFamily(name="LS2000", category="Level Switch")
        >>> print(pf)
    """

    __tablename__ = "product_families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)  # e.g., "LS2000", "LS7000"
    description = Column(Text)
    category = Column(String, index=True)  # e.g., "Level Switch", "Transmitter"

    # Relationships
    base_model = relationship(
        "BaseModel", back_populates="product_family", uselist=False
    )
    spare_parts = relationship("SparePart", back_populates="product_family")
    option_associations = relationship(
        "ProductFamilyOption",
        back_populates="product_family",
        cascade="all, delete-orphan",
    )
    options = association_proxy("option_associations", "option")

    def __repr__(self):
        """
        Return a string representation of the ProductFamily.
        Returns:
            str: A string showing the product family ID, name, and category
        """
        return f"<ProductFamily(id={self.id}, name='{self.name}', category='{self.category}')>"
