"""
Option model for storing product add-ons and their pricing.

This module defines models for product options (add-ons) and their association
with quote line items. It includes:
- Option: Represents a configurable add-on or feature for a product
- ProductFamilyOption: Junction table linking product families to options
- QuoteItemOption: Junction table for tracking which options are added to which quote items

These models support:
- Option pricing (fixed, per-inch, per-foot)
- Compatibility with product families via proper many-to-many relationships
- Exclusion of incompatible products
- Tracking option selections in quotes
- Structured choices, adders, and rules for dynamic configuration
"""

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from sqlalchemy.ext.associationproxy import association_proxy

from core.database import Base


class Option(Base):
    """
    SQLAlchemy model representing a configurable product option (add-on).

    Stores information about an option, including its name, description, pricing,
    category, compatibility rules, and now structured choices/adders/rules for dynamic configuration.

    Attributes:
        id (int): Primary key
        name (str): Option name
        description (str): Detailed description
        price (float): Base price for the option
        price_type (str): Pricing type ("fixed", "per_inch", "per_foot")
        category (str): Option category (e.g., "mounting", "feature")
        excluded_products (str): Comma-separated incompatible products
        choices (list): List of possible choices for this option
        adders (dict): Mapping of choice to price adder
        rules (str or dict): Rules for option logic
        product_families (association_proxy): Many-to-many relationship with ProductFamily

    Example:
        >>> option = Option(name="Material", choices=["S", "H"], adders={"H": 110}, rules="H max 72\"")
        >>> print(option)
    """

    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)

    # Pricing information
    price = Column(Float, nullable=False, default=0.0)
    price_type = Column(String, default="fixed")  # "fixed", "per_inch", "per_foot"

    # Option category
    category = Column(String, index=True)  # e.g., "mounting", "material", "feature"

    # Compatibility
    excluded_products = Column(String)  # Comma-separated list of incompatible products

    # Structured configuration
    choices = Column(JSON, nullable=True)  # List of possible choices
    adders = Column(JSON, nullable=True)  # Dict of choice -> adder
    rules = Column(JSON, nullable=True)  # Rules for option logic (or Text if preferred)

    # Relationships
    family_associations = relationship(
        "ProductFamilyOption", back_populates="option", cascade="all, delete-orphan"
    )
    product_families = association_proxy("family_associations", "product_family")

    def __repr__(self):
        """
        Return a string representation of the Option.
        Returns:
            str: A string showing the option's ID, name, and price
        """
        return f"<Option(id={self.id}, name='{self.name}', price={self.price}, choices={self.choices})>"


class ProductFamilyOption(Base):
    """
    SQLAlchemy model representing the association between product families and options.

    This is a junction table that tracks which options are available for each
    product family, including any family-specific pricing or availability rules.

    Attributes:
        product_family_id (int): Foreign key to the product family
        option_id (int): Foreign key to the option
        is_available (bool): Whether this option is available for this family
        family_specific_price (float): Optional family-specific price override
        notes (str): Any family-specific notes or rules
    """

    __tablename__ = "product_family_options"

    product_family_id = Column(
        Integer, ForeignKey("product_families.id"), primary_key=True
    )
    option_id = Column(Integer, ForeignKey("options.id"), primary_key=True)
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available
    family_specific_price = Column(Float, nullable=True)  # Optional price override
    notes = Column(Text, nullable=True)  # Family-specific notes

    # Relationships
    product_family = relationship("ProductFamily", back_populates="option_associations")
    option = relationship("Option", back_populates="family_associations")

    def __repr__(self):
        """
        Return a string representation of the ProductFamilyOption.
        Returns:
            str: A string showing the family and option IDs
        """
        return f"<ProductFamilyOption(family_id={self.product_family_id}, option_id={self.option_id})>"


class QuoteItemOption(Base):
    """
    SQLAlchemy model representing an option added to a quote line item.

    This is a junction table that tracks which options are selected for each
    quote item, including the quantity and price at the time of quoting.

    Attributes:
        id (int): Primary key
        quote_item_id (int): Foreign key to the quote item
        option_id (int): Foreign key to the option
        quantity (int): Number of this option selected
        price (float): Price per unit at the time of quote
        quote_item (QuoteItem): Parent quote item
        option (Option): Related option object

    Example:
        >>> qio = QuoteItemOption(quote_item_id=1, option_id=2, quantity=1, price=250.0)
        >>> print(qio)
    """

    __tablename__ = "quote_item_options"

    id = Column(Integer, primary_key=True, index=True)
    quote_item_id = Column(Integer, ForeignKey("quote_items.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("options.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)  # Price at time of quote

    # Relationships
    quote_item = relationship("QuoteItem", back_populates="options")
    option = relationship("Option")

    def __repr__(self):
        """
        Return a string representation of the QuoteItemOption.
        Returns:
            str: A string showing the option ID and price
        """
        return f"<QuoteItemOption(id={self.id}, option_id={self.option_id}, price={self.price})>"
