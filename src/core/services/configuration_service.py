import logging
from typing import Optional

from sqlalchemy.orm import Session

from src.core.models.configuration import Configuration
from src.core.pricing import calculate_product_price
from src.core.services.product_service import ProductService

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

    @property
    def current_config(self) -> Optional[Configuration]:
        """Get the current configuration."""
        return self._current_config

    @current_config.setter
    def current_config(self, value: Optional[Configuration]):
        """Set the current configuration."""
        self._current_config = value

    def start_configuration(
        self, product_family_id: int, product_family_name: str, base_product_info: dict
    ) -> Configuration:
        """
        Initializes a new product configuration session.

        Args:
            product_family_id: The ID of the product family being configured.
            product_family_name: The name of the product family.
            base_product_info: A dictionary containing the details of the base product selected.

        Returns:
            The newly created Configuration object.
        """
        self.current_config = Configuration(
            db=self.db,
            product_family_id=product_family_id,
            product_family_name=product_family_name,
            base_product=base_product_info,
        )

        # Initialize with base product values to ensure defaults are set
        options = self.current_config.selected_options
        options['Voltage'] = base_product_info.get('voltage')
        options['Material'] = base_product_info.get('material')
        options['Probe Length'] = base_product_info.get('base_length', 0.0)

        # Perform initial calculation and model number generation
        self.current_config.final_price = self.calculate_price()
        self.current_config.model_number = self.generate_model_number()

        return self.current_config

    def select_option(self, option_name: str, value: any):
        """
        Updates the current configuration with a selected option.

        Args:
            option_name (str): The name of the option (e.g., "Material", "Length").
            value (any): The selected value for the option.
        """
        if not self.current_config:
            return

        # Store the current material before updating options
        current_material = self.current_config.selected_options.get('Material')
        if not current_material:
            current_material = self.current_config.base_product.get('material')

        # Update the selected option
        if option_name == 'Material':
            # If the value is a number (like a length), don't update it
            if str(value).isdigit():
                self.current_config.selected_options['Material'] = current_material
            else:
                # Map full material names to their codes if needed
                material_map = {
                    '316SS': 'S',
                    '304SS': 'S',
                    'Hastelloy C': 'H',
                    'Monel': 'M',
                    'Titanium': 'T',
                    'Inconel': 'I',
                    '316SS with Teflon Sleeve': 'TS',
                    '316SS with Halar Coating': 'H',
                    'Titanium with Teflon Sleeve': 'TS',
                }

                # For LS2000, always use single-letter codes
                if self.current_config.product_family_name == 'LS2000':
                    # If it's already a single letter or two letters (like TS), use it directly
                    if len(str(value)) <= 2:
                        self.current_config.selected_options['Material'] = value
                    else:
                        # Otherwise, look up the code in the material map
                        self.current_config.selected_options['Material'] = (
                            material_map.get(str(value), value)
                        )
                else:
                    # For other models, preserve the original value
                    self.current_config.selected_options['Material'] = value
        elif option_name == 'Probe Length':
            # If we're changing the length, ensure we preserve the material
            self.current_config.selected_options[option_name] = value
            # Only update material if it's not already set or if it was accidentally changed
            if (
                not self.current_config.selected_options.get('Material')
                or str(self.current_config.selected_options.get('Material')).isdigit()
            ):
                self.current_config.selected_options['Material'] = current_material
        else:
            # For all other options, just update the value
            self.current_config.selected_options[option_name] = value

        self.current_config.final_price = self.calculate_price()
        self.current_config.model_number = self.generate_model_number()

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

    # More methods will be added here to handle validation, etc.
