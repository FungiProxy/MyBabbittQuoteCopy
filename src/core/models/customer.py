"""
Customer model for storing customer information.

This module defines the Customer model for Babbitt International's quoting system.
It stores client contact and company information, and supports relationships to quotes.

Supports:
- Customer contact and company details
- Relationship to all quotes for the customer
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

from ..database import Base


class Customer(Base):
    """
    SQLAlchemy model representing a customer/client.

    Stores contact and company information for a customer, and provides a relationship
    to all quotes associated with the customer.

    Attributes:
        id (int): Primary key
        name (str): Customer's name
        company (str): Company name
        email (str): Email address
        phone (str): Phone number
        address (str): Street address
        city (str): City
        state (str): State
        zip_code (str): Postal code
        notes (str): Additional notes
        quotes (List[Quote]): List of quotes for this customer
        created_at (DateTime): Timestamp when the customer was created
        updated_at (DateTime): Timestamp when the customer was last updated

    Example:
        >>> customer = Customer(name="Jane Doe", company="Acme Corp", email="jane@acme.com")
        >>> print(customer)
    """

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    company = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship to quotes
    quotes = relationship(
        "Quote", back_populates="customer", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """
        Return a string representation of the Customer.
        Returns:
            str: A string showing the customer ID, name, and company
        """
        return f"<Customer(id={self.id}, name='{self.name}', company='{self.company}')>"
