"""
Exotic metal configuration for all product families.

This module defines exotic metal types, their properties, and application notes
for all product families. It consolidates all exotic metal-related configurations into
a single source of truth.

Supports:
- Exotic metal types (Monel, Hastelloy, etc.)
- Temperature and chemical resistance ratings
- Application notes and restrictions
- Material-specific configurations
- Pricing rules and validation
"""

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlalchemy import Column, String, Float, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel


class ExoticMetal(BaseModel):
    """
    SQLAlchemy model representing exotic metal configurations.

    This model stores all exotic metal-related configurations including types,
    properties, temperature limits, and application notes. It serves as a single
    source of truth for exotic metal data across all product families.

    Attributes:
        id (int): Primary key
        code (str): Unique metal code (e.g., "MON", "HAS", "TIT")
        name (str): Full metal name (e.g., "Monel", "Hastelloy", "Titanium")
        description (str): Detailed description
        temperature_limit (float): Maximum temperature in Fahrenheit
        price (float): Standard price adjustment for this metal type
        material_dependencies (List[str]): List of compatible material codes
        product_families (List[str]): List of compatible product families
        application_notes (str): Important notes about usage and restrictions
        is_active (bool): Whether this metal type is currently active
        sort_order (int): Display order in UI
        validation_rules (Dict): Additional validation rules
        properties (Dict): Metal-specific properties
        restrictions (Dict): Usage restrictions and limitations
        chemical_resistance (Dict): Chemical resistance ratings
        mechanical_properties (Dict): Mechanical properties (strength, hardness, etc.)
        certifications (List[str]): Industry certifications and approvals
    """

    __tablename__ = "exotic_metals"

    # Core fields
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    temperature_limit = Column(Float, nullable=False)
    price = Column(Float, default=0.0)  # Standard price adjustment
    material_dependencies = Column(JSON, nullable=True)
    product_families = Column(JSON, nullable=True)
    application_notes = Column(String(500))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # Additional properties
    validation_rules = Column(JSON, nullable=True)
    properties = Column(JSON, nullable=True)
    restrictions = Column(JSON, nullable=True)
    chemical_resistance = Column(JSON, nullable=True)
    mechanical_properties = Column(JSON, nullable=True)
    certifications = Column(JSON, nullable=True)

    @validator("code")
    def validate_code(cls, v):
        """Validate metal code format."""
        if not v or len(v) > 10:
            raise ValueError("Metal code must be between 1 and 10 characters")
        return v.upper()

    @validator("temperature_limit")
    def validate_temperature(cls, v):
        """Ensure temperature limit is positive and reasonable."""
        if v <= 0 or v > 2000:  # 2000°F as maximum reasonable limit for exotic metals
            raise ValueError("Temperature limit must be between 0 and 2000°F")
        return v

    @validator("price")
    def validate_price(cls, v):
        """Ensure price is non-negative."""
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    def is_compatible_with_material(self, material_code: str) -> bool:
        """Check if this metal is compatible with a given material."""
        if not self.material_dependencies:
            return True
        return material_code in self.material_dependencies

    def is_compatible_with_product_family(self, family_code: str) -> bool:
        """Check if this metal is compatible with a given product family."""
        if not self.product_families:
            return True
        return family_code in self.product_families

    def get_chemical_resistance(self, chemical: str) -> Optional[str]:
        """Get the chemical resistance rating for a specific chemical."""
        if not self.chemical_resistance:
            return None
        return self.chemical_resistance.get(chemical)

    def get_mechanical_property(
        self, property_name: str
    ) -> Optional[Union[float, str]]:
        """Get a specific mechanical property value."""
        if not self.mechanical_properties:
            return None
        return self.mechanical_properties.get(property_name)

    def has_certification(self, certification: str) -> bool:
        """Check if this metal has a specific certification."""
        if not self.certifications:
            return False
        return certification in self.certifications

    def __repr__(self):
        """Return a string representation of the exotic metal."""
        return f"<ExoticMetal(code='{self.code}', name='{self.name}')>"


def init_exotic_metal_options(db):
    """Initialize all exotic metal-related options in the database."""
    exotic_metals = [
        ExoticMetal(
            code="MON",
            name="Monel",
            description="Monel 400 alloy",
            temperature_limit=1000.0,
            price=250.0,  # Standard price adjustment for Monel
            material_dependencies=["S", "H", "TS"],
            product_families=[
                "LS2000",
                "LS2100",
                "LS6000",
                "LS7000",
                "LS7000/2",
                "LS8000",
                "LS8000/2",
                "LT9000",
                "FS10000",
            ],
            application_notes="Excellent corrosion resistance in marine environments. Good for high-temperature applications.",
            is_active=True,
            sort_order=1,
            chemical_resistance={
                "acids": {
                    "rating": "Good",
                    "details": "Resistant to most acids except oxidizing acids",
                    "max_concentration": "50%",
                    "temperature_limit": 200,
                },
                "alkalis": {
                    "rating": "Excellent",
                    "details": "Highly resistant to alkaline solutions",
                    "max_concentration": "75%",
                    "temperature_limit": 300,
                },
                "salt_water": {
                    "rating": "Excellent",
                    "details": "Superior resistance to salt water and marine environments",
                    "max_concentration": "100%",
                    "temperature_limit": 400,
                },
                "steam": {
                    "rating": "Good",
                    "details": "Good resistance to steam and high-temperature water",
                    "max_concentration": "100%",
                    "temperature_limit": 500,
                },
            },
            mechanical_properties={
                "tensile_strength": 80000,  # psi
                "yield_strength": 35000,  # psi
                "hardness": "Brinell 150",
                "elongation": "35%",
            },
            certifications=["ASME", "ASTM B127", "NACE MR0175"],
        ),
        ExoticMetal(
            code="HAS",
            name="Hastelloy",
            description="Hastelloy C-276 alloy",
            temperature_limit=1200.0,
            price=350.0,  # Standard price adjustment for Hastelloy
            material_dependencies=["S", "H", "TS"],
            product_families=[
                "LS2000",
                "LS2100",
                "LS6000",
                "LS7000",
                "LS7000/2",
                "LS8000",
                "LS8000/2",
                "LT9000",
                "FS10000",
            ],
            application_notes="Superior corrosion resistance in harsh chemical environments. Excellent for high-temperature applications.",
            is_active=True,
            sort_order=2,
            chemical_resistance={
                "acids": {
                    "rating": "Excellent",
                    "details": "Superior resistance to oxidizing and reducing acids",
                    "max_concentration": "100%",
                    "temperature_limit": 400,
                },
                "alkalis": {
                    "rating": "Excellent",
                    "details": "Excellent resistance to alkaline solutions",
                    "max_concentration": "100%",
                    "temperature_limit": 500,
                },
                "salt_water": {
                    "rating": "Excellent",
                    "details": "Superior resistance to salt water and marine environments",
                    "max_concentration": "100%",
                    "temperature_limit": 600,
                },
                "steam": {
                    "rating": "Excellent",
                    "details": "Superior resistance to steam and high-temperature water",
                    "max_concentration": "100%",
                    "temperature_limit": 700,
                },
            },
            mechanical_properties={
                "tensile_strength": 100000,  # psi
                "yield_strength": 45000,  # psi
                "hardness": "Brinell 200",
                "elongation": "40%",
            },
            certifications=["ASME", "ASTM B575", "NACE MR0175", "ISO 15156"],
        ),
        ExoticMetal(
            code="TIT",
            name="Titanium",
            description="Titanium Grade 2",
            temperature_limit=800.0,
            price=300.0,  # Standard price adjustment for Titanium
            material_dependencies=["S", "H", "TS"],
            product_families=[
                "LS2000",
                "LS2100",
                "LS6000",
                "LS7000",
                "LS7000/2",
                "LS8000",
                "LS8000/2",
                "LT9000",
                "FS10000",
            ],
            application_notes="Excellent corrosion resistance and high strength-to-weight ratio. Good for marine and chemical applications.",
            is_active=True,
            sort_order=3,
            chemical_resistance={
                "acids": {
                    "rating": "Good",
                    "details": "Good resistance to most acids except hydrofluoric and concentrated sulfuric",
                    "max_concentration": "30%",
                    "temperature_limit": 150,
                },
                "alkalis": {
                    "rating": "Good",
                    "details": "Good resistance to alkaline solutions",
                    "max_concentration": "50%",
                    "temperature_limit": 200,
                },
                "salt_water": {
                    "rating": "Excellent",
                    "details": "Superior resistance to salt water and marine environments",
                    "max_concentration": "100%",
                    "temperature_limit": 300,
                },
                "steam": {
                    "rating": "Good",
                    "details": "Good resistance to steam and high-temperature water",
                    "max_concentration": "100%",
                    "temperature_limit": 400,
                },
            },
            mechanical_properties={
                "tensile_strength": 50000,  # psi
                "yield_strength": 40000,  # psi
                "hardness": "Brinell 120",
                "elongation": "20%",
            },
            certifications=["ASME", "ASTM B265", "NACE MR0175", "ISO 15156"],
        ),
    ]

    for metal in exotic_metals:
        exists = db.query(ExoticMetal).filter_by(code=metal.code).first()
        if not exists:
            db.add(metal)
