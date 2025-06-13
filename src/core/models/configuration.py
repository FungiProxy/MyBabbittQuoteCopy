from dataclasses import dataclass, field
from typing import Any, Dict

from sqlalchemy.orm import Session

from src.core.models.option import Option


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
            return 0.0

        option_details = self.db.query(Option).filter_by(name=option_name).first()
        if not option_details or not option_details.adders:
            return 0.0

        # The price may be in a nested dictionary if adders are complex
        price = option_details.adders.get(str(option_value), 0.0)
        return float(price or 0.0)
