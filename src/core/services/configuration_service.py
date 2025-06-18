"""
Configuration service for managing product configurations.
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session

from src.core.models.configuration import Configuration
from src.core.models.connection_option import ConnectionOption
from src.core.models.material import Material
from src.core.models.option import Option
from src.core.models.standard_length import StandardLength
from src.core.models.voltage_option import VoltageOption
from src.core.services.product_service import ProductService

# Set up logging
logger = logging.getLogger(__name__)


class ConfigurationService:
    """
    Manages the business logic of configuring a product.
    This service is responsible for creating a configuration session,
    handling option selections, validating the configuration, and calculating the final price.
    """

    def __init__(self, db: Session, product_service: ProductService):
        self.db = db
        self.product_service = product_service
        self._current_config: Optional[Configuration] = None
        logger.debug("ConfigurationService initialized")

    @property
    def current_config(self) -> Optional[Configuration]:
        """Get the current configuration."""
        return self._current_config

    @current_config.setter
    def current_config(self, value: Optional[Configuration]):
        """Set the current configuration."""
        self._current_config = value
        if value:
            logger.debug(
                f"Current configuration set for product family: {value.product_family_name}"
            )
        else:
            logger.debug("Current configuration cleared")

    def start_configuration(
        self, product_family_id: int, product_family_name: str, base_product_info: dict
    ):
        """
        Start a new configuration session for a product family.

        Args:
            product_family_id: ID of the product family
            product_family_name: Name of the product family
            base_product_info: Base product information
        """
        logger.debug(
            f"Starting configuration for {product_family_name} (ID: {product_family_id})"
        )
        logger.debug(f"Base product info: {base_product_info}")

        try:
            self._current_config = Configuration(
                db=self.db,
                product_family_id=product_family_id,
                product_family_name=product_family_name,
                base_product=base_product_info,
            )
            logger.debug("Configuration object created successfully")

            # Update price and model number
            self._update_price()
            self._update_model_number()

        except Exception as e:
            logger.error(f"Error creating configuration: {e!s}", exc_info=True)
            raise

    def select_option(self, option_name: str, value: any):
        """
        Updates the current configuration with a selected option.

        Args:
            option_name (str): The name of the option (e.g., "Material", "Length").
            value (any): The selected value for the option.
        """
        if not self.current_config:
            logger.warning("No current configuration when trying to select option")
            return

        logger.debug(f"Selecting option: {option_name} = {value}")

        # Update the selected option
        self.current_config.selected_options[option_name] = value

        # Update the model number and price
        self._update_model_number()
        self._update_price()
        logger.debug(f"Updated configuration: {self.current_config.selected_options}")

    def _update_model_number(self):
        """Update the model number based on selected options."""
        if not self.current_config:
            logger.warning(
                "No current configuration when trying to update model number"
            )
            return

        logger.debug("Updating model number")
        self.current_config.model_number = self.generate_model_number()

    def _get_current_variant(self):
        """Get the current product variant based on selected options."""
        if not self.current_config:
            logger.warning("No current configuration when trying to get variant")
            return None

        try:
            # Find the specific variant that matches the current selection
            variant = self.product_service.find_variant(
                self.db,
                self.current_config.product_family_id,
                self.current_config.selected_options,
            )

            if not variant:
                logger.warning(
                    f"No matching variant found for options: {self.current_config.selected_options}"
                )
                return None

            return variant

        except Exception as e:
            logger.error(f"Error getting current variant: {e!s}", exc_info=True)
            return None

    def _update_price(self):
        """Update the price based on the current configuration."""
        try:
            variant = self._get_current_variant()
            if not variant:
                logger.error("No variant found for current configuration")
                # Fallback to base product price
                base_price = self._to_float(
                    self.current_config.base_product.get("base_price", 0.0)
                )
                if base_price == 0.0:
                    base_price = 500.0
                self.current_config.final_price = base_price
                self.current_config.model_number = ""
                logger.info(f"Using fallback base price: {base_price}")
                return

            # Start with the variant's base price
            final_price = self._to_float(getattr(variant, "base_price", 0.0))
            if final_price == 0.0:
                final_price = self._to_float(
                    self.current_config.base_product.get("base_price", 0.0)
                )
            logger.info(f"Base price from variant: {final_price}")

            # Add material price
            material_name = self.current_config.selected_options.get("Material")
            if material_name:
                material = self.db.query(Material).filter_by(name=material_name).first()
                if material:
                    final_price += material.base_price
                    logger.debug(f"Added material base price: {material.base_price}")

            # Add voltage price
            voltage_name = self.current_config.selected_options.get("Voltage")
            if voltage_name:
                voltage = (
                    self.db.query(VoltageOption).filter_by(name=voltage_name).first()
                )
            if voltage:
                final_price += voltage.price
                logger.debug(f"Added voltage price: {voltage.price}")

            # Add connection price
            connection_name = self.current_config.selected_options.get("Connection")
            if connection_name:
                connection = (
                    self.db.query(ConnectionOption)
                    .filter_by(name=connection_name)
                    .first()
                )
                if connection:
                    final_price += connection.price
                    logger.debug(f"Added connection price: {connection.price}")

            # Add length price
            length = self._to_float(self.current_config.selected_options.get("Length"))
            if length and material:
                standard_length = (
                    self.db.query(StandardLength)
                    .filter_by(material_id=material.id, length=length)
                    .first()
                )
                if standard_length:
                    final_price += standard_length.price
                    logger.debug(f"Added length price: {standard_length.price}")

            # Add miscellaneous options prices
            for (
                option_name,
                option_value,
            ) in self.current_config.selected_options.items():
                if option_name not in ["Material", "Voltage", "Connection", "Length"]:
                    option = (
                        self.db.query(Option)
                        .filter_by(
                            product_family_id=self.current_config.product_family_id,
                            name=option_name,
                            value=option_value,
                        )
                        .first()
                    )
                    if option:
                        final_price += option.price
                        logger.debug(f"Added {option_name} price: {option.price}")

            # Update the final price
            self.current_config.final_price = final_price
            logger.info(f"Final price calculated: {final_price}")

        except Exception as e:
            logger.error(f"Error updating price: {e!s}", exc_info=True)
            # Set a fallback price
            self.current_config.final_price = 500.0

    def _to_float(self, value, default=0.0):
        """Convert value to float, handling various types."""
        try:
            if value is None:
                return default
            return float(value)
        except (TypeError, ValueError):
            return default

    def generate_model_number(self) -> str:
        """Generates the model number based on the current configuration."""
        if not self.current_config:
            return ""

        config = self.current_config
        family = config.product_family_name

        # Get values from selected options, falling back to base product values
        voltage = config.selected_options.get(
            "Voltage", config.base_product.get("voltage")
        )
        material = config.selected_options.get(
            "Material", config.base_product.get("material")
        )
        length = config.selected_options.get(
            "Length", config.base_product.get("base_length")
        )

        # Format the length to remove decimals if it's a whole number
        try:
            length_val = float(length)
            length_str = (
                f'{int(length_val)}"' if length_val.is_integer() else f'{length_val}"'
            )
        except (ValueError, TypeError):
            length_str = f'{length}"' if length else 'LENGTH"'

        return f"{family}-{voltage}-{material}-{length_str}"

    def get_final_description(self) -> str:
        """
        Generates a final description based on the selected options.
        """
        if not self.current_config:
            return ""

        # Basic description, can be expanded
        desc = f"{self.current_config.product_family_name} with:"
        for name, value in self.current_config.selected_options.items():
            if value:
                desc += f" {name}: {value},"

        return desc.strip(",")

    def add_non_standard_length_adder(self):
        """Add the non-standard length surcharge to the configuration."""
        if not self.current_config:
            return

        # Add the non-standard length surcharge
        self.current_config.selected_options["NonStandardLengthSurcharge"] = True
        self.current_config.final_price = self.calculate_price()

    def remove_non_standard_length_adder(self):
        """Remove the non-standard length surcharge from the configuration."""
        if not self.current_config:
            return

        # Remove the non-standard length surcharge
        self.current_config.selected_options.pop("NonStandardLengthSurcharge", None)
        self.current_config.final_price = self.calculate_price()

    # More methods will be added here to handle validation, etc.
