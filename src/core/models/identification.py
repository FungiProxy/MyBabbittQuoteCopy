from sqlalchemy import Column, String, Float, Boolean, JSON, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base_model import BaseModel


class Identification(BaseModel):
    """Model for product identification and marking options."""

    __tablename__ = "identifications"

    # Basic Information
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    # Label Configuration
    label_type = Column(
        String(50), nullable=False
    )  # e.g., "Engraved", "Laser Etched", "Printed"
    marking_method = Column(
        String(50), nullable=False
    )  # e.g., "Direct", "Label", "Tag"
    placement_location = Column(
        String(50), nullable=False
    )  # e.g., "Body", "Cable", "Tag"

    # Content Options
    content_type = Column(
        String(50), nullable=False
    )  # e.g., "Model Number", "Serial Number", "Custom Text"
    max_characters = Column(Integer)
    font_type = Column(String(50))
    font_size = Column(String(20))

    # Material Properties
    material = Column(String(50))  # e.g., "Stainless Steel", "Aluminum", "Plastic"
    surface_finish = Column(String(50))  # e.g., "Polished", "Bead Blasted", "Matte"

    # Durability
    durability_rating = Column(String(50))  # e.g., "High", "Medium", "Low"
    weather_resistance = Column(Boolean, default=False)
    chemical_resistance = Column(Boolean, default=False)

    # Pricing
    base_price = Column(Float, nullable=False)
    price_per_character = Column(Float, default=0.0)
    setup_fee = Column(Float, default=0.0)

    # Compatibility
    product_families = Column(JSON, default=list)  # List of compatible product families
    material_dependencies = Column(JSON, default=list)  # List of compatible materials
    restrictions = Column(JSON, default=dict)  # Any restrictions or limitations

    # Additional Properties
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # Validation Rules
    validation_rules = Column(JSON, default=dict)

    # Customization Options
    customization_options = Column(JSON, default=dict)  # e.g., colors, sizes, styles

    # Compliance
    compliance_standards = Column(JSON, default=list)  # e.g., UL, CSA, ATEX

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_attributes()

    def _validate_attributes(self):
        """Validate all attributes according to rules."""
        self._validate_code()
        self._validate_name()
        self._validate_price()
        self._validate_characters()

    def _validate_code(self):
        """Validate identification code format."""
        if not self.code:
            raise ValueError("Code is required")
        if not self.code.isalnum():
            raise ValueError("Code must be alphanumeric")

    def _validate_name(self):
        """Validate identification name."""
        if not self.name:
            raise ValueError("Name is required")

    def _validate_price(self):
        """Validate pricing information."""
        if self.base_price < 0:
            raise ValueError("Base price cannot be negative")
        if self.price_per_character < 0:
            raise ValueError("Price per character cannot be negative")
        if self.setup_fee < 0:
            raise ValueError("Setup fee cannot be negative")

    def _validate_characters(self):
        """Validate character limits."""
        if self.max_characters is not None and self.max_characters < 0:
            raise ValueError("Maximum characters cannot be negative")

    def is_compatible_with_material(self, material_code: str) -> bool:
        """Check if identification is compatible with a material."""
        return material_code in self.material_dependencies

    def is_compatible_with_product_family(self, family_code: str) -> bool:
        """Check if identification is compatible with a product family."""
        return family_code in self.product_families

    def calculate_price(self, character_count: int = 0) -> float:
        """Calculate total price for identification."""
        total = self.base_price
        if character_count > 0:
            total += character_count * self.price_per_character
        total += self.setup_fee
        return total

    def get_placement_guidelines(self) -> dict:
        """Get placement guidelines for the identification."""
        return {
            "location": self.placement_location,
            "orientation": self.validation_rules.get("orientation", "horizontal"),
            "spacing": self.validation_rules.get("spacing", "standard"),
            "clearance": self.validation_rules.get("clearance", "minimum"),
        }

    def get_durability_info(self) -> dict:
        """Get durability information."""
        return {
            "rating": self.durability_rating,
            "weather_resistant": self.weather_resistance,
            "chemical_resistant": self.chemical_resistance,
            "expected_lifetime": self.validation_rules.get(
                "expected_lifetime", "standard"
            ),
        }

    def get_compliance_info(self) -> dict:
        """Get compliance and certification information."""
        return {
            "standards": self.compliance_standards,
            "certifications": self.validation_rules.get("certifications", []),
            "marking_requirements": self.validation_rules.get(
                "marking_requirements", {}
            ),
        }


def init_identification_options(db):
    """Initialize identification options in the database."""
    options = [
        {
            "code": "ENGRAVED",
            "name": "Engraved Marking",
            "description": "Permanent engraved marking on product body",
            "label_type": "Engraved",
            "marking_method": "Direct",
            "placement_location": "Body",
            "content_type": "Model Number",
            "max_characters": 50,
            "font_type": "Standard",
            "font_size": "Medium",
            "material": "Stainless Steel",
            "surface_finish": "Bead Blasted",
            "durability_rating": "High",
            "weather_resistance": True,
            "chemical_resistance": True,
            "base_price": 25.00,
            "price_per_character": 0.50,
            "setup_fee": 15.00,
            "product_families": ["RTD", "TC", "PRESSURE"],
            "material_dependencies": ["SS304", "SS316", "ALUMINUM"],
            "validation_rules": {
                "orientation": "horizontal",
                "spacing": "standard",
                "clearance": "minimum",
                "expected_lifetime": "10 years",
                "certifications": ["UL", "CSA"],
                "marking_requirements": {"depth": "0.5mm", "width": "0.3mm"},
            },
            "compliance_standards": ["UL", "CSA", "ATEX"],
        },
        {
            "code": "LASER",
            "name": "Laser Etched Marking",
            "description": "High-precision laser etched marking",
            "label_type": "Laser Etched",
            "marking_method": "Direct",
            "placement_location": "Body",
            "content_type": "Model Number",
            "max_characters": 100,
            "font_type": "Standard",
            "font_size": "Small",
            "material": "Stainless Steel",
            "surface_finish": "Polished",
            "durability_rating": "High",
            "weather_resistance": True,
            "chemical_resistance": True,
            "base_price": 35.00,
            "price_per_character": 0.25,
            "setup_fee": 20.00,
            "product_families": ["RTD", "TC", "PRESSURE"],
            "material_dependencies": ["SS304", "SS316", "ALUMINUM"],
            "validation_rules": {
                "orientation": "horizontal",
                "spacing": "compact",
                "clearance": "minimum",
                "expected_lifetime": "15 years",
                "certifications": ["UL", "CSA"],
                "marking_requirements": {"depth": "0.2mm", "width": "0.1mm"},
            },
            "compliance_standards": ["UL", "CSA", "ATEX"],
        },
        {
            "code": "LABEL",
            "name": "Adhesive Label",
            "description": "Durable adhesive label with custom text",
            "label_type": "Printed",
            "marking_method": "Label",
            "placement_location": "Body",
            "content_type": "Custom Text",
            "max_characters": 200,
            "font_type": "Custom",
            "font_size": "Medium",
            "material": "Polyester",
            "surface_finish": "Matte",
            "durability_rating": "Medium",
            "weather_resistance": True,
            "chemical_resistance": False,
            "base_price": 15.00,
            "price_per_character": 0.10,
            "setup_fee": 10.00,
            "product_families": ["RTD", "TC", "PRESSURE"],
            "material_dependencies": ["SS304", "SS316", "ALUMINUM", "PLASTIC"],
            "validation_rules": {
                "orientation": "horizontal",
                "spacing": "standard",
                "clearance": "standard",
                "expected_lifetime": "5 years",
                "certifications": ["UL"],
                "marking_requirements": {
                    "adhesive_type": "Permanent",
                    "thickness": "0.1mm",
                },
            },
            "compliance_standards": ["UL"],
        },
    ]

    for option_data in options:
        option = Identification(**option_data)
        db.add(option)

    db.commit()
