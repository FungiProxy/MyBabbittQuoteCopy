"""
Pricing module for calculating product prices with complex rules.

This module provides a strategy-based pricing calculator for Babbitt International products.
It orchestrates a series of pricing strategies to calculate the final price,
ensuring that complex business rules for materials, lengths, and options are applied correctly.
"""
from typing import Optional, Dict, Any, List

from sqlalchemy.orm import Session

from src.core.pricing.context import PricingContext
from src.core.pricing.strategies import (
    PricingStrategy,
    MaterialAvailabilityStrategy,
    BasePriceStrategy,
    MaterialPremiumStrategy,
    ExtraLengthStrategy,
    NonStandardLengthSurchargeStrategy,
    ConnectionOptionStrategy,
)


class PriceCalculator:
    def __init__(self, strategies: List[PricingStrategy]):
        self.strategies = strategies

    def calculate(self, context: PricingContext) -> float:
        for strategy in self.strategies:
            strategy.calculate(context)
        return context.price


def calculate_product_price(
    db: Session, 
    product_id: int, 
    length: Optional[float] = None,
    material_override: Optional[str] = None,
    specs: Optional[Dict[str, Any]] = None
) -> float:
    """
    Calculate the total price for a product using a strategy-based calculator.
    
    This function orchestrates the pricing logic for Babbitt International products
    by applying a series of pricing strategies in a specific order.
    
    Args:
        db: SQLAlchemy database session
        product_id: Unique identifier of the product
        length: Length in inches (if applicable)
        material_override: Material code to override the product's default material
        specs: Dictionary containing product specifications including connection options
        
    Returns:
        float: Calculated total price.
        
    Raises:
        ValueError: If the product, material, or options are invalid or unavailable.
    """
    # Create the context for this pricing calculation
    context = PricingContext(
        db=db,
        product_id=product_id,
        length_in=length,
        material_override_code=material_override,
        specs=specs or {}
    )

    # Define the sequence of pricing strategies
    # The order is critical for correct calculation
    pricing_strategies = [
        MaterialAvailabilityStrategy(),
        BasePriceStrategy(),
        MaterialPremiumStrategy(),
        ExtraLengthStrategy(),
        NonStandardLengthSurchargeStrategy(),
        ConnectionOptionStrategy(),
    ]

    # Create and run the calculator
    calculator = PriceCalculator(pricing_strategies)
    final_price = calculator.calculate(context)
    
    return final_price


def calculate_option_price(
    option_price: float,
    option_price_type: str,
    length: Optional[float] = None
) -> float:
    """
    Calculate the price of an option based on its type and parameters.
    
    Handles different pricing models including fixed prices, per-inch pricing,
    and per-foot pricing for product options.
    
    Args:
        option_price: Base price of the option
        option_price_type: Type of pricing calculation to apply:
                         - "fixed": Single fixed price
                         - "per_inch": Price multiplied by length in inches
                         - "per_foot": Price multiplied by length in feet
        length: Length in inches (required for per_inch and per_foot options)
        
    Returns:
        float: Calculated option price
    """
    if option_price_type == "fixed":
        return option_price
    elif option_price_type == "per_inch" and length is not None:
        return option_price * length
    elif option_price_type == "per_foot" and length is not None:
        # Convert inches to feet
        return option_price * (length / 12)
    else:
        return option_price  # Default to fixed price 