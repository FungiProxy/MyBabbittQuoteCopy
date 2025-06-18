"""
Database models for the application.
"""

from src.core.models.base_model import BaseModel
from src.core.models.connection import Connection
from src.core.models.connection_option import ConnectionOption
from src.core.models.customer import Customer
from src.core.models.material import Material, MaterialAvailability, StandardLength
from src.core.models.material_option import MaterialOption
from src.core.models.option import Option, QuoteItemOption
from src.core.models.product import Product
from src.core.models.product_family import ProductFamily
from src.core.models.product_variant import ProductVariant
from src.core.models.quote import Quote, QuoteItem
from src.core.models.spare_part import SparePart
from src.core.models.voltage_option import VoltageOption
from src.core.models.cable import Cable
from src.core.models.enclosure import Enclosure
from src.core.models.electrical_protection import ElectricalProtection
from src.core.models.insulation import Insulation
from src.core.models.configuration import Configuration
from src.core.models.o_ring import O_Ring
from src.core.models.exotic_metal import ExoticMetal
from src.core.models.identification import Identification
from src.core.models.price_component import PriceComponent

__all__ = [
    "BaseModel",
    "Connection",
    "ConnectionOption",
    "Customer",
    "Material",
    "MaterialAvailability",
    "MaterialOption",
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
    "Cable",
    "Enclosure",
    "ElectricalProtection",
    "Insulation",
    "Configuration",
    "O_Ring",
    "ExoticMetal",
    "Identification",
    "PriceComponent",
]
