"""
Material model for storing product material information and pricing rules.

This module defines models for product materials, standard lengths, and material
availability for Babbitt International's quoting system. It includes:
- Material: Material codes, names, and pricing rules
- StandardLength: Standard lengths for materials (for surcharge logic)
- MaterialAvailability: Which materials are available for which product types

Supports:
- Material-specific pricing and surcharges
- Standard vs. non-standard length logic
- Material compatibility with product types
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Base


class Material(Base):
    """
    SQLAlchemy model representing a product material and its pricing rules.
    
    Stores material codes, names, descriptions, and pricing logic for length-based
    adjustments and surcharges. Also tracks which product types the material is
    available for.
    
    Attributes:
        id (int): Primary key
        code (str): Material code (e.g., "S", "H", "U", "T")
        name (str): Full material name
        description (str): Description of the material
        base_length (float): Standard base length in inches
        length_adder_per_inch (float): Additional cost per inch
        length_adder_per_foot (float): Additional cost per foot
        has_nonstandard_length_surcharge (bool): If non-standard length surcharge applies
        nonstandard_length_surcharge (float): Surcharge amount
        base_price_adder (float): Additional base price for this material
        product_types (List[MaterialAvailability]): Product types this material is available for
    
    Example:
        >>> material = Material(code="S", name="316 Stainless Steel", base_length=10.0)
        >>> print(material)
    """
    
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, index=True, unique=True)  # e.g., "S", "H", "U", "T"
    name = Column(String, nullable=False)  # Full name, e.g., "316 Stainless Steel"
    description = Column(Text)
    
    # Pricing information
    base_length = Column(Float, nullable=False)  # Standard base length in inches
    length_adder_per_inch = Column(Float)  # Additional cost per inch
    length_adder_per_foot = Column(Float)  # Additional cost per foot
    
    # Special pricing rules
    has_nonstandard_length_surcharge = Column(Boolean, default=False)
    nonstandard_length_surcharge = Column(Float, default=0.0)
    base_price_adder = Column(Float, default=0.0)  # Amount to add to base price
    
    # Relationships
    product_types = relationship("MaterialAvailability", back_populates="material")
    
    def __repr__(self):
        """
        Return a string representation of the Material.
        Returns:
            str: A string showing the material code and name
        """
        return f"<Material(code='{self.code}', name='{self.name}')>"
    
    
class StandardLength(Base):
    """
    SQLAlchemy model representing standard lengths for a material.
    
    Used to determine if a length is standard (no surcharge) or non-standard
    (surcharge applies) for a given material.
    
    Attributes:
        id (int): Primary key
        material_code (str): Material code
        length (float): Standard length in inches
    
    Example:
        >>> sl = StandardLength(material_code="H", length=24.0)
        >>> print(sl)
    """
    
    __tablename__ = "standard_lengths"
    
    id = Column(Integer, primary_key=True, index=True)
    material_code = Column(String, nullable=False, index=True)
    length = Column(Float, nullable=False)  # Length in inches
    
    def __repr__(self):
        """
        Return a string representation of the StandardLength.
        Returns:
            str: A string showing the material code and length
        """
        return f"<StandardLength(material='{self.material_code}', length={self.length})>"


class MaterialAvailability(Base):
    """
    SQLAlchemy model tracking which materials are available for which product types.
    
    Used to enforce material compatibility and availability rules for quoting.
    
    Attributes:
        id (int): Primary key
        material_code (str): Material code (foreign key)
        product_type (str): Product type/model (e.g., "LS2000")
        is_available (bool): If the material is available for this product type
        notes (str): Additional notes
        material (Material): Related material object
    
    Example:
        >>> ma = MaterialAvailability(material_code="S", product_type="LS2000", is_available=True)
        >>> print(ma)
    """
    
    __tablename__ = "material_availability"
    
    id = Column(Integer, primary_key=True, index=True)
    material_code = Column(String, ForeignKey("materials.code"), nullable=False, index=True)
    product_type = Column(String, nullable=False, index=True)  # e.g., "LS2000", "LS7000/2", "FS10000"
    is_available = Column(Boolean, default=True)
    notes = Column(Text)
    
    # Relationships
    material = relationship("Material", back_populates="product_types")
    
    def __repr__(self):
        """
        Return a string representation of the MaterialAvailability.
        Returns:
            str: A string showing the material code, product type, and availability
        """
        return f"<MaterialAvailability(material='{self.material_code}', product_type='{self.product_type}', available={self.is_available})>" 