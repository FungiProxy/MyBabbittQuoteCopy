"""
Database models for the application.
"""

from src.core.models.customer import Customer
from src.core.models.product import Product
from src.core.models.product_variant import ProductFamily, ProductVariant
from src.core.models.material import Material, StandardLength, MaterialAvailability
from src.core.models.option import Option, QuoteItemOption
from src.core.models.quote import Quote, QuoteItem
from src.core.models.spare_part import SparePart
from src.core.models.connection_option import ConnectionOption
from src.core.models.voltage_option import VoltageOption
from src.core.models.material_option import MaterialOption
from src.core.models.o_ring_material_option import O_RingMaterialOption
from src.core.models.cable_length_option import CableLengthOption
from src.core.models.housing_type_option import HousingTypeOption

__all__ = [
    "Customer",
    "Product",
    "ProductFamily",
    "ProductVariant",
    "Material",
    "StandardLength",
    "MaterialAvailability",
    "Option",
    "QuoteItemOption",
    "Quote",
    "QuoteItem",
    "SparePart",
    "ConnectionOption",
    "VoltageOption",
    "MaterialOption",
    "O_RingMaterialOption",
    "CableLengthOption",
    "HousingTypeOption",
]
