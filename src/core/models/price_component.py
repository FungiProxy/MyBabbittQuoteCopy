from sqlalchemy import (
    Column,
    String,
    Float,
    Boolean,
    JSON,
    Integer,
    ForeignKey,
    Text,
    Enum,
)
from sqlalchemy.orm import relationship
from .base_model import BaseModel
import enum


class PriceType(enum.Enum):
    """Enum for different types of price components."""

    FIXED = "fixed"
    PER_UNIT = "per_unit"
    PERCENTAGE = "percentage"
    QUANTITY_BASED = "quantity_based"
    LENGTH_BASED = "length_based"
    VOLUME_BASED = "volume_based"
    WEIGHT_BASED = "weight_based"
    CONDITIONAL = "conditional"


class PriceComponent(BaseModel):
    """Model for price components and their calculation rules."""

    __tablename__ = "price_components"

    # Basic Information
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    # Price Configuration
    price_type = Column(Enum(PriceType), nullable=False)
    base_value = Column(Float, nullable=False)
    min_value = Column(Float)
    max_value = Column(Float)
    unit = Column(String(20))  # e.g., "USD", "EUR", "per foot", "per unit"

    # Calculation Rules
    calculation_rules = Column(JSON, default=dict)  # Rules for price calculation
    quantity_breaks = Column(JSON, default=dict)  # Quantity-based pricing breaks
    length_breaks = Column(JSON, default=dict)  # Length-based pricing breaks
    volume_breaks = Column(JSON, default=dict)  # Volume-based pricing breaks
    weight_breaks = Column(JSON, default=dict)  # Weight-based pricing breaks

    # Conditions and Dependencies
    conditions = Column(JSON, default=dict)  # Conditions for applying the price
    dependencies = Column(JSON, default=dict)  # Dependencies on other components
    exclusions = Column(JSON, default=dict)  # Exclusions and conflicts

    # Compatibility
    product_families = Column(JSON, default=list)  # Compatible product families
    material_dependencies = Column(JSON, default=list)  # Compatible materials
    option_dependencies = Column(JSON, default=list)  # Compatible options

    # Additional Properties
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    is_required = Column(Boolean, default=False)
    is_taxable = Column(Boolean, default=True)

    # Validation Rules
    validation_rules = Column(JSON, default=dict)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_attributes()

    def _validate_attributes(self):
        """Validate all attributes according to rules."""
        self._validate_code()
        self._validate_name()
        self._validate_price()
        self._validate_breaks()

    def _validate_code(self):
        """Validate price component code format."""
        if not self.code:
            raise ValueError("Code is required")
        if not self.code.isalnum():
            raise ValueError("Code must be alphanumeric")

    def _validate_name(self):
        """Validate price component name."""
        if not self.name:
            raise ValueError("Name is required")

    def _validate_price(self):
        """Validate price values."""
        if self.base_value < 0:
            raise ValueError("Base value cannot be negative")
        if self.min_value is not None and self.min_value < 0:
            raise ValueError("Minimum value cannot be negative")
        if self.max_value is not None and self.max_value < 0:
            raise ValueError("Maximum value cannot be negative")
        if (
            self.min_value is not None
            and self.max_value is not None
            and self.min_value > self.max_value
        ):
            raise ValueError("Minimum value cannot be greater than maximum value")

    def _validate_breaks(self):
        """Validate pricing breaks."""
        for break_type in [
            "quantity_breaks",
            "length_breaks",
            "volume_breaks",
            "weight_breaks",
        ]:
            breaks = getattr(self, break_type)
            if breaks:
                for threshold, value in breaks.items():
                    if float(threshold) < 0:
                        raise ValueError(
                            f"Break threshold cannot be negative: {threshold}"
                        )
                    if value < 0:
                        raise ValueError(f"Break value cannot be negative: {value}")

    def calculate_price(
        self,
        quantity: float = 1.0,
        length: float = None,
        volume: float = None,
        weight: float = None,
    ) -> float:
        """Calculate price based on component type and parameters."""
        if not self.is_active:
            return 0.0

        if self.price_type == PriceType.FIXED:
            return self.base_value

        elif self.price_type == PriceType.PER_UNIT:
            return self.base_value * quantity

        elif self.price_type == PriceType.PERCENTAGE:
            return self.base_value / 100.0

        elif self.price_type == PriceType.QUANTITY_BASED:
            return self._calculate_break_price(quantity, self.quantity_breaks)

        elif self.price_type == PriceType.LENGTH_BASED and length is not None:
            return self._calculate_break_price(length, self.length_breaks)

        elif self.price_type == PriceType.VOLUME_BASED and volume is not None:
            return self._calculate_break_price(volume, self.volume_breaks)

        elif self.price_type == PriceType.WEIGHT_BASED and weight is not None:
            return self._calculate_break_price(weight, self.weight_breaks)

        elif self.price_type == PriceType.CONDITIONAL:
            return self._calculate_conditional_price(quantity, length, volume, weight)

        return 0.0

    def _calculate_break_price(self, value: float, breaks: dict) -> float:
        """Calculate price based on break points."""
        if not breaks:
            return self.base_value * value

        # Sort break points in descending order
        sorted_breaks = sorted([float(k) for k in breaks.keys()], reverse=True)

        # Find applicable break point
        for break_point in sorted_breaks:
            if value >= break_point:
                return breaks[str(break_point)] * value

        return self.base_value * value

    def _calculate_conditional_price(
        self, quantity: float, length: float, volume: float, weight: float
    ) -> float:
        """Calculate price based on conditions."""
        if not self.conditions:
            return self.base_value

        # Evaluate conditions and return appropriate price
        for condition, price in self.conditions.items():
            if self._evaluate_condition(condition, quantity, length, volume, weight):
                return price

        return self.base_value

    def _evaluate_condition(
        self,
        condition: str,
        quantity: float,
        length: float,
        volume: float,
        weight: float,
    ) -> bool:
        """Evaluate a condition string."""
        # This is a simplified implementation
        # In a real system, you would use a proper condition parser
        try:
            # Replace variables with actual values
            condition = condition.replace("quantity", str(quantity))
            if length is not None:
                condition = condition.replace("length", str(length))
            if volume is not None:
                condition = condition.replace("volume", str(volume))
            if weight is not None:
                condition = condition.replace("weight", str(weight))

            return eval(condition)
        except:
            return False

    def is_compatible_with_material(self, material_code: str) -> bool:
        """Check if price component is compatible with a material."""
        return material_code in self.material_dependencies

    def is_compatible_with_product_family(self, family_code: str) -> bool:
        """Check if price component is compatible with a product family."""
        return family_code in self.product_families

    def is_compatible_with_option(self, option_code: str) -> bool:
        """Check if price component is compatible with an option."""
        return option_code in self.option_dependencies

    def get_break_points(self) -> dict:
        """Get all break points for the price component."""
        return {
            "quantity": self.quantity_breaks,
            "length": self.length_breaks,
            "volume": self.volume_breaks,
            "weight": self.weight_breaks,
        }

    def get_conditions(self) -> dict:
        """Get all conditions for the price component."""
        return self.conditions


def init_price_components(db):
    """Initialize price components in the database."""
    components = [
        {
            "code": "BASE",
            "name": "Base Price",
            "description": "Base price for the product",
            "price_type": PriceType.FIXED,
            "base_value": 100.00,
            "unit": "USD",
            "is_required": True,
            "is_taxable": True,
            "product_families": ["RTD", "TC", "PRESSURE"],
            "validation_rules": {"min_value": 0, "max_value": 10000},
        },
        {
            "code": "LENGTH",
            "name": "Length-based Price",
            "description": "Price based on product length",
            "price_type": PriceType.LENGTH_BASED,
            "base_value": 5.00,
            "unit": "USD per foot",
            "length_breaks": {"10": 4.50, "20": 4.00, "50": 3.50},
            "is_required": True,
            "is_taxable": True,
            "product_families": ["RTD", "TC"],
            "validation_rules": {"min_length": 1, "max_length": 100},
        },
        {
            "code": "QUANTITY",
            "name": "Quantity Discount",
            "description": "Quantity-based price breaks",
            "price_type": PriceType.QUANTITY_BASED,
            "base_value": 1.00,
            "unit": "USD per unit",
            "quantity_breaks": {"10": 0.95, "50": 0.90, "100": 0.85},
            "is_required": False,
            "is_taxable": True,
            "product_families": ["RTD", "TC", "PRESSURE"],
            "validation_rules": {"min_quantity": 1, "max_quantity": 1000},
        },
        {
            "code": "MATERIAL",
            "name": "Material Premium",
            "description": "Price adjustment for special materials",
            "price_type": PriceType.PERCENTAGE,
            "base_value": 15.00,  # 15% premium
            "unit": "percent",
            "is_required": False,
            "is_taxable": True,
            "material_dependencies": ["SS316", "HASTELLOY", "TITANIUM"],
            "validation_rules": {"min_value": 0, "max_value": 100},
        },
    ]

    for component_data in components:
        component = PriceComponent(**component_data)
        db.add(component)

    db.commit()
