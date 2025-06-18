"""
Product family model for storing product family information.

This module defines the ProductFamily model which represents a family of related products
(e.g., LS2000 series) in Babbitt International's quoting system. Each product family
contains basic information about a group of related products, including their common
attributes, pricing rules, and available configurations.

The ProductFamily model supports:
- Unique product family identification
- Base pricing information
- Standard configurations
- Material and voltage options
- Categorization and searching
- Relationships to variants and spare parts
"""

from sqlalchemy import Column, Float, String, Text
from sqlalchemy.orm import relationship

from src.core.models.base_model import BaseModel


class ProductFamily(BaseModel):
    """
    SQLAlchemy model representing a Babbitt International product family.

    This model stores the fundamental product family information and serves as the base
    for product configuration and pricing calculations. Each product family has a unique
    name and can be configured with different materials, voltages, and other options.

    Attributes:
        name (str): Unique product family name (e.g., "LS2000", "LS8000")
        description (str): Detailed product family description
        category (str): Product category for grouping (e.g., "Level Switch", "Transmitter")
        base_price (float): Starting price before material/length adjustments
        base_length (float): Standard length in inches for the product family
        default_voltage (str): Default voltage configuration (e.g., "115VAC", "24VDC")
        default_material (str): Default material code:
                - "S": 316 Stainless Steel
                - "H": Halar Coated
                - "U": UHMWPE
                - "T": Teflon
        is_active (bool): Whether this product family is currently active
        variants (List[ProductVariant]): List of product variants in this family
        spare_parts (List[SparePart]): List of spare parts for this family
        products (List[Product]): List of products in this family

    Note:
        - Product variants (specific configurations) are handled by the ProductVariant model
        - Pricing calculations consider material-specific rules and length adjustments
        - The name field is indexed for efficient searching
        - Categories are indexed to support filtering and grouping

    Example:
        >>> family = ProductFamily(
        ...     name="LS2000",
        ...     description="Level Switch Series 2000",
        ...     category="Level Switch",
        ...     base_price=450.00,
        ...     base_length=10.0,
        ...     default_voltage="115VAC",
        ...     default_material="S"
        ... )
    """

    __tablename__ = "product_families"

    # Basic information
    name = Column(String, nullable=False, index=True, unique=True)
    description = Column(Text)
    category = Column(String, index=True)

    # Pricing information
    base_price = Column(Float, nullable=False, default=0.0)
    base_length = Column(Float)  # Base length in inches

    # Default configuration options
    default_voltage = Column(String)  # e.g., "115VAC", "24VDC"
    default_material = Column(String)  # e.g., "S", "H", "U", "T"

    # Status
    is_active = Column(String, default="Y")  # "Y" for active, "N" for inactive

    # Relationships
    products = relationship(
        "Product", back_populates="product_family", cascade="all, delete-orphan"
    )
    variants = relationship(
        "ProductVariant", back_populates="product_family", cascade="all, delete-orphan"
    )
    voltage_options = relationship(
        "VoltageOption", back_populates="product_family", cascade="all, delete-orphan"
    )
    connection_options = relationship(
        "ConnectionOption",
        back_populates="product_family",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """
        Return a string representation of the ProductFamily.

        Returns:
            str: A string showing the product family's name and category
        """
        return f"<ProductFamily(name='{self.name}', category='{self.category}')>"

    def get_active_variants(self):
        """
        Get all active variants for this product family.

        Returns:
            List[ProductVariant]: List of active product variants
        """
        return [v for v in self.variants if v.is_active == "Y"]

    def to_dict(self) -> dict:
        """
        Convert product family to dictionary, including active variants.

        Returns:
            dict: Dictionary representation of the product family
        """
        data = super().to_dict()
        data["variants"] = [v.to_dict() for v in self.get_active_variants()]
        return data
