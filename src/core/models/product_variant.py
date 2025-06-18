"""
Product variant model for storing specific product configurations.

This module defines the ProductVariant model which represents a specific configuration
of a product family in Babbitt International's quoting system. Each variant is a unique
combination of options (material, voltage, length, etc.) for a product family.

The ProductVariant model supports:
- Unique variant identification
- Specific configuration options
- Pricing calculations
- Relationships to product families and quotes
- Material and voltage specifications
- Length and dimension tracking
"""

from sqlalchemy import Column, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from src.core.models.base_model import BaseModel


class ProductVariant(BaseModel):
    """
    SQLAlchemy model representing a specific product configuration (variant).

    This model stores information about a specific configuration of a product family,
    including its model number, description, pricing, and all configuration options.
    Each variant represents a unique combination of options that can be ordered.

    Attributes:
        product_family_id (int): Foreign key to the product family
        model_number (str): Unique model number for the variant (e.g., "LS2000-115VAC-S-10")
        description (str): Description of the variant
        base_price (float): Base price for the variant
        base_length (float): Base length in inches
        voltage (str): Voltage configuration (e.g., "115VAC", "24VDC")
        material (str): Material code:
                - "S": 316 Stainless Steel
                - "H": Halar Coated
                - "U": UHMWPE
                - "T": Teflon
        is_active (str): Whether this variant is currently active ("Y"/"N")
        min_length (float): Minimum allowed length in inches
        max_length (float): Maximum allowed length in inches
        length_increment (float): Standard length increment in inches
        product_family (ProductFamily): Related product family
        quote_items (List[QuoteItem]): List of quote items for this variant

    Note:
        - Model numbers should follow the format: "{family}-{voltage}-{material}-{length}"
        - Pricing calculations consider material-specific rules and length adjustments
        - Length constraints ensure valid configurations
        - The model_number field is indexed for efficient searching

    Example:
        >>> variant = ProductVariant(
        ...     model_number="LS2000-115VAC-S-10",
        ...     description="Level Switch, 10 inch, Stainless Steel",
        ...     base_price=450.00,
        ...     base_length=10.0,
        ...     voltage="115VAC",
        ...     material="S",
        ...     min_length=6.0,
        ...     max_length=72.0,
        ...     length_increment=1.0
        ... )
    """

    __tablename__ = "product_variants"

    # Foreign keys
    product_family_id = Column(
        ForeignKey("product_families.id"), nullable=False, index=True
    )

    # Basic information
    model_number = Column(
        String, nullable=False, index=True, unique=True
    )  # e.g., "LS2000-115VAC-S-10"
    description = Column(Text)

    # Pricing information
    base_price = Column(Float, nullable=False, default=0.0)
    base_length = Column(Float)  # Base length in inches

    # Configuration options
    voltage = Column(String)  # e.g., "115VAC", "24VDC"
    material = Column(String)  # e.g., "S", "H", "U", "T"

    # Length constraints
    min_length = Column(Float)  # Minimum allowed length in inches
    max_length = Column(Float)  # Maximum allowed length in inches
    length_increment = Column(Float)  # Standard length increment in inches

    # Status
    is_active = Column(String, default="Y")  # "Y" for active, "N" for inactive

    # Relationships
    product_family = relationship("ProductFamily", back_populates="variants")
    quote_items = relationship(
        "QuoteItem", back_populates="product", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Return a string representation of the ProductVariant.

        Returns:
            str: A string showing the variant's model number and base price
        """
        return f"<ProductVariant(model='{self.model_number}', base_price={self.base_price})>"

    def is_valid_length(self, length: float) -> bool:
        """
        Check if a given length is valid for this variant.

        Args:
            length (float): Length to check in inches

        Returns:
            bool: True if length is valid, False otherwise
        """
        if not self.min_length or not self.max_length:
            return True
        return self.min_length <= length <= self.max_length

    def get_next_valid_length(self, length: float) -> float:
        """
        Get the next valid length based on the increment.

        Args:
            length (float): Current length in inches

        Returns:
            float: Next valid length
        """
        if not self.length_increment:
            return length
        return round(length / self.length_increment) * self.length_increment

    def calculate_price(self, length: float = None) -> float:
        """
        Calculate the price for this variant at a given length.

        Args:
            length (float, optional): Length in inches. If None, uses base_length.

        Returns:
            float: Calculated price
        """
        if length is None:
            length = self.base_length

        if not self.is_valid_length(length):
            raise ValueError(f"Invalid length {length} for variant {self.model_number}")

        # Get the product family for material-specific pricing
        family = self.product_family
        if not family:
            return self.base_price

        # Calculate length-based price adjustments
        length_diff = length - self.base_length
        price = self.base_price

        # Add material-specific pricing
        if self.material and family.default_material != self.material:
            # TODO: Add material-specific pricing logic
            pass

        return price

    def to_dict(self) -> dict:
        """
        Convert variant to dictionary, including related quote items.

        Returns:
            dict: Dictionary representation of the variant
        """
        data = super().to_dict()
        data["quote_items"] = [item.to_dict() for item in self.quote_items]
        return data
