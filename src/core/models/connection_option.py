"""
Connection option model for storing product connection configurations.

This module defines the ConnectionOption model for Babbitt International's quoting system.
It stores information about available connection types (flanges and tri-clamps) and their
pricing for different product families.

Supports:
- Flange connections (150# and 300# ratings)
- Tri-Clamp connections
- Size-specific pricing
- Product family compatibility
"""
from sqlalchemy import Column, Integer, String, Float
from src.core.database import Base

class ConnectionOption(Base):
    """
    SQLAlchemy model representing a product connection option.
    
    Stores information about connection types (flanges and tri-clamps), their sizes,
    ratings (for flanges), and pricing. Each connection option can be associated with
    multiple product families.
    
    Attributes:
        id (int): Primary key
        type (str): Connection type ("Flange" or "Tri-Clamp")
        rating (str): Pressure rating for flanges ("150#", "300#"), None for Tri-Clamp
        size (str): Connection size (e.g., '1"', '1.5"', '2"', '3"', '4"')
        price (float): Additional cost for this connection option
        product_families (str): Comma-separated list of compatible product families
    
    Example:
        >>> conn = ConnectionOption(type="Flange", rating="150#", size='2"', price=75.0)
        >>> print(conn)
    """
    
    __tablename__ = "connection_options"
    
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # "Flange" or "Tri-Clamp"
    rating = Column(String, nullable=True)  # "150#", "300#", or None for Tri-Clamp
    size = Column(String, nullable=False)   # e.g., '1"', '1.5"', '2"', '3"', '4"'
    price = Column(Float, default=0.0)
    product_families = Column(String)  # Comma-separated, e.g., "LS2000,LS6000"
    
    def __repr__(self):
        """
        Return a string representation of the ConnectionOption.
        Returns:
            str: A string showing the connection type, rating (if applicable), and size
        """
        rating_str = f", rating='{self.rating}'" if self.rating else ""
        return f"<ConnectionOption(type='{self.type}'{rating_str}, size='{self.size}')>" 