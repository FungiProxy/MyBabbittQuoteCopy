"""
Business logic services for the application.
"""

from src.core.services.customer_service import CustomerService
from src.core.services.product_service import ProductService
from src.core.services.quote_service import QuoteService
from src.core.services.spare_part_service import SparePartService
from src.core.services.configuration_service import ConfigurationService
from src.core.services.pricing_service import PricingService
from src.core.services.validation_service import ValidationService

__all__ = [
    "CustomerService",
    "ProductService",
    "QuoteService",
    "SparePartService",
    "ConfigurationService",
    "PricingService",
    "ValidationService",
]

"""
Services package initialization.
"""
