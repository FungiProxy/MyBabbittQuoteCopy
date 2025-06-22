"""
Pricing service for handling product pricing calculations.

This service provides a unified interface for pricing operations,
wrapping the existing pricing module and configuration service functionality.
"""

import logging
from typing import Dict, Any, Optional

from sqlalchemy.orm import Session

from src.core.pricing import PricingContext, calculate_product_price
from src.core.services.product_service import ProductService

logger = logging.getLogger(__name__)


class PricingService:
    """
    Service for handling product pricing calculations.
    
    This service provides a unified interface for pricing operations,
    wrapping the existing pricing module and configuration service functionality.
    """

    def __init__(self, db: Session, product_service: Optional[ProductService] = None):
        self.db = db
        self.product_service = product_service or ProductService()

    def calculate_product_price(self, context_data: Dict[str, Any]) -> float:
        """
        Calculate the total price for a product configuration.
        
        Args:
            context_data: Dictionary containing pricing context information:
                - product_family: Product family name
                - selected_options: Dictionary of selected options
                - base_price: Base price (optional, for fallback)
                
        Returns:
            float: Calculated total price
        """
        try:
            product_family = context_data.get('product_family')
            if not product_family:
                logger.error("product_family not provided in context_data")
                return context_data.get('base_price', 0.0)

            selected_options = context_data.get('selected_options', {})

            # Find the base product from the family name
            base_product_model = self.product_service.get_base_product_for_family(self.db, product_family)
            if not base_product_model:
                logger.error(f"Could not find base product for family: {product_family}")
                return context_data.get('base_price', 0.0)

            # Extract necessary details for PricingContext
            length = selected_options.get('Length', base_product_model.base_length)
            material_code = selected_options.get('Material', base_product_model.material)
            
            # Create the official PricingContext
            pricing_context = PricingContext(
                db=self.db,
                product_id=base_product_model.id,
                length_in=float(length) if length else None,
                material_override_code=material_code,
                specs=selected_options
            )
            
            # Calculate the price
            final_price = calculate_product_price(pricing_context)
            return final_price

        except Exception as e:
            logger.error(f"Error during price calculation: {e}", exc_info=True)
            return context_data.get('base_price', 0.0)

    def calculate_option_price(self, option_name: str, option_value: str, 
                             product_family: str, selected_options: Dict[str, Any]) -> float:
        """
        Calculate the price for a specific option.
        
        Args:
            option_name: Name of the option
            option_value: Selected value for the option
            product_family: Product family name
            selected_options: Current selected options
            
        Returns:
            float: Price adder for the option
        """
        try:
            # Get all options for this product family
            all_options = self.product_service.get_additional_options(self.db, product_family)

            # Find the specific option
            for option in all_options:
                if option.get("name") == option_name:
                    adders = option.get("adders", {})
                    if isinstance(adders, dict) and option_value in adders:
                        return float(adders[option_value])
                    break

            return 0.0

        except Exception as e:
            logger.error(f"Error calculating option price: {e}", exc_info=True)
            return 0.0

    def get_price_breakdown(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a detailed price breakdown for a product configuration.
        
        Args:
            context_data: Dictionary containing pricing context information
            
        Returns:
            Dict containing price breakdown information
        """
        try:
            product_family = context_data.get('product_family')
            selected_options = context_data.get('selected_options', {})
            
            # Get base product
            base_product_model = self.product_service.get_base_product_for_family(self.db, product_family)
            if not base_product_model:
                return {
                    'base_price': 0.0,
                    'option_adders': {},
                    'total_price': 0.0,
                    'breakdown': []
                }

            base_price = base_product_model.base_price
            option_adders = {}
            breakdown = [f"Base Price: ${base_price:.2f}"]

            # Calculate option adders
            for option_name, value in selected_options.items():
                if value and option_name not in ['Length']:  # Skip length as it's handled by pricing strategies
                    adder = self.calculate_option_price(option_name, value, product_family, selected_options)
                    if adder > 0:
                        option_adders[option_name] = adder
                        breakdown.append(f"{option_name}: +${adder:.2f}")

            # Calculate total price
            total_price = self.calculate_product_price(context_data)

            return {
                'base_price': base_price,
                'option_adders': option_adders,
                'total_price': total_price,
                'breakdown': breakdown
            }

        except Exception as e:
            logger.error(f"Error getting price breakdown: {e}", exc_info=True)
            return {
                'base_price': 0.0,
                'option_adders': {},
                'total_price': 0.0,
                'breakdown': []
            } 