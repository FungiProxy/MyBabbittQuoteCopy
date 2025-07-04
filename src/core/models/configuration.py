import logging
from dataclasses import dataclass, field
from typing import Any, Dict

from sqlalchemy.orm import Session

from src.core.models.option import Option

logger = logging.getLogger(__name__)


@dataclass
class Configuration:
    """A data class to hold the state of a product configuration session."""

    db: Session
    product_family_id: int
    product_family_name: str

    # The base product selected by the user
    base_product: Dict[str, Any] = field(default_factory=dict)

    # Selections made by the user
    selected_options: Dict[str, Any] = field(default_factory=dict)

    # Calculated values
    final_price: float = 0.0
    final_description: str = ''
    model_number: str = ''
    quantity: int = 1  # Default quantity is 1

    # Metadata
    is_valid: bool = False
    validation_errors: list[str] = field(default_factory=list)

    def get_option_price(self, option_name: str, option_value: Any) -> float:
        """Get the price for a given option and its selected value."""
        if not option_value:
            logger.debug(f'No value provided for option {option_name}')
            return 0.0

        logger.debug(f'Getting price for {option_name}={option_value}')
        logger.debug(f'Product family: {self.product_family_name}')

        # Filter options by name and product family
        option_details = (
            self.db.query(Option)
            .filter(
                Option.name == option_name,
                Option.product_families == self.product_family_name,
            )
            .first()
        )

        if not option_details:
            logger.warning(
                f'No option found for {option_name} in {self.product_family_name}'
            )
            return 0.0

        logger.debug(f'Found option: {option_details.name}')
        logger.debug(f'Choices: {option_details.choices}')
        logger.debug(f'Adders: {option_details.adders}')

        if not option_details.adders:
            logger.warning(f'No adders found for option {option_name}')
            return 0.0

        # Convert option_value to string for comparison
        option_value_str = str(option_value)
        logger.debug(f'Looking for price for value: {option_value_str}')

        # The price may be in a nested dictionary if adders are complex
        price = option_details.adders.get(option_value_str, 0.0)
        logger.debug(f'Found price: ${price:,.2f}')

        return float(price or 0.0)
