"""
Option model for storing product add-ons and their pricing.

This module defines models for product options (add-ons) and their association
with quote line items. It includes:
- Option: Represents a configurable add-on or feature for a product
- QuoteItemOption: Junction table for tracking which options are added to which quote items

These models support:
- Option pricing (fixed, per-inch, per-foot)
- Compatibility with product families
- Exclusion of incompatible products
- Tracking option selections in quotes
- Structured choices, adders, and rules for dynamic configuration
"""

from datetime import datetime
from typing import Dict, List, Optional, Union
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel


class Option(BaseModel):
    """
    SQLAlchemy model representing a configurable product option (add-on).

    Stores information about an option, including its name, description, pricing,
    category, compatibility rules, and structured choices/adders/rules for dynamic configuration.

    Attributes:
        id (int): Primary key
        name (str): Option name
        description (str): Detailed description
        price (float): Base price for the option
        price_type (str): Pricing type ("fixed", "per_inch", "per_foot")
        category (str): Option category (e.g., "mounting", "feature")
        product_families (List[str]): List of compatible product families
        excluded_products (List[str]): List of incompatible products
        choices (List[str]): List of possible choices for this option
        adders (Dict[str, float]): Mapping of choice to price adder
        rules (Dict): Rules for option logic
        created_at (datetime): Timestamp of creation
        updated_at (datetime): Timestamp of last update
        is_active (bool): Whether the option is currently active
        sort_order (int): Display order in UI
        validation_rules (Dict): Additional validation rules
        dependencies (List[int]): IDs of options this depends on
        conflicts (List[int]): IDs of options this conflicts with
    """

    __tablename__ = "options"

    # Core fields
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50), index=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    # Pricing information
    price = Column(Float, nullable=False, default=0.0)
    price_type = Column(String(20), default="fixed")  # "fixed", "per_inch", "per_foot"

    # Compatibility and relationships
    product_families = Column(JSON, default=list)  # List of compatible product families
    excluded_products = Column(JSON, default=list)  # List of incompatible products
    dependencies = Column(JSON, default=list)  # List of option IDs this depends on
    conflicts = Column(JSON, default=list)  # List of option IDs this conflicts with

    # Structured configuration
    choices = Column(JSON, nullable=True)  # List of possible choices
    adders = Column(JSON, nullable=True)  # Dict of choice -> adder
    rules = Column(JSON, nullable=True)  # Rules for option logic
    validation_rules = Column(JSON, nullable=True)  # Additional validation rules

    # Relationships
    quote_items = relationship(
        "QuoteItemOption", back_populates="option", cascade="all, delete-orphan"
    )

    @validator("price_type")
    def validate_price_type(cls, v):
        """Validate that price_type is one of the allowed values."""
        allowed_types = {"fixed", "per_inch", "per_foot"}
        if v not in allowed_types:
            raise ValueError(f"price_type must be one of {allowed_types}")
        return v

    @validator("product_families", "excluded_products", "dependencies", "conflicts")
    def validate_lists(cls, v):
        """Ensure lists are properly formatted."""
        if not isinstance(v, list):
            return []
        return v

    def is_compatible_with_product(self, product_id: str) -> bool:
        """Check if this option is compatible with a given product."""
        return product_id not in self.excluded_products

    def get_price_for_choice(self, choice: str, quantity: float = 1.0) -> float:
        """Calculate the total price for a given choice and quantity."""
        base_price = self.price
        if self.adders and choice in self.adders:
            base_price += self.adders[choice]

        if self.price_type == "per_inch":
            return base_price * quantity
        elif self.price_type == "per_foot":
            return base_price * (quantity / 12)
        return base_price

    def validate_choice(self, choice: str) -> bool:
        """Validate if a choice is valid for this option."""
        if not self.choices:
            return False
        return choice in self.choices

    def __repr__(self):
        """Return a string representation of the Option."""
        return f"<Option(id={self.id}, name='{self.name}', price={self.price}, choices={self.choices})>"


class QuoteItemOption(BaseModel):
    """
    SQLAlchemy model representing an option added to a quote line item.

    This is a junction table that tracks which options are selected for each
    quote item, including the quantity and price at the time of quoting.

    Attributes:
        id (int): Primary key
        quote_item_id (int): Foreign key to the quote item
        option_id (int): Foreign key to the option
        quantity (int): Number of this option selected
        price (float): Price per unit at the time of quoting
        selected_choice (str): The specific choice selected for this option
        quote_item (QuoteItem): Parent quote item
        option (Option): Related option object
        created_at (datetime): Timestamp of creation
        updated_at (datetime): Timestamp of last update
    """

    __tablename__ = "quote_item_options"

    quote_item_id = Column(Integer, ForeignKey("quote_items.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("options.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)
    selected_choice = Column(String(100), nullable=True)

    # Relationships
    quote_item = relationship("QuoteItem", back_populates="options")
    option = relationship("Option", back_populates="quote_items")

    @validator("quantity")
    def validate_quantity(cls, v):
        """Ensure quantity is positive."""
        if v < 1:
            raise ValueError("Quantity must be at least 1")
        return v

    @validator("price")
    def validate_price(cls, v):
        """Ensure price is non-negative."""
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    def calculate_total_price(self) -> float:
        """Calculate the total price for this option selection."""
        return self.price * self.quantity

    def __repr__(self):
        """Return a string representation of the QuoteItemOption."""
        return f"<QuoteItemOption(id={self.id}, option_id={self.option_id}, price={self.price})>"
