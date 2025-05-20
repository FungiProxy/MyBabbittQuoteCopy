"""
Product family and variant models for storing product information.

This module defines models for product families and product variants for Babbitt
International's quoting system. It supports grouping related products and storing
specific product configurations.

Supports:
- Product family grouping and categorization
- Product variant configuration and pricing
- Relationships to spare parts and quote items
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


class ProductFamily(Base):
    """
    SQLAlchemy model representing a product family (group of related products).
    
    Stores information about a product family, including its name, description,
    category, and relationships to variants and spare parts.
    
    Attributes:
        id (int): Primary key
        name (str): Product family name (e.g., "LS2000")
        description (str): Description of the product family
        category (str): Category (e.g., "Level Switch")
        variants (List[ProductVariant]): List of product variants in this family
        spare_parts (List[SparePart]): List of spare parts for this family
    
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
    variants = relationship("ProductVariant", back_populates="product_family")
    spare_parts = relationship("SparePart", back_populates="product_family")
    
    def __repr__(self):
        """
        Return a string representation of the ProductFamily.
        Returns:
            str: A string showing the product family ID, name, and category
        """
        return f"<ProductFamily(id={self.id}, name='{self.name}', category='{self.category}')>"


class ProductVariant(Base):
    """
    SQLAlchemy model representing a specific product configuration (variant).
    
    Stores information about a product variant, including its model number,
    description, pricing, configuration options, and relationships to its family
    and quote items.
    
    Attributes:
        id (int): Primary key
        product_family_id (int): Foreign key to the product family
        model_number (str): Unique model number for the variant
        description (str): Description of the variant
        base_price (float): Base price for the variant
        base_length (float): Base length in inches
        voltage (str): Voltage configuration
        material (str): Material code
        product_family (ProductFamily): Related product family
        quote_items (List[QuoteItem]): List of quote items for this variant
    
    Example:
        >>> pv = ProductVariant(model_number="LS2000-115VAC-S-10", base_price=450.0)
        >>> print(pv)
    """
    
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    product_family_id = Column(Integer, ForeignKey("product_families.id"), nullable=False)
    model_number = Column(String, nullable=False, index=True)  # e.g., "LS2000-115VAC-S-10""
    description = Column(Text)
    
    # Pricing information
    base_price = Column(Float, nullable=False, default=0.0)
    base_length = Column(Float)  # Base length in inches
    
    # Configuration options
    voltage = Column(String)  # e.g., "115VAC", "24VDC"
    material = Column(String)  # e.g., "S", "H", "U", "T"
    
    # Relationships
    product_family = relationship("ProductFamily", back_populates="variants")
    quote_items = relationship("QuoteItem", back_populates="product")
    
    def __repr__(self):
        """
        Return a string representation of the ProductVariant.
        Returns:
            str: A string showing the variant ID, model number, and base price
        """
        return f"<ProductVariant(id={self.id}, model='{self.model_number}', base_price={self.base_price})>" 