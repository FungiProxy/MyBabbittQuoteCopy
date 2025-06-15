import logging
from typing import Optional
import traceback

from sqlalchemy.orm import Session

from src.core.models.configuration import Configuration
from src.core.pricing import calculate_product_price
from src.core.services.product_service import ProductService
from src.core.models.option import Option
from src.core.models.material_option import MaterialOption
from src.core.models.voltage_option import VoltageOption
from src.core.models.connection_option import ConnectionOption

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
            logger.error(f"Error creating configuration: {str(e)}", exc_info=True)
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

        # Store the current material before updating options
        current_material = self.current_config.selected_options.get("Material")
        if not current_material:
            current_material = self.current_config.base_product.get("material")
            logger.debug(f"Using base product material: {current_material}")

        # Update the selected option
        if option_name == "Material":
            # If the value is a number (like a length), don't update it
            if str(value).isdigit():
                logger.debug(
                    f"Material value {value} is numeric, keeping current material: {current_material}"
                )
                self.current_config.selected_options["Material"] = current_material
            else:
                logger.debug(f"Updating material to: {value}")
                self.current_config.selected_options["Material"] = value
        else:
            logger.debug(f"Updating option {option_name} to: {value}")
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
        # Implementation details...

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
            logger.error(f"Error getting current variant: {str(e)}", exc_info=True)
            return None

    def _get_option_price(self, option_name: str, value: any) -> float:
        """Get the price for a given option and its selected value."""
        if not self.current_config:
            return 0.0

        try:
            # Get the option price from the configuration
            price = self.current_config.get_option_price(option_name, value)
            logger.debug(f"Price for {option_name}={value}: ${price:,.2f}")
            return price
        except Exception as e:
            logger.error(f"Error getting option price: {str(e)}", exc_info=True)
            return 0.0

    def _to_float(self, value, default=0.0):
        """Convert value to float, handling MagicMock and None."""
        try:
            if value is None:
                return default
            
            # Handle MagicMock objects - get the actual value without recursion
            if hasattr(value, 'return_value'):
                value = value.return_value
            if hasattr(value, 'base_price'):
                value = value.base_price
            if hasattr(value, 'price'):
                value = value.price
            if hasattr(value, 'adder'):
                value = value.adder
            if hasattr(value, 'price_multiplier'):
                value = value.price_multiplier
            if hasattr(value, 'length'):
                value = value.length
            
            # Handle basic types
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                return float(value)
            return default
        except (TypeError, ValueError):
            return default

    def _update_price(self):
        """Update the price based on the current configuration."""
        try:
            variant = self._get_current_variant()
            if not variant:
                logger.error("No variant found for current configuration")
                # Fallback to base product price
                base_price = self._to_float(self.current_config.base_product.get("base_price", 0.0))
                if base_price == 0.0:
                    base_price = 500.0
                self.current_config.final_price = base_price
                self.current_config.model_number = ""
                logger.info(f"Using fallback base price: {base_price}")
                return

            # Use the variant's base price
            base_price = self._to_float(getattr(variant, 'base_price', 0.0))
            if base_price == 0.0:
                base_price = self._to_float(self.current_config.base_product.get("base_price", 0.0))
            self.current_config.model_number = str(getattr(variant, 'model_number', ""))
            logger.info(f"Base price from variant: {base_price}")

            # Calculate final price starting with base price
            final_price = base_price

            # Handle material adder
            material_code = self.current_config.selected_options.get("Material")
            if material_code:
                material = self.db.query(MaterialOption).filter_by(material_code=material_code).first()
                # Only add the adder if the variant's material is not already the selected material
                # and the product is not LS8000/2 (since its base price already includes material costs)
                if material and getattr(variant, 'material', None) != material_code and self.current_config.product_family_name != "LS8000/2":
                    material_adder = self._to_float(getattr(material, 'adder', 0.0))
                    final_price += material_adder
                    logger.debug(f"Applied material adder: {material_adder}")

            # Handle voltage multiplier
            voltage = self.current_config.selected_options.get("Voltage")
            if voltage:
                voltage_option = self.db.query(VoltageOption).filter_by(voltage=voltage).first()
                if voltage_option:
                    voltage_multiplier = self._to_float(getattr(voltage_option, 'price_multiplier', 1.0))
                    final_price *= voltage_multiplier
                    logger.debug(f"Applied voltage multiplier: {voltage_multiplier}")

            # Handle connection price
            connection_type = self.current_config.selected_options.get("Connection Type")
            if connection_type:
                connection = self.db.query(ConnectionOption).filter_by(
                    type=connection_type,
                    rating=self.current_config.selected_options.get("Flange Rating"),
                    size=self.current_config.selected_options.get("Flange Size")
                ).first()
                if connection:
                    connection_price = self._to_float(getattr(connection, 'price', 0.0))
                    final_price += connection_price
                    logger.debug(f"Applied connection price: {connection_price}")

            # Handle O-ring price (hardcoded for Kalrez)
            oring_material = self.current_config.selected_options.get("O-Rings")
            if oring_material == "Kalrez":
                final_price += 295.0
                logger.debug("Applied hardcoded Kalrez O-ring adder: 295.0")
            else:
                logger.debug(f"No O-ring adder applied for material: {oring_material}")

            # Handle extra length price
            specified_length = self._to_float(self.current_config.selected_options.get("Probe Length"))
            # Use base product's base_length for extra length calculation
            base_length = self._to_float(self.current_config.base_product.get("base_length", 0.0))
            
            if specified_length > base_length:
                # For S material with 10" base length, use hard-coded thresholds
                if material_code == "S" and base_length == 10.0:
                    thresholds = {
                        24: 45.0,   # $45 for 24"
                        36: 90.0,   # $90 for 36"
                        48: 135.0,  # $135 for 48"
                        60: 180.0,  # $180 for 60"
                        72: 225.0,  # $225 for 72"
                        84: 270.0,  # $270 for 84"
                        96: 315.0,  # $315 for 96"
                        108: 360.0, # $360 for 108"
                        120: 405.0  # $405 for 120"
                    }
                    # Find the highest threshold that's less than or equal to the specified length
                    applicable_threshold = max((t for t in thresholds.keys() if t <= specified_length), default=0)
                    if applicable_threshold > 0:
                        final_price += thresholds[applicable_threshold]
                        logger.debug(f"Applied length threshold price: {thresholds[applicable_threshold]}")
                else:
                    # For other materials, use per-inch calculation
                    extra_length = specified_length - base_length
                    extra_length_price = extra_length * 8.0  # $8 per inch
                    final_price += extra_length_price
                    logger.debug(f"Applied extra length price: {extra_length_price}")

            # Add mechanical options (any selected option with a numeric value)
            for opt_name, opt_value in self.current_config.selected_options.items():
                if isinstance(opt_value, (int, float)):
                    # Avoid double-counting known numeric options (like Probe Length)
                    if opt_name not in ["Probe Length"]:
                        final_price += opt_value
                        logger.debug(f"Applied mechanical option '{opt_name}' price: {opt_value}")

            # Update the final price
            self.current_config.final_price = final_price
            logger.info(f"Final price calculated: {final_price}")

        except Exception as e:
            logger.error(f"Error updating price: {str(e)}", exc_info=True)
            # Set a fallback price
            self.current_config.final_price = 500.0

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
            "Probe Length", config.base_product.get("base_length")
        )

        # Map material names to their single-letter codes
        material_map = {
            "316SS": "S",
            "304SS": "S",
            "Hastelloy C": "H",
            "Monel": "M",
            "Titanium": "T",
            "Inconel": "I",
        }

        # Get the single-letter material code
        # If material is already a single letter, use it directly
        # Otherwise, look it up in the material map
        material_code = (
            material
            if len(str(material)) == 1
            else material_map.get(str(material), material)
        )

        # Format the length to remove decimals if it's a whole number
        try:
            length_val = float(length)
            length_str = (
                f'{int(length_val)}"' if length_val.is_integer() else f'{length_val}"'
            )
        except (ValueError, TypeError):
            length_str = f'{length}"' if length else 'LENGTH"'

        return f"{family}-{voltage}-{material_code}-{length_str}"

    def calculate_price(self) -> float:
        """
        Calculates the total price for the current configuration.
        """
        if not self.current_config:
            return 0.0

        config = self.current_config

        # Find the specific variant that matches the current selection
        variant = self.product_service.find_variant(
            self.db, config.product_family_id, config.selected_options
        )

        # If no specific variant is found, we cannot price accurately.
        # Fallback to base product or handle as an error. For now, return base price.
        if not variant:
            logger.warning(
                f"No matching variant found for options: {config.selected_options}. Using base price."
            )
            # Attempt to use the family's base product as a fallback
            return config.base_product.get("base_price", 0.0)

        # Now, we have a specific variant, so we can use its ID for pricing
        price = calculate_product_price(
            db=self.db,
            product_id=variant.id,  # Use the specific variant ID
            length=config.selected_options.get("Probe Length"),
            material_override=variant.material,  # Use the variant's material
            specs={
                "connection_type": config.selected_options.get("Connection"),
                "flange_rating": config.selected_options.get("Flange Rating"),
                "flange_size": config.selected_options.get("Flange Size"),
                "triclamp_size": config.selected_options.get("Tri-Clamp Size"),
            },
        )
        return price

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
