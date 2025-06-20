import logging
from typing import Optional

from sqlalchemy.orm import Session

from src.core.models.configuration import Configuration
from src.core.pricing import PricingContext, calculate_product_price
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
        # logger.debug("ConfigurationService initialized")

    @property
    def current_config(self) -> Optional[Configuration]:
        """Get the current configuration."""
        return self._current_config

    @current_config.setter
    def current_config(self, value: Optional[Configuration]):
        """Set the current configuration."""
        self._current_config = value
        if value:
            # logger.debug(
            #     f"Current configuration set for product family: {value.product_family_name}"
            # )
            pass
        else:
            # logger.debug("Current configuration cleared")
            pass

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
        # logger.debug(
        #     f"Starting configuration for {product_family_name} (ID: {product_family_id})"
        # )
        # logger.debug(f"Base product info: {base_product_info}")

        try:
            self._current_config = Configuration(
                db=self.db,
                product_family_id=product_family_id,
                product_family_name=product_family_name,
                base_product=base_product_info,
            )
            # logger.debug("Configuration object created successfully")

            # Set default material and voltage from base product
            if 'material' in base_product_info:
                self.set_option('Material', base_product_info['material'])
            if 'voltage' in base_product_info:
                self.set_option('Voltage', base_product_info['voltage'])

            self._update_price()
            self._update_model_number()

        except Exception as e:
            logger.error(f'Error creating configuration: {e!s}', exc_info=True)
            raise

    def set_option(self, option_name: str, value: any):
        """Set an option in the current configuration."""
        if self._current_config:
            self._current_config.set_option(option_name, value)
            self._update_price()
            self._update_model_number()

    def select_option(self, option_name: str, value: any):
        """
        Updates the current configuration with a selected option.

        Args:
            option_name (str): The name of the option (e.g., "Material", "Length").
            value (any): The selected value for the option.
        """
        print(f'DEBUG: select_option called with {option_name}={value}')

        if not self.current_config:
            print('DEBUG: No current configuration')
            return

        # Store the current material before updating options
        current_material = self.current_config.selected_options.get('Material')
        if not current_material:
            current_material = self.current_config.base_product.get('material')

        # Update the selected option
        if option_name == 'Material':
            print(f'DEBUG: Processing material selection: {value}')
            # If the value is a number (like a length), don't update it
            if str(value).isdigit():
                print(
                    f'DEBUG: Material value {value} is numeric, keeping current material: {current_material}'
                )
                self.current_config.selected_options['Material'] = current_material
            else:
                print(f'DEBUG: Updating material to: {value}')
                self.current_config.selected_options['Material'] = value
        else:
            print(f'DEBUG: Updating option {option_name} to: {value}')
            self.current_config.selected_options[option_name] = value

        print('DEBUG: About to call _update_price()')
        # Update the model number and price
        self._update_model_number()
        self._update_price()
        print('DEBUG: Finished _update_price()')
        print(f'DEBUG: Final configuration: {self.current_config.selected_options}')

    def _update_model_number(self):
        """Update the model number based on selected options."""
        if not self.current_config:
            # logger.warning(
            #     "No current configuration when trying to update model number"
            # )
            return

        # logger.debug("Updating model number")
        # Implementation details...

    def _get_current_variant(self):
        """Get the current product variant based on selected options."""
        if not self.current_config:
            # logger.warning("No current configuration when trying to get variant")
            return None

        try:
            # Find the specific variant that matches the current selection
            variant = self.product_service.find_variant(
                self.db,
                self.current_config.product_family_id,
                self.current_config.selected_options,
            )

            if not variant:
                # logger.warning(
                #     f"No matching variant found for options: {self.current_config.selected_options}"
                # )
                return None

            return variant

        except Exception as e:
            logger.error(f'Error getting current variant: {e!s}', exc_info=True)
            return None

    def _get_option_price(self, option_name: str, value: any) -> float:
        """Get the price for a given option and its selected value using the unified options structure."""
        if not self.current_config:
            return 0.0

        try:
            # Get all options for this product family
            all_options = self.product_service.get_additional_options(
                self.db, self.current_config.product_family_name
            )

            # Find the specific option
            for option in all_options:
                if option.get('name') == option_name:
                    adders = option.get('adders', {})
                    if isinstance(adders, dict) and value in adders:
                        return float(adders[value])
                    break

            # Fallback to configuration's get_option_price method
            price = self.current_config.get_option_price(option_name, value)
            # logger.debug(f"Price for {option_name}={value}: ${price:,.2f}")
            return price
        except Exception as e:
            logger.error(f'Error getting option price: {e!s}', exc_info=True)
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
        if not self.current_config:
            return

        effective_length = self.current_config.get_effective_length()
        material_code = self.current_config.get_selected_material_code()

        base_product = self.current_config.base_product
        if not base_product or 'id' not in base_product:
            logger.error('Base product not found or missing ID in configuration.')
            return

        # Create a pricing context
        context = PricingContext(
            db=self.db,
            product_id=base_product['id'],
            length_in=effective_length,
            material_override_code=material_code,
            specs=self.current_config.selected_options,
        )

        # Calculate price using the pricing engine
        self.current_config.final_price = calculate_product_price(context)

    def generate_model_number(self) -> str:
        """Generates the model number based on the current configuration."""
        if not self.current_config:
            return ''

        config = self.current_config
        family = config.product_family_name

        # Get values from selected options, falling back to base product values
        voltage = config.selected_options.get(
            'Voltage', config.base_product.get('voltage')
        )
        material = config.selected_options.get(
            'Material', config.base_product.get('material')
        )
        length = config.selected_options.get(
            'Probe Length', config.base_product.get('base_length')
        )

        # Map material names to their single-letter codes
        material_map = {
            '316SS': 'S',
            '304SS': 'S',
            'Hastelloy C': 'H',
            'Monel': 'M',
            'Titanium': 'T',
            'Inconel': 'I',
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

        return f'{family}-{voltage}-{material_code}-{length_str}'

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
            # logger.warning(
            logger.warning(
                f'No matching variant found for options: {config.selected_options}. Using base price.'
            )
            # Attempt to use the family's base product as a fallback
            return config.base_product.get('base_price', 0.0)

        # Now, we have a specific variant, so we can use its ID for pricing
        price = calculate_product_price(
            db=self.db,
            product_id=variant.id,  # Use the specific variant ID
            length=config.selected_options.get('Probe Length'),
            material_override=variant.material,  # Use the variant's material
            specs={
                'connection_type': config.selected_options.get('Connection'),
                'flange_rating': config.selected_options.get('Flange Rating'),
                'flange_size': config.selected_options.get('Flange Size'),
                'triclamp_size': config.selected_options.get('Tri-Clamp Size'),
            },
        )
        return price

    def get_final_description(self) -> str:
        """
        Generates a final description based on the selected options.
        """
        if not self.current_config:
            return ''

        # Basic description, can be expanded
        desc = f'{self.current_config.product_family_name} with:'
        for name, value in self.current_config.selected_options.items():
            if value:
                desc += f' {name}: {value},'

        return desc.strip(',')

    def add_non_standard_length_adder(self):
        """Add the non-standard length surcharge to the configuration."""
        if not self.current_config:
            return

        # Add the non-standard length surcharge
        self.current_config.selected_options['NonStandardLengthSurcharge'] = True
        self.current_config.final_price = self.calculate_price()

    def remove_non_standard_length_adder(self):
        """Remove the non-standard length surcharge from the configuration."""
        if not self.current_config:
            return

        # Remove the non-standard length surcharge
        self.current_config.selected_options.pop('NonStandardLengthSurcharge', None)
        self.current_config.final_price = self.calculate_price()

    def get_final_price(self) -> float:
        """Get the final price of the configured product."""
        if not self.current_config:
            return 0.0
        return self.current_config.final_price

    # More methods will be added here to handle validation, etc.
