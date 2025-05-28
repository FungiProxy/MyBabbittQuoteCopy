"""
HousingTypeOption model for storing available housing type options for each product family.

This module defines the HousingTypeOption model for Babbitt International's quoting system.
It stores which housing types are available for each product family, along with any price adder.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.core.database import Base

class HousingTypeOption(Base):
    """
    SQLAlchemy model representing available housing type options for a product family.
    
    Attributes:
        id (int): Primary key
        product_family_id (int): Foreign key to product family
        housing_type (str): Type of housing (e.g., "Aluminum", "Stainless Steel")
        price (float): Additional cost for this housing type
        is_available (int): 1 if available, 0 if not
    
    Example:
        >>> hto = HousingTypeOption(product_family_id=1, housing_type="Aluminum", price=0.0, is_available=1)
        >>> print(hto)
    """
    __tablename__ = "housing_type_options"

    id = Column(Integer, primary_key=True)
    product_family_id = Column(Integer, ForeignKey("product_families.id"), nullable=False)
    housing_type = Column(String, nullable=False)  # Type of housing
    price = Column(Float, default=0.0)  # Additional cost for this housing type
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available

    def __repr__(self):
        return f"<HousingTypeOption(product_family_id='{self.product_family_id}', housing_type='{self.housing_type}', price={self.price})>" 