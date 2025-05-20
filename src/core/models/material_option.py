"""
MaterialOption model for storing available material options for each product family.

This module defines the MaterialOption model for Babbitt International's quoting system.
It stores which material configurations are available for each product family, along
with display names and pricing adders.

Supports:
- Material compatibility and filtering for products
- Material-specific pricing adders
"""
from sqlalchemy import Column, Integer, String, Float
from src.core.database import Base

class MaterialOption(Base):
    """
    SQLAlchemy model representing available material options for a product family.
    
    Stores which material codes (e.g., "S", "H") are available for each product family,
    along with display names and any additional base price for the material.
    
    Attributes:
        id (int): Primary key
        product_family (str): Product family identifier
        material_code (str): Material code (e.g., "S", "H")
        display_name (str): Human-readable material name
        base_price (float): Additional cost for this material
        is_available (int): 1 if available, 0 if not
    
    Example:
        >>> mo = MaterialOption(product_family="LS2000", material_code="S", display_name="S - 316 Stainless Steel", base_price=0.0)
        >>> print(mo)
    """
    
    __tablename__ = "material_options"
    
    id = Column(Integer, primary_key=True)
    product_family = Column(String, nullable=False)  # e.g., "LS2000", "LS6000"
    material_code = Column(String, nullable=False)  # e.g., "S", "H", "A"
    display_name = Column(String, nullable=False)  # e.g., "S - 316 Stainless Steel"
    base_price = Column(Float, default=0.0)  # Additional cost for this material
    is_available = Column(Integer, default=1)  # 1 for available, 0 for not available
    
    def __repr__(self):
        """
        Return a string representation of the MaterialOption.
        Returns:
            str: A string showing the product family, material code, and display name
        """
        return f"<MaterialOption(product_family='{self.product_family}', material='{self.material_code}', display_name='{self.display_name}')>" 