from sqlalchemy import (
    Column,
    String,
    Float,
    Boolean,
    JSON,
    Integer,
    ForeignKey,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .base_model import BaseModel


class SparePart(BaseModel):
    """Model for spare parts and replacement components."""

    __tablename__ = "spare_parts"

    # Basic Information
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    part_number = Column(String(50), unique=True, nullable=False)

    # Part Details
    part_type = Column(
        String(50), nullable=False
    )  # e.g., "Sensor", "Cable", "Connector"
    material = Column(String(50))  # e.g., "Stainless Steel", "Aluminum"
    dimensions = Column(JSON, default=dict)  # Physical dimensions
    weight = Column(Float)  # Weight in grams

    # Compatibility
    compatible_models = Column(JSON, default=list)  # List of compatible product models
    product_families = Column(JSON, default=list)  # List of compatible product families
    material_dependencies = Column(JSON, default=list)  # List of compatible materials
    restrictions = Column(JSON, default=dict)  # Any restrictions or limitations

    # Inventory
    current_stock = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=0)
    reorder_point = Column(Integer, default=0)
    reorder_quantity = Column(Integer, default=0)
    lead_time_days = Column(Integer, default=0)

    # Pricing
    base_price = Column(Float, nullable=False)
    price_breaks = Column(JSON, default=dict)  # Quantity-based price breaks
    is_taxable = Column(Boolean, default=True)

    # Technical Specifications
    specifications = Column(JSON, default=dict)  # Technical specifications
    certifications = Column(JSON, default=list)  # e.g., UL, CSA, ATEX
    operating_conditions = Column(JSON, default=dict)  # Temperature, pressure, etc.

    # Additional Properties
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    is_critical = Column(Boolean, default=False)  # Critical for operation
    is_consumable = Column(Boolean, default=False)  # Regular replacement part

    # Validation Rules
    validation_rules = Column(JSON, default=dict)

    # Tracking
    last_restock_date = Column(DateTime)
    last_restock_quantity = Column(Integer)
    last_order_date = Column(DateTime)
    last_order_quantity = Column(Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_attributes()

    def _validate_attributes(self):
        """Validate all attributes according to rules."""
        self._validate_code()
        self._validate_name()
        self._validate_part_number()
        self._validate_price()
        self._validate_stock()

    def _validate_code(self):
        """Validate spare part code format."""
        if not self.code:
            raise ValueError("Code is required")
        if not self.code.isalnum():
            raise ValueError("Code must be alphanumeric")

    def _validate_name(self):
        """Validate spare part name."""
        if not self.name:
            raise ValueError("Name is required")

    def _validate_part_number(self):
        """Validate part number format."""
        if not self.part_number:
            raise ValueError("Part number is required")
        if not self.part_number.isalnum():
            raise ValueError("Part number must be alphanumeric")

    def _validate_price(self):
        """Validate pricing information."""
        if self.base_price < 0:
            raise ValueError("Base price cannot be negative")
        if self.price_breaks:
            for quantity, price in self.price_breaks.items():
                if float(quantity) < 0:
                    raise ValueError(
                        f"Price break quantity cannot be negative: {quantity}"
                    )
                if price < 0:
                    raise ValueError(f"Price break value cannot be negative: {price}")

    def _validate_stock(self):
        """Validate stock levels."""
        if self.current_stock < 0:
            raise ValueError("Current stock cannot be negative")
        if self.minimum_stock < 0:
            raise ValueError("Minimum stock cannot be negative")
        if self.reorder_point < 0:
            raise ValueError("Reorder point cannot be negative")
        if self.reorder_quantity < 0:
            raise ValueError("Reorder quantity cannot be negative")
        if self.lead_time_days < 0:
            raise ValueError("Lead time cannot be negative")

    def is_compatible_with_model(self, model_number: str) -> bool:
        """Check if spare part is compatible with a product model."""
        return model_number in self.compatible_models

    def is_compatible_with_product_family(self, family_code: str) -> bool:
        """Check if spare part is compatible with a product family."""
        return family_code in self.product_families

    def is_compatible_with_material(self, material_code: str) -> bool:
        """Check if spare part is compatible with a material."""
        return material_code in self.material_dependencies

    def calculate_price(self, quantity: int = 1) -> float:
        """Calculate price based on quantity and price breaks."""
        if not self.is_active:
            return 0.0

        if not self.price_breaks:
            return self.base_price * quantity

        # Sort break points in descending order
        sorted_breaks = sorted(
            [float(k) for k in self.price_breaks.keys()], reverse=True
        )

        # Find applicable break point
        for break_point in sorted_breaks:
            if quantity >= break_point:
                return self.price_breaks[str(break_point)] * quantity

        return self.base_price * quantity

    def needs_reorder(self) -> bool:
        """Check if part needs to be reordered."""
        return self.current_stock <= self.reorder_point

    def get_reorder_quantity(self) -> int:
        """Calculate quantity to reorder."""
        if self.needs_reorder():
            return max(self.reorder_quantity, self.minimum_stock - self.current_stock)
        return 0

    def update_stock(self, quantity: int, is_restock: bool = False):
        """Update stock levels and tracking information."""
        if is_restock:
            self.current_stock += quantity
            self.last_restock_date = datetime.utcnow()
            self.last_restock_quantity = quantity
        else:
            if quantity > self.current_stock:
                raise ValueError("Insufficient stock")
            self.current_stock -= quantity
            self.last_order_date = datetime.utcnow()
            self.last_order_quantity = quantity

    def get_specifications(self) -> dict:
        """Get technical specifications."""
        return {
            "specifications": self.specifications,
            "certifications": self.certifications,
            "operating_conditions": self.operating_conditions,
            "dimensions": self.dimensions,
            "weight": self.weight,
        }

    def get_inventory_status(self) -> dict:
        """Get current inventory status."""
        return {
            "current_stock": self.current_stock,
            "minimum_stock": self.minimum_stock,
            "reorder_point": self.reorder_point,
            "needs_reorder": self.needs_reorder(),
            "reorder_quantity": self.get_reorder_quantity(),
            "lead_time_days": self.lead_time_days,
            "last_restock_date": self.last_restock_date,
            "last_order_date": self.last_order_date,
        }


def init_spare_parts(db):
    """Initialize spare parts in the database."""
    parts = [
        {
            "code": "RTD-SENSOR",
            "name": "RTD Sensor Element",
            "description": "Replaceable RTD sensor element",
            "part_number": "SP-RTD-001",
            "part_type": "Sensor",
            "material": "Stainless Steel",
            "dimensions": {"diameter": "3mm", "length": "50mm"},
            "weight": 10.0,
            "compatible_models": ["RTD-100", "RTD-200", "RTD-300"],
            "product_families": ["RTD"],
            "material_dependencies": ["SS304", "SS316"],
            "current_stock": 100,
            "minimum_stock": 20,
            "reorder_point": 30,
            "reorder_quantity": 50,
            "lead_time_days": 14,
            "base_price": 25.00,
            "price_breaks": {"10": 23.00, "50": 20.00, "100": 18.00},
            "is_taxable": True,
            "specifications": {
                "resistance": "100 ohm",
                "tolerance": "0.1%",
                "temperature_range": "-200 to 600°C",
            },
            "certifications": ["UL", "CSA"],
            "operating_conditions": {
                "max_temperature": "600°C",
                "max_pressure": "1000 PSI",
            },
            "is_critical": True,
            "is_consumable": False,
        },
        {
            "code": "TC-CABLE",
            "name": "Thermocouple Extension Cable",
            "description": "High-temperature extension cable",
            "part_number": "SP-TC-001",
            "part_type": "Cable",
            "material": "Teflon",
            "dimensions": {"diameter": "5mm", "length": "10ft"},
            "weight": 200.0,
            "compatible_models": ["TC-100", "TC-200"],
            "product_families": ["TC"],
            "material_dependencies": ["TEFLON", "PVC"],
            "current_stock": 50,
            "minimum_stock": 10,
            "reorder_point": 15,
            "reorder_quantity": 25,
            "lead_time_days": 7,
            "base_price": 15.00,
            "price_breaks": {"5": 14.00, "20": 13.00, "50": 12.00},
            "is_taxable": True,
            "specifications": {
                "wire_gauge": "20 AWG",
                "insulation": "Teflon",
                "temperature_rating": "200°C",
            },
            "certifications": ["UL"],
            "operating_conditions": {
                "max_temperature": "200°C",
                "min_temperature": "-40°C",
            },
            "is_critical": False,
            "is_consumable": True,
        },
    ]

    for part_data in parts:
        part = SparePart(**part_data)
        db.add(part)

    db.commit()
