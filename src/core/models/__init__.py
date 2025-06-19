"""
Database models for the application.
"""

from core.models.cable_length_option import CableLengthOption
from core.models.connection_option import ConnectionOption
from core.models.customer import Customer
from core.models.housing_type import HousingType
from core.models.housing_type_option import HousingTypeOption
from core.models.material import Material, MaterialAvailability, StandardLength
from core.models.material_option import MaterialOption
from core.models.o_ring_material_option import O_RingMaterialOption
from core.models.option import Option, QuoteItemOption
from core.models.product import Product
from core.models.product_variant import ProductFamily, ProductVariant
from core.models.quote import Quote, QuoteItem
from core.models.spare_part import SparePart
from core.models.voltage_option import VoltageOption

__all__ = [
    "CableLengthOption",
    "ConnectionOption",
    "Customer",
    "HousingType",
    "HousingTypeOption",
    "Material",
    "MaterialAvailability",
    "MaterialOption",
    "O_RingMaterialOption",
    "Option",
    "Product",
    "ProductFamily",
    "ProductVariant",
    "Quote",
    "QuoteItem",
    "QuoteItemOption",
    "SparePart",
    "StandardLength",
    "VoltageOption",
]
