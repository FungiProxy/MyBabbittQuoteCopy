"""
Electrical protection configuration for all product families.

This module defines electrical protection types, their ratings, and application notes
for all product families. It consolidates all electrical protection-related configurations
into a single source of truth.

Supports:
- Protection types (Intrinsic Safety, Explosion Proof, etc.)
- Protection ratings (Class, Division, Groups)
- Application notes and restrictions
- Product-specific configurations
- Certification requirements
"""

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlalchemy import Column, String, Float, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel


class ElectricalProtection(BaseModel):
    """
    SQLAlchemy model representing electrical protection configurations.

    This model stores all electrical protection-related configurations including types,
    ratings, certifications, and application notes. It serves as a single source of truth
    for electrical protection data across all product families.

    Attributes:
        id (int): Primary key
        code (str): Unique protection code (e.g., "IS", "XP", "NPT")
        name (str): Full protection name (e.g., "Intrinsic Safety", "Explosion Proof")
        description (str): Detailed description
        protection_type (str): Type of protection (e.g., "Intrinsic Safety", "Explosion Proof")
        class_rating (str): Class rating (e.g., "I", "II", "III")
        division_rating (str): Division rating (e.g., "1", "2")
        group_rating (str): Group rating (e.g., "A", "B", "C", "D", "E", "F", "G")
        temperature_rating (str): Temperature rating (e.g., "T1", "T2", "T3", "T4", "T5", "T6")
        price (float): Standard price adjustment for this protection type
        material_dependencies (List[str]): List of compatible material codes
        product_families (List[str]): List of compatible product families
        application_notes (str): Important notes about usage and restrictions
        is_active (bool): Whether this protection type is currently active
        sort_order (int): Display order in UI
        validation_rules (Dict): Additional validation rules
        properties (Dict): Protection-specific properties
        restrictions (Dict): Usage restrictions and limitations
        certifications (List[str]): Required certifications and approvals
        installation_requirements (Dict): Installation and maintenance requirements
    """

    __tablename__ = "electrical_protections"

    # Core fields
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    protection_type = Column(String(30), nullable=False)
    class_rating = Column(String(10), nullable=False)
    division_rating = Column(String(10), nullable=False)
    group_rating = Column(String(10), nullable=False)
    temperature_rating = Column(String(10), nullable=False)
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
    certifications = Column(JSON, nullable=True)
    installation_requirements = Column(JSON, nullable=True)

    @validator("code")
    def validate_code(cls, v):
        """Validate protection code format."""
        if not v or len(v) > 10:
            raise ValueError("Protection code must be between 1 and 10 characters")
        return v.upper()

    @validator("class_rating")
    def validate_class_rating(cls, v):
        """Validate class rating."""
        allowed_classes = {"I", "II", "III"}
        if v not in allowed_classes:
            raise ValueError(f"Class rating must be one of {allowed_classes}")
        return v

    @validator("division_rating")
    def validate_division_rating(cls, v):
        """Validate division rating."""
        allowed_divisions = {"1", "2"}
        if v not in allowed_divisions:
            raise ValueError(f"Division rating must be one of {allowed_divisions}")
        return v

    @validator("group_rating")
    def validate_group_rating(cls, v):
        """Validate group rating."""
        allowed_groups = {"A", "B", "C", "D", "E", "F", "G"}
        if v not in allowed_groups:
            raise ValueError(f"Group rating must be one of {allowed_groups}")
        return v

    @validator("temperature_rating")
    def validate_temperature_rating(cls, v):
        """Validate temperature rating."""
        allowed_temps = {"T1", "T2", "T3", "T4", "T5", "T6"}
        if v not in allowed_temps:
            raise ValueError(f"Temperature rating must be one of {allowed_temps}")
        return v

    @validator("price")
    def validate_price(cls, v):
        """Ensure price is non-negative."""
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    def is_compatible_with_material(self, material_code: str) -> bool:
        """Check if this protection type is compatible with a given material."""
        if not self.material_dependencies:
            return True
        return material_code in self.material_dependencies

    def is_compatible_with_product_family(self, family_code: str) -> bool:
        """Check if this protection type is compatible with a given product family."""
        if not self.product_families:
            return True
        return family_code in self.product_families

    def has_certification(self, certification: str) -> bool:
        """Check if this protection type has a specific certification."""
        if not self.certifications:
            return False
        return certification in self.certifications

    def get_installation_requirement(
        self, requirement: str
    ) -> Optional[Union[str, Dict]]:
        """Get a specific installation requirement."""
        if not self.installation_requirements:
            return None
        return self.installation_requirements.get(requirement)

    def __repr__(self):
        """Return a string representation of the electrical protection."""
        return f"<ElectricalProtection(code='{self.code}', name='{self.name}')>"


def init_electrical_protection_options(db):
    """Initialize all electrical protection-related options in the database."""
    protections = [
        ElectricalProtection(
            code="IS",
            name="Intrinsic Safety",
            description="Intrinsic Safety protection for hazardous locations",
            protection_type="Intrinsic Safety",
            class_rating="I",
            division_rating="1",
            group_rating="A",
            temperature_rating="T4",
            price=150.0,  # Standard price adjustment for Intrinsic Safety
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
            application_notes="Intrinsic Safety protection for Class I, Division 1, Group A hazardous locations. Suitable for areas with flammable gases or vapors.",
            is_active=True,
            sort_order=1,
            certifications=["UL", "FM", "ATEX", "IECEx"],
            installation_requirements={
                "barrier_required": True,
                "wiring_requirements": "Shielded cable required",
                "grounding": "Special grounding requirements apply",
                "maintenance": "Annual inspection required",
            },
        ),
        ElectricalProtection(
            code="XP",
            name="Explosion Proof",
            description="Explosion Proof protection for hazardous locations",
            protection_type="Explosion Proof",
            class_rating="I",
            division_rating="1",
            group_rating="D",
            temperature_rating="T4",
            price=200.0,  # Standard price adjustment for Explosion Proof
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
            application_notes="Explosion Proof protection for Class I, Division 1, Group D hazardous locations. Suitable for areas with flammable gases or vapors.",
            is_active=True,
            sort_order=2,
            certifications=["UL", "FM", "ATEX", "IECEx"],
            installation_requirements={
                "conduit_required": True,
                "wiring_requirements": "Conduit seal required",
                "grounding": "Standard grounding requirements",
                "maintenance": "Quarterly inspection required",
            },
        ),
        ElectricalProtection(
            code="NPT",
            name="Non-Incendive",
            description="Non-Incendive protection for hazardous locations",
            protection_type="Non-Incendive",
            class_rating="I",
            division_rating="2",
            group_rating="D",
            temperature_rating="T4",
            price=100.0,  # Standard price adjustment for Non-Incendive
            material_dependencies=["S", "H", "TS", "U", "T"],
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
            application_notes="Non-Incendive protection for Class I, Division 2, Group D hazardous locations. Suitable for areas where flammable gases or vapors are not normally present.",
            is_active=True,
            sort_order=3,
            certifications=["UL", "FM", "ATEX", "IECEx"],
            installation_requirements={
                "conduit_required": False,
                "wiring_requirements": "Standard wiring acceptable",
                "grounding": "Standard grounding requirements",
                "maintenance": "Annual inspection required",
            },
        ),
    ]

    for protection in protections:
        exists = db.query(ElectricalProtection).filter_by(code=protection.code).first()
        if not exists:
            db.add(protection)
