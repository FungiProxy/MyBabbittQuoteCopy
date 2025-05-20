"""
Product model for storing product information.

This module defines the Product model which represents the core product catalog
for Babbitt International. Each product entry contains basic information about
a product type, including its model number, description, pricing, and default
configuration options.

The Product model supports:
- Unique product identification
- Base pricing information
- Standard configurations
- Material and voltage options
- Categorization and searching
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


class Product(Base):
    """
    SQLAlchemy model representing a Babbitt International product.
    
    This model stores the fundamental product information and serves as the base
    for product configuration and pricing calculations. Each product has a unique
    model number and can be configured with different materials and voltages.
    
    Attributes:
        id (int): Primary key for the product
        model_number (str): Unique product model number (e.g., "LS2000", "LS8000/2")
        description (str): Detailed product description
        category (str): Product category for grouping (e.g., "Level Switch", "Transmitter")
        base_price (float): Starting price before material/length adjustments
        base_length (float): Standard length in inches for the product
        voltage (str): Default voltage configuration (e.g., "115VAC", "24VDC")
        material (str): Default material code:
                       - "S": 316 Stainless Steel
                       - "H": Halar Coated
                       - "U": UHMWPE
                       - "T": Teflon
    
    Note:
        - Product variants (specific configurations) are handled by the ProductVariant model
        - Pricing calculations consider material-specific rules and length adjustments
        - The model_number field is indexed for efficient searching
        - Categories are indexed to support filtering and grouping
    
    Example:
        >>> product = Product(
        ...     model_number="LS2000-115VAC-S-10",
        ...     description="Level Switch, 10 inch, Stainless Steel",
        ...     category="Level Switch",
        ...     base_price=450.00,
        ...     base_length=10.0,
        ...     voltage="115VAC",
        ...     material="S"
        ... )
    """
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    model_number = Column(String, nullable=False, index=True)  # e.g., "LS2000", "LS8000/2"
    description = Column(Text)
    category = Column(String, index=True)  # e.g., "Level Switch", "Transmitter"
    
    # Pricing information
    base_price = Column(Float, nullable=False, default=0.0)
    base_length = Column(Float)  # Base length in inches
    
    # Configuration options
    voltage = Column(String)  # e.g., "115VAC", "24VDC"
    material = Column(String)  # e.g., "S", "H", "U", "T"
    
    # No relationships with QuoteItem - it now relates to ProductVariant
    
    def __repr__(self) -> str:
        """
        Return a string representation of the Product.
        
        Returns:
            str: A string showing the product's ID, model number, and base price
        """
        return f"<Product(id={self.id}, model='{self.model_number}', base_price={self.base_price})>"            