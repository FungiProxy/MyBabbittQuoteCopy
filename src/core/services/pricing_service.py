"""
Service for managing product pricing.

This module provides a service layer for managing product pricing in Babbitt International's
quoting system. It implements business logic for:

- Base price calculations
- Material pricing
- Length-based pricing
- Option pricing
- Special pricing rules
- Price validation

The service follows domain-driven design principles and separates business logic
from data access, providing a clean interface for pricing operations.
"""

import logging
from typing import Dict, Optional

from sqlalchemy.orm import Session

from src.core.models.material import Material
from src.core.models.option import Option
from src.core.models.standard_length import StandardLength
from src.core.models.voltage_option import VoltageOption
from src.core.models.connection_option import ConnectionOption
from src.core.models.product_family import ProductFamily

# Set up logging
logger = logging.getLogger(__name__)


class PricingService:
    """
    Service class for managing product pricing.

    This service provides methods for calculating prices based on various factors
    such as materials, lengths, options, and special pricing rules. It encapsulates
    all pricing-related business logic and data access.

    Example:
        >>> db = SessionLocal()
        >>> pricing_service = PricingService(db)
        >>> price = pricing_service.calculate_price(
        ...     product_family_id=1,
        ...     material="316SS",
        ...     length=24.0,
        ...     voltage="115VAC",
        ...     connection="1/2\" NPT"
        ... )
    """

    def __init__(self, db: Session):
        self.db = db
        logger.debug("PricingService initialized")

    def calculate_price(
        self,
        product_family_id: int,
        material: str,
        length: float,
        voltage: Optional[str] = None,
        connection: Optional[str] = None,
        options: Optional[Dict[str, str]] = None,
    ) -> float:
        """
        Calculate the total price for a product configuration.

        Args:
            product_family_id: ID of the product family
            material: Material name (e.g., "316SS", "Hastelloy C")
            length: Length in inches
            voltage: Optional voltage option
            connection: Optional connection type
            options: Optional dictionary of additional options

        Returns:
            float: Total calculated price
        """
        try:
            # Start with base price from product family
            base_price = self._get_base_price(product_family_id)
            logger.debug(f"Base price: {base_price}")

            # Add material price
            material_price = self._get_material_price(material)
            base_price += material_price
            logger.debug(f"Material price: {material_price}")

            # Add length price
            length_price = self._get_length_price(material, length)
            base_price += length_price
            logger.debug(f"Length price: {length_price}")

            # Add voltage price if specified
            if voltage:
                voltage_price = self._get_voltage_price(voltage)
                base_price += voltage_price
                logger.debug(f"Voltage price: {voltage_price}")

            # Add connection price if specified
            if connection:
                connection_price = self._get_connection_price(connection)
                base_price += connection_price
                logger.debug(f"Connection price: {connection_price}")

            # Add option prices if specified
            if options:
                for option_name, option_value in options.items():
                    option_price = self._get_option_price(
                        product_family_id, option_name, option_value
                    )
                    base_price += option_price
                    logger.debug(f"Option {option_name} price: {option_price}")

            logger.info(f"Final calculated price: {base_price}")
            return base_price

        except Exception as e:
            logger.error(f"Error calculating price: {e!s}", exc_info=True)
            return 0.0

    def _get_base_price(self, product_family_id: int) -> float:
        """Get the base price for a product family."""
        try:
            # Query the product family's base price
            product_family = self.db.query(ProductFamily).get(product_family_id)
            if not product_family:
                logger.warning(f"Product family {product_family_id} not found")
                return 500.0  # Default base price
            return float(product_family.base_price)
        except Exception as e:
            logger.error(f"Error getting base price: {e!s}", exc_info=True)
            return 500.0

    def _get_material_price(self, material: str) -> float:
        """Get the price for a material."""
        try:
            material_obj = self.db.query(Material).filter_by(name=material).first()
            if not material_obj:
                logger.warning(f"Material {material} not found")
                return 0.0
            return float(material_obj.base_price)
        except Exception as e:
            logger.error(f"Error getting material price: {e!s}", exc_info=True)
            return 0.0

    def _get_length_price(self, material: str, length: float) -> float:
        """Get the price for a specific length and material combination."""
        try:
            material_obj = self.db.query(Material).filter_by(name=material).first()
            if not material_obj:
                logger.warning(f"Material {material} not found")
                return 0.0

            standard_length = (
                self.db.query(StandardLength)
                .filter_by(material_id=material_obj.id, length=length)
                .first()
            )

            if not standard_length:
                logger.warning(f'No standard length found for {material} at {length}"')
                return 0.0

            return float(standard_length.price)
        except Exception as e:
            logger.error(f"Error getting length price: {e!s}", exc_info=True)
            return 0.0

    def _get_voltage_price(self, voltage: str) -> float:
        """Get the price for a voltage option."""
        try:
            voltage_obj = self.db.query(VoltageOption).filter_by(name=voltage).first()
            if not voltage_obj:
                logger.warning(f"Voltage {voltage} not found")
                return 0.0
            return float(voltage_obj.price)
        except Exception as e:
            logger.error(f"Error getting voltage price: {e!s}", exc_info=True)
            return 0.0

    def _get_connection_price(self, connection: str) -> float:
        """Get the price for a connection option."""
        try:
            connection_obj = (
                self.db.query(ConnectionOption).filter_by(name=connection).first()
            )
            if not connection_obj:
                logger.warning(f"Connection {connection} not found")
                return 0.0
            return float(connection_obj.price)
        except Exception as e:
            logger.error(f"Error getting connection price: {e!s}", exc_info=True)
            return 0.0

    def _get_option_price(
        self, product_family_id: int, option_name: str, option_value: str
    ) -> float:
        """Get the price for a specific option."""
        try:
            option = (
                self.db.query(Option)
                .filter_by(
                    product_family_id=product_family_id,
                    name=option_name,
                    value=option_value,
                )
                .first()
            )

            if not option:
                logger.warning(
                    f"Option {option_name}={option_value} not found for product family {product_family_id}"
                )
                return 0.0

            return float(option.price)
        except Exception as e:
            logger.error(f"Error getting option price: {e!s}", exc_info=True)
            return 0.0
