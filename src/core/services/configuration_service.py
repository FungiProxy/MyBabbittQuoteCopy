from sqlalchemy.orm import Session
from src.core.models.configuration import Configuration
from src.core.services.product_service import ProductService
from src.core.pricing import calculate_product_price
from typing import Optional


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
            product_family_id=product_family_id,
            product_family_name=product_family_name,
            base_product=base_product_info,
        )
        # Initialize with base values
        self.current_config.selected_options["Length"] = base_product_info.get(
            "base_length", 0.0
        )
        self.current_config.final_price = self.calculate_price()

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

        self.current_config.selected_options[option_name] = value
        self.current_config.final_price = self.calculate_price()

    def calculate_price(self) -> float:
        """
        Calculates the total price for the current configuration.
        """
        if not self.current_config:
            return 0.0

        # Prepare arguments for the pricing function
        config = self.current_config

        # We need the product_id of the specific variant, not the family.
        # This part of the logic needs to be robust. For now, we'll assume
        # the base_product dictionary contains a 'variant_id' or similar.
        # This will need to be improved later.
        product_id = config.base_product.get(
            "id"
        )  # This is family id, needs to be variant id

        # The pricing function needs the actual variant from the DB.
        # This lookup should ideally be part of the product_service.
        # For now, we'll pass the family ID and see how the pricing function handles it.

        price = calculate_product_price(
            db=self.db,
            product_id=product_id,
            length=config.selected_options.get("Probe Length"),
            material_override=config.selected_options.get("Material"),
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
