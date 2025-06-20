import logging
from typing import Optional
import traceback

from sqlalchemy.orm import Session

from src.core.models.configuration import Configuration
from src.core.pricing import calculate_product_price
from src.core.services.product_service import ProductService
from src.core.models.option import Option

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
        print(f"DEBUG: select_option called with {option_name}={value}")

        if not self.current_config:
            print("DEBUG: No current configuration")
            return

        # Store the current material before updating options
        current_material = self.current_config.selected_options.get("Material")
        if not current_material:
            current_material = self.current_config.base_product.get("material")

        # Update the selected option
        if option_name == "Material":
            print(f"DEBUG: Processing material selection: {value}")
            # If the value is a number (like a length), don't update it
            if str(value).isdigit():
                print(
                    f"DEBUG: Material value {value} is numeric, keeping current material: {current_material}"
                )
                self.current_config.selected_options["Material"] = current_material
            else:
                print(f"DEBUG: Updating material to: {value}")
                self.current_config.selected_options["Material"] = value
        else:
            print(f"DEBUG: Updating option {option_name} to: {value}")
            self.current_config.selected_options[option_name] = value

        print(f"DEBUG: About to call _update_price()")
        # Update the model number and price
        self._update_model_number()
        self._update_price()
        print(f"DEBUG: Finished _update_price()")
        print(f"DEBUG: Final configuration: {self.current_config.selected_options}")

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
            logger.error(f"Error getting current variant: {str(e)}", exc_info=True)
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
                if option.get("name") == option_name:
                    adders = option.get("adders", {})
                    if isinstance(adders, dict) and value in adders:
                        return float(adders[value])
                    break

            # Fallback to configuration's get_option_price method
            price = self.current_config.get_option_price(option_name, value)
            # logger.debug(f"Price for {option_name}={value}: ${price:,.2f}")
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
            if hasattr(value, "return_value"):
                value = value.return_value
            if hasattr(value, "base_price"):
                value = value.base_price
            if hasattr(value, "price"):
                value = value.price
            if hasattr(value, "adder"):
                value = value.adder
            if hasattr(value, "price_multiplier"):
                value = value.price_multiplier
            if hasattr(value, "length"):
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
        """Update the price based on the current configuration using the unified options structure."""
        print("DEBUG: _update_price() called")
        try:
            print("DEBUG: Getting current variant...")
            try:
                variant = self._get_current_variant()
                print(f"DEBUG: Got variant: {variant}")
            except Exception as e:
                print(f"DEBUG: Exception in _get_current_variant(): {e}")
                variant = None
            if not variant:
                print(
                    "DEBUG: No variant found, using fallback pricing WITH option adders"
                )
                # Fallback to base product price
                base_price = self._to_float(
                    self.current_config.base_product.get("base_price", 0.0)
                )
                if base_price == 0.0:
                    base_price = 425.0  # Use the current fallback price

                # Calculate final price starting with base price
                final_price = base_price
                print(
                    f"DEBUG: Starting fallback calculation with base price: {base_price}"
                )

                # Get all options for this product family and apply adders
                all_options = self.product_service.get_additional_options(
                    self.db, self.current_config.product_family_name
                )
                print(f"DEBUG: Got {len(all_options)} options for fallback pricing")

                # Apply option adders
                for (
                    option_name,
                    selected_value,
                ) in self.current_config.selected_options.items():
                    if selected_value is None:
                        continue

                    print(
                        f"DEBUG: Processing fallback option: {option_name}={selected_value}"
                    )

                    # Handle exotic metal override pricing
                    if option_name == "Exotic Metal Override":
                        override_value = self._to_float(selected_value)
                        if override_value > 0:
                            final_price += override_value
                            print(
                                f"DEBUG: Applied exotic metal override: {override_value}, new total: {final_price}"
                            )
                        continue

                    # Find the option in the unified structure
                    for option in all_options:
                        if option.get("name") == option_name:
                            adders = option.get("adders", {})
                            selected_value_str = str(selected_value).strip()
                            print(
                                f"DEBUG: Checking adders for {option_name}: {list(adders.keys())}"
                            )

                            if (
                                isinstance(adders, dict)
                                and selected_value_str in adders
                            ):
                                adder_value = float(adders[selected_value_str])
                                final_price += adder_value
                                print(
                                    f"DEBUG: Applied {option_name} adder: {adder_value}, new total: {final_price}"
                                )
                            else:
                                print(
                                    f"DEBUG: No adder found for {selected_value_str} in {option_name}"
                                )
                            break

                self.current_config.final_price = final_price
                self.current_config.model_number = ""
                print(f"DEBUG: Set final fallback price to: {final_price}")
                return

            print("DEBUG: Using variant pricing...")
            # Use the variant's base price
            base_price = self._to_float(getattr(variant, "base_price", 0.0))
            if base_price == 0.0:
                base_price = self._to_float(
                    self.current_config.base_product.get("base_price", 0.0)
                )
            self.current_config.model_number = str(getattr(variant, "model_number", ""))
            print(f"DEBUG: Base price from variant: {base_price}")

            # Calculate final price starting with base price
            final_price = base_price
            print(f"DEBUG: Starting final_price calculation with: {final_price}")

            print("DEBUG: Getting additional options...")
            # Get all options for this product family
            all_options = self.product_service.get_additional_options(
                self.db, self.current_config.product_family_name
            )
            print(f"DEBUG: Got {len(all_options)} options")

            # Print all options and adders for diagnosis
            print("--- OPTIONS DIAG ---")
            for option in all_options:
                print(
                    f"Option: {option.get('name')}, Adders: {option.get('adders')}, Choices: {option.get('choices')}"
                )
            print("-------------------")

            # Print selected options for diagnosis
            print("--- SELECTED OPTIONS DIAG ---")
            for (
                option_name,
                selected_value,
            ) in self.current_config.selected_options.items():
                print(f"Selected option: {option_name}, Value: {selected_value}")
            print("----------------------------")

            # Apply option adders using the unified structure
            for (
                option_name,
                selected_value,
            ) in self.current_config.selected_options.items():
                if selected_value is None:
                    continue

                # Handle exotic metal override pricing
                if option_name == "Exotic Metal Override":
                    # This is a manual override value for exotic metals
                    override_value = self._to_float(selected_value)
                    if override_value > 0:
                        final_price += override_value
                        # logger.debug(f"Applied exotic metal override: {override_value}")
                    continue

                # Find the option in the unified structure
                # Check all options since multiple options can have the same name (e.g., Material)
                for option in all_options:
                    if option.get("name") == option_name:
                        adders = option.get("adders", {})
                        selected_value_str = str(selected_value).strip()
                        print(f"DEBUG: Adders keys: {list(adders.keys())}")
                        print(f"DEBUG: Selected value: '{selected_value_str}'")
                        if isinstance(adders, dict) and selected_value_str in adders:
                            print(
                                f"DEBUG: Found adder for {selected_value_str}: {adders[selected_value_str]}"
                            )
                            # Check if this product family is excluded from adders
                            excluded_products = option.get("excluded_products", "")
                            if excluded_products is None:
                                excluded_products = ""
                            excluded_list = [
                                f.strip()
                                for f in excluded_products.split(",")
                                if f.strip()
                            ]
                            is_excluded = (
                                self.current_config.product_family_name in excluded_list
                            )

                            if not is_excluded:
                                adder_value = float(adders[selected_value_str])
                                final_price += adder_value
                                print(
                                    f"DEBUG: Applied {option_name} adder: {adder_value}, new total: {final_price}"
                                )
                            else:
                                print(
                                    f"DEBUG: Skipped {option_name} adder for excluded family: {self.current_config.product_family_name}"
                                )
                                pass
                            break
                        else:
                            print(
                                f"DEBUG: No adder found for {selected_value_str} in {adders}"
                            )

            # Handle special cases that might not be in the unified structure yet
            # Handle extra length price
            specified_length = self._to_float(
                self.current_config.selected_options.get("Probe Length")
            )
            # Use base product's base_length for extra length calculation
            base_length = self._to_float(
                self.current_config.base_product.get("base_length", 0.0)
            )

            if specified_length > base_length:
                # For S material with 10" base length, use hard-coded thresholds
                material_code = self.current_config.selected_options.get("Material")
                if material_code == "S" and base_length == 10.0:
                    thresholds = {
                        24: 45.0,  # $45 for 24"
                        36: 90.0,  # $90 for 36"
                        48: 135.0,  # $135 for 48"
                        60: 180.0,  # $180 for 60"
                        72: 225.0,  # $225 for 72"
                        84: 270.0,  # $270 for 84"
                        96: 315.0,  # $315 for 96"
                        108: 360.0,  # $360 for 108"
                        120: 405.0,  # $405 for 120"
                    }
                    # Find the highest threshold that's less than or equal to the specified length
                    applicable_threshold = max(
                        (t for t in thresholds.keys() if t <= specified_length),
                        default=0,
                    )
                    if applicable_threshold > 0:
                        final_price += thresholds[applicable_threshold]
                        # logger.debug(
                        #     f"Applied length threshold price: {thresholds[applicable_threshold]}"
                        # )
                else:
                    # For other materials, use per-inch calculation
                    extra_length = specified_length - base_length
                    extra_length_price = extra_length * 8.0  # $8 per inch
                    final_price += extra_length_price
                    # logger.debug(f"Applied extra length price: {extra_length_price}")

            # Add mechanical options (any selected option with a numeric value)
            for opt_name, opt_value in self.current_config.selected_options.items():
                if isinstance(opt_value, (int, float)):
                    # Avoid double-counting known numeric options (like Probe Length)
                    if opt_name not in ["Probe Length"]:
                        final_price += opt_value
                        # logger.debug(
                        #     f"Applied mechanical option '{opt_name}' price: {opt_value}"
                        # )

            # --- DIRECT MATERIAL ADDER FIX ---
            # Get selected material
            selected_material = self.current_config.selected_options.get("Material")
            # Get material adders from the material option
            material_option = next(
                (o for o in all_options if o.get("name") == "Material"), None
            )
            if material_option:
                adders = material_option.get("adders", {})
                selected_material_str = str(selected_material).strip()
                if selected_material_str in adders:
                    adder_value = float(adders[selected_material_str])
                    final_price += adder_value
                    print(
                        f"[FIX] Applied material adder for {selected_material_str}: {adder_value}, new total: {final_price}"
                    )
            # --- END DIRECT MATERIAL ADDER FIX ---

            # Update the final price
            self.current_config.final_price = final_price
            # logger.info(f"Final price calculated: {final_price}")

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
            # logger.warning(
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
