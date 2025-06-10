from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from src.core.models import Product

@dataclass
class Configuration:
    """A data class to hold the state of a product configuration session."""
    product_family_id: int
    product_family_name: str
    
    # The base product selected by the user
    base_product: Dict[str, Any] = field(default_factory=dict)
    
    # Selections made by the user
    selected_options: Dict[str, Any] = field(default_factory=dict)
    
    # Calculated values
    final_price: float = 0.0
    final_description: str = ""
    
    # Metadata
    is_valid: bool = False
    validation_errors: list[str] = field(default_factory=list) 