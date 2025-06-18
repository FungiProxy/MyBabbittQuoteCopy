"""
Service for managing products and product configuration.

This module provides a service layer for managing Babbitt International products,
including product retrieval, configuration, pricing, and option management. It
implements business logic for:

- Product filtering and searching
- Material and voltage compatibility
- Product configuration and pricing
- Option management and compatibility
- Material management and availability
- Material pricing rules and compatibility
- Cable and enclosure management
- Electrical protection management

The service follows the Repository pattern and provides a clean interface
for interacting with product-related data and business rules.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from src.core.models import (
    Material,
    MaterialOption,
    Option,
    Product,
    ProductFamily,
    VoltageOption,
    Cable,
    Enclosure,
    ElectricalProtection,
    MaterialAvailability,
    StandardLength,
)
from src.core.models.connection_option import ConnectionOption
from src.core.models.product_variant import ProductVariant
from src.core.pricing import calculate_product_price
from src.utils.db_utils import get_all, get_by_id
from src.core.services.validation_service import ValidationService

# Set up logging
logger = logging.getLogger(__name__)


class ProductService:
    """
    Service class for managing Babbitt International products, configurations, and materials.

    This service provides methods for retrieving, configuring, and pricing products,
    as well as managing product options, materials, and voltages. It encapsulates
    all product and material-related business logic and data access.

    The service handles:
    - Product retrieval and configuration
    - Material management and compatibility
    - Voltage options and compatibility
    - Product options and pricing
    - Material-specific pricing rules
    - Length-based calculations
    - Cable and enclosure management
    - Electrical protection management

    Example:
        >>> db = SessionLocal()
        >>> service = ProductService(db)
        >>> # Product-related operations
        >>> products = service.get_products(material="S", category="Level Switch")
        >>> product, price = service.configure_product(product_id=1, length=24)
        >>>
        >>> # Material-related operations
        >>> materials = service.get_available_materials()
        >>> product_materials = service.get_available_materials_for_product("LS2000")
        >>> voltages = service.get_available_voltages("LS2000")
    """

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self.session = session
        self.validator = ValidationService(session)
        logger.debug("ProductService initialized")

    def get_products(
        self,
        material: Optional[str] = None,
        category: Optional[str] = None,
        voltage: Optional[str] = None,
        connection: Optional[str] = None,
        cable: Optional[str] = None,
        enclosure: Optional[str] = None,
        electrical_protection: Optional[str] = None,
    ) -> List[Product]:
        """
        Get products matching the specified criteria.

        Args:
            material: Optional material code to filter by
            category: Optional product category to filter by
            voltage: Optional voltage option to filter by
            connection: Optional connection type to filter by
            cable: Optional cable type to filter by
            enclosure: Optional enclosure type to filter by
            electrical_protection: Optional electrical protection type to filter by

        Returns:
            List[Product]: List of matching Product objects
        """
        try:
            query = self.session.query(Product)

            if material:
                query = query.filter(Product.material == material)
            if category:
                query = query.filter(Product.category == category)
            if voltage:
                query = query.filter(Product.voltage == voltage)
            if connection:
                query = query.filter(Product.connection == connection)
            if cable:
                query = query.filter(Product.cable == cable)
            if enclosure:
                query = query.filter(Product.enclosure == enclosure)
            if electrical_protection:
                query = query.filter(
                    Product.electrical_protection == electrical_protection
                )

            return query.all()
        except Exception as e:
            logger.error(f"Error getting products: {e!s}", exc_info=True)
            return []

    def get_available_materials(self) -> List[Material]:
        """Get all available materials."""
        try:
            return (
                self.session.query(Material)
                .join(MaterialAvailability)
                .filter(MaterialAvailability.is_available == True)
                .all()
            )
        except Exception as e:
            logger.error(f"Error getting available materials: {e!s}", exc_info=True)
            return []

    def get_available_materials_for_product(
        self, product_family: str
    ) -> List[Material]:
        """Get available materials for a specific product family."""
        try:
            return (
                self.session.query(Material)
                .join(MaterialAvailability)
                .filter(
                    MaterialAvailability.product_type == product_family,
                    MaterialAvailability.is_available == True,
                )
                .all()
            )
        except Exception as e:
            logger.error(
                f"Error getting available materials for product {product_family}: {e!s}",
                exc_info=True,
            )
            return []

    def get_available_voltages(self, product_family: str) -> List[VoltageOption]:
        """Get available voltage options for a product family."""
        try:
            return (
                self.session.query(VoltageOption)
                .filter(
                    VoltageOption.product_family_id == product_family,
                    VoltageOption.is_available == True,
                )
                .all()
            )
        except Exception as e:
            logger.error(
                f"Error getting available voltages for product {product_family}: {e!s}",
                exc_info=True,
            )
            return []

    def get_available_connections(self) -> List[ConnectionOption]:
        """Get all available connection options."""
        try:
            return (
                self.session.query(ConnectionOption)
                .filter(ConnectionOption.is_available == True)
                .all()
            )
        except Exception as e:
            logger.error(f"Error getting available connections: {e!s}", exc_info=True)
            return []

    def get_available_cables(self) -> List[Cable]:
        """Get all available cable types."""
        try:
            return self.session.query(Cable).filter(Cable.is_available == True).all()
        except Exception as e:
            logger.error(f"Error getting available cables: {e!s}", exc_info=True)
            return []

    def get_available_enclosures(self) -> List[Enclosure]:
        """Get all available enclosure types."""
        try:
            return (
                self.session.query(Enclosure)
                .filter(Enclosure.is_available == True)
                .all()
            )
        except Exception as e:
            logger.error(f"Error getting available enclosures: {e!s}", exc_info=True)
            return []

    def get_available_electrical_protection(self) -> List[ElectricalProtection]:
        """Get all available electrical protection types."""
        try:
            return (
                self.session.query(ElectricalProtection)
                .filter(ElectricalProtection.is_available == True)
                .all()
            )
        except Exception as e:
            logger.error(
                f"Error getting available electrical protection: {e!s}", exc_info=True
            )
            return []

    def configure_product(
        self,
        product_id: int,
        length: Optional[float] = None,
        material_override: Optional[str] = None,
        voltage: Optional[str] = None,
        connection: Optional[str] = None,
        cable: Optional[str] = None,
        enclosure: Optional[str] = None,
        electrical_protection: Optional[str] = None,
        options: Optional[Dict[str, str]] = None,
    ) -> Tuple[Optional[ProductVariant], Optional[float], Optional[str]]:
        """
        Configure a product with the specified options.

        Args:
            product_id: ID of the product to configure
            length: Optional length override
            material_override: Optional material code override
            voltage: Optional voltage override
            connection: Optional connection type override
            cable: Optional cable type override
            enclosure: Optional enclosure type override
            electrical_protection: Optional electrical protection type override
            options: Optional dictionary of additional options

        Returns:
            Tuple[Optional[ProductVariant], Optional[float], Optional[str]]:
            Tuple containing:
            - Configured product variant
            - Calculated price
            - Error message if any
        """
        try:
            # Get the base product
            product = (
                self.session.query(Product).filter(Product.id == product_id).first()
            )
            if not product:
                return None, None, f"Product with ID {product_id} not found"

            # Validate material if provided
            if material_override:
                material = (
                    self.session.query(Material)
                    .filter(Material.code == material_override)
                    .first()
                )
                if not material:
                    return None, None, f"Invalid material code: {material_override}"
                if not material.is_available_for_product(
                    product.model_number.split("-")[0]
                ):
                    return (
                        None,
                        None,
                        f"Material {material_override} not available for this product",
                    )

            # Validate length if provided
            if length is not None:
                if length <= 0:
                    return None, None, "Length must be greater than 0"
                if material_override:
                    material = (
                        self.session.query(Material)
                        .filter(Material.code == material_override)
                        .first()
                    )
                    if not material.is_standard_length(length):
                        return (
                            None,
                            None,
                            f"Length {length} is not a standard length for material {material_override}",
                        )

            # Create product variant
            variant = ProductVariant(
                product_id=product_id,
                length=length or product.base_length,
                material=material_override or product.material,
                voltage=voltage or product.voltage,
                connection=connection,
                cable=cable,
                enclosure=enclosure,
                electrical_protection=electrical_protection,
                options=options or {},
            )

            # Calculate price
            price = calculate_product_price(
                self.session,
                variant,
                length=length,
                material_override=material_override,
                voltage=voltage,
                connection=connection,
                cable=cable,
                enclosure=enclosure,
                electrical_protection=electrical_protection,
                options=options,
            )

            return variant, price, None

        except Exception as e:
            logger.error(f"Error configuring product: {e!s}", exc_info=True)
            return None, None, str(e)

    def search_products(self, query: str) -> List[Dict]:
        """Search for products by name or model number."""
        families = (
            self.session.query(ProductFamily)
            .filter(ProductFamily.name.ilike(f"%{query}%"))
            .all()
        )
        variants = (
            self.session.query(ProductVariant)
            .filter(ProductVariant.model_number.ilike(f"%{query}%"))
            .all()
        )
        results = []
        for f in families:
            results.append(
                {
                    "id": f.id,
                    "name": f.name,
                    "description": f.description,
                    "category": f.category,
                    "type": "family",
                }
            )
        for v in variants:
            results.append(
                {
                    "id": v.id,
                    "model_number": v.model_number,
                    "description": v.description,
                    "base_price": v.base_price,
                    "type": "variant",
                }
            )
        return results

    def get_variant_by_id(self, variant_id: int) -> Optional[Dict]:
        """Get a variant by its ID."""
        variant = (
            self.session.query(ProductVariant)
            .filter(ProductVariant.id == variant_id)
            .first()
        )
        if not variant:
            return None
        return {
            "id": variant.id,
            "model_number": variant.model_number,
            "description": variant.description,
            "base_price": variant.base_price,
        }

    def get_product_families(self) -> List[Dict]:
        """Get all product families."""
        families = self.session.query(ProductFamily).all()
        return [
            {
                "id": f.id,
                "name": f.name,
                "description": f.description,
                "category": f.category,
            }
            for f in families
        ]

    def get_variants_for_family(self, family_id: int) -> List[Dict]:
        """Get all variants for a product family."""
        variants = (
            self.session.query(ProductVariant)
            .filter(ProductVariant.product_family_id == family_id)
            .all()
        )
        return [
            {
                "id": v.id,
                "model_number": v.model_number,
                "description": v.description,
                "base_price": v.base_price,
            }
            for v in variants
        ]

    def get_material_options(self, product_family_id: int) -> List[Dict]:
        """Get material options for a product family."""
        options = (
            self.session.query(MaterialOption)
            .filter(
                MaterialOption.product_family_id == product_family_id,
                MaterialOption.is_available == 1,
            )
            .all()
        )
        return [
            {
                "material_code": o.material_code,
                "display_name": o.display_name,
                "base_price": o.base_price,
            }
            for o in options
        ]

    def get_voltage_options(self, product_family_id: int) -> List[Dict]:
        """Get voltage options for a product family."""
        options = (
            self.session.query(VoltageOption)
            .filter(
                VoltageOption.product_family_id == product_family_id,
                VoltageOption.is_available == 1,
            )
            .all()
        )
        return [{"voltage": o.voltage, "is_available": o.is_available} for o in options]

    def get_connection_options(self, product_family_id: int) -> List[Dict]:
        """Get connection options for a product family."""
        options = (
            self.session.query(ConnectionOption)
            .filter(ConnectionOption.product_family_id == product_family_id)
            .all()
        )
        return [
            {
                "code": o.code,
                "name": o.name,
                "connection_type": o.connection_type,
                "rating": o.rating,
                "size": o.size,
                "price": o.price,
            }
            for o in options
        ]

    def get_additional_options(self, product_family: str) -> List[Dict]:
        """Get additional options for a product family."""
        options = (
            self.session.query(Option)
            .filter(Option.product_families.like(f"%{product_family}%"))
            .all()
        )
        return [
            {
                "name": o.name,
                "description": o.description,
                "price": o.price,
                "price_type": o.price_type,
                "category": o.category,
            }
            for o in options
        ]

    def get_valid_options_for_selection(
        self, family_id: int, selected_options: dict
    ) -> dict:
        """Get valid options for selection based on current selections."""
        try:
            # Get all options for the family
            options = (
                self.session.query(Option)
                .filter(Option.product_family_id == family_id)
                .all()
            )

            # Filter options based on compatibility
            valid_options = {}
            for option in options:
                if option.is_compatible_with(selected_options):
                    valid_options[option.name] = option.choices

            return valid_options
        except Exception as e:
            logger.error(f"Error getting valid options: {e!s}", exc_info=True)
            return {}

    def get_standard_lengths(self, product_family: str) -> List[int]:
        """Get standard lengths for a product family."""
        try:
            lengths = (
                self.session.query(StandardLength)
                .join(Material)
                .filter(Material.product_family == product_family)
                .all()
            )
            return [length.length for length in lengths]
        except Exception as e:
            logger.error(f"Error getting standard lengths: {e!s}", exc_info=True)
            return []

    def validate_length(
        self, product_family: str, material_code: str, length: float
    ) -> Tuple[bool, str]:
        """Validate a length for a product family and material."""
        try:
            # Get material
            material = (
                self.session.query(Material)
                .filter(Material.code == material_code)
                .first()
            )
            if not material:
                return False, f"Material {material_code} not found"

            # Check minimum length
            if length < material.min_length:
                return (
                    False,
                    f"Length {length} is less than minimum {material.min_length}",
                )

            # Check standard lengths
            standard_lengths = (
                self.session.query(StandardLength)
                .filter(
                    StandardLength.material_code == material_code,
                    StandardLength.product_family == product_family,
                )
                .all()
            )

            # If no standard lengths, any length is valid
            if not standard_lengths:
                return True, ""

            # Check if length is within tolerance of any standard length
            for std_length in standard_lengths:
                if abs(length - std_length.length) <= std_length.tolerance:
                    return True, ""

            return False, f"Length {length} is not a standard length"
        except Exception as e:
            logger.error(f"Error validating length: {e!s}", exc_info=True)
            return False, f"Error validating length: {str(e)}"
