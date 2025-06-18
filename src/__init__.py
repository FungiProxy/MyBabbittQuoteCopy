"""
MyBabbittQuote application package
"""

__version__ = "0.1.0"

from src.core.models import (
    BaseModel,
    ProductFamily,
    ProductVariant,
    Option,
    Material,
    MaterialOption,
    VoltageOption,
    Connection,
    ConnectionOption,
    Insulation,
    O_Ring,
    ExoticMetal,
    Enclosure,
    Cable,
    ElectricalProtection,
    Identification,
    PriceComponent,
    SparePart,
    Customer,
    Quote,
    QuoteItem,
    QuoteItemOption,
    StandardLength,
)

from src.core.services import (
    ConfigurationService,
    PricingService,
    ValidationService,
    ProductService,
)

__all__ = [
    "BaseModel",
    "ProductFamily",
    "ProductVariant",
    "Option",
    "Material",
    "MaterialOption",
    "VoltageOption",
    "Connection",
    "ConnectionOption",
    "Insulation",
    "O_Ring",
    "ExoticMetal",
    "Enclosure",
    "Cable",
    "ElectricalProtection",
    "Identification",
    "PriceComponent",
    "SparePart",
    "Customer",
    "Quote",
    "QuoteItem",
    "QuoteItemOption",
    "StandardLength",
    "ConfigurationService",
    "PricingService",
    "ValidationService",
    "ProductService",
]

# Empty __init__.py to mark directory as Python package
