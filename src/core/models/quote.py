"""
Quote models for storing customer quotes and line items.

This module defines the data models for customer quotes and their associated line items
in the Babbitt International quoting system. It includes:
- Quote: The quote header, customer, status, and overall metadata
- QuoteItem: Individual line items, each representing a product configuration

These models support:
- Quote and line item storage
- Relationships to customers, products, and options
- Calculation of totals, discounts, and option pricing
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


class Quote(Base):
    """
    SQLAlchemy model representing a customer quote (header).
    
    Stores metadata about a quote, including the customer, creation/expiration dates,
    status, and associated line items. Provides a property to calculate the total
    value of the quote.
    
    Attributes:
        id (int): Primary key
        quote_number (str): Unique quote identifier
        customer_id (int): Foreign key to the customer
        date_created (datetime): Quote creation timestamp
        expiration_date (datetime): Expiration date for the quote
        status (str): Quote status ("draft", "sent", "accepted", "rejected")
        notes (str): Additional notes or comments
        customer (Customer): Related customer object
        items (List[QuoteItem]): List of line items in the quote
    
    Example:
        >>> quote = Quote(quote_number="Q-2024-001", customer_id=1)
        >>> print(quote.total)
    """
    
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_number = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    expiration_date = Column(DateTime)
    status = Column(String, default="draft")  # "draft", "sent", "accepted", "rejected"
    notes = Column(Text)
    
    # Relationships
    customer = relationship("Customer", back_populates="quotes")
    items = relationship("QuoteItem", back_populates="quote", cascade="all, delete-orphan")
    
    def __repr__(self):
        """
        Return a string representation of the Quote.
        Returns:
            str: A string showing the quote's ID, number, and status
        """
        return f"<Quote(id={self.id}, quote_number='{self.quote_number}', status='{self.status}')>"
    
    @property
    def total(self):
        """
        Calculate the total amount for the quote (sum of all line items).
        Returns:
            float: Total value of the quote
        """
        return sum(item.total for item in self.items)


class QuoteItem(Base):
    """
    SQLAlchemy model representing a line item in a quote.
    
    Each QuoteItem stores a specific product configuration, including quantity,
    pricing, material, voltage, and any options. Provides properties for subtotal,
    discount, and total calculations.
    
    Attributes:
        id (int): Primary key
        quote_id (int): Foreign key to the parent quote
        product_id (int): Foreign key to the product variant
        quantity (int): Number of units for this line item
        unit_price (float): Price per unit at the time of quoting
        length (float): Length in inches (if applicable)
        material (str): Material code (if applicable)
        voltage (str): Voltage specification (if applicable)
        description (str): Custom description for the line item
        discount_percent (float): Discount percentage applied
        quote (Quote): Parent quote object
        product (ProductVariant): Related product variant
        options (List[QuoteItemOption]): List of option line items
    
    Example:
        >>> item = QuoteItem(product_id=1, quantity=2, unit_price=500.0)
        >>> print(item.total)
    """
    
    __tablename__ = "quote_items"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False)
    
    # Product configuration
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)  # Base price at time of quote
    length = Column(Float)  # Length in inches if applicable
    material = Column(String)  # Material code if applicable
    voltage = Column(String)  # Voltage specification if applicable
    description = Column(Text)  # Custom description
    
    # Pricing
    discount_percent = Column(Float, default=0.0)
    
    # Relationships
    quote = relationship("Quote", back_populates="items")
    product = relationship("ProductVariant", back_populates="quote_items")
    options = relationship("QuoteItemOption", back_populates="quote_item", cascade="all, delete-orphan")
    
    def __repr__(self):
        """
        Return a string representation of the QuoteItem.
        Returns:
            str: A string showing the item ID, product ID, and quantity
        """
        return f"<QuoteItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
    
    @property
    def options_total(self):
        """
        Calculate the total price for all options in this line item.
        
        Sums up the price of each option multiplied by its quantity. This represents
        the total cost of all add-ons and customizations for this line item.
        
        Returns:
            float: Total value of all options
        """
        return sum(option.price * option.quantity for option in self.options)
    
    @property
    def subtotal(self):
        """
        Calculate the subtotal before discount.
        
        Combines the base price (unit price * quantity) with the total cost of all
        options. This represents the full price before any discounts are applied.
        
        Returns:
            float: Subtotal before discount
        """
        return (self.unit_price * self.quantity) + self.options_total
    
    @property
    def discount_amount(self):
        """
        Calculate the discount amount for this line item.
        
        Applies the discount percentage to the subtotal to determine the actual
        discount value in currency units.
        
        Returns:
            float: Discount value in currency units
        """
        return self.subtotal * (self.discount_percent / 100)
    
    @property
    def total(self):
        """
        Calculate the total for this line item with discount applied.
        
        Subtracts the discount amount from the subtotal to get the final price
        for this line item, including all options and discounts.
        
        Returns:
            float: Final total for the line item
        """
        return self.subtotal - self.discount_amount 