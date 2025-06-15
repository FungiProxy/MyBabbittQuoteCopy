from abc import ABC, abstractmethod
from typing import Dict, Optional

from src.core.models import (
    ConnectionOption,
    MaterialAvailability,
    Product,
    StandardLength,
    Option,
)

from .context import PricingContext


class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, context: PricingContext) -> float:
        """Calculates a price component and returns the new total price."""
        pass


class MaterialAvailabilityStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        if not context.material_override_code:
            return context.price

        # Get product type from model number
        product_type = context.product.model_number.split("-")[0]
        
        # Handle special cases for dual point switches
        if product_type == "LS7000" and "/2" in context.product.model_number:
            product_type = "LS7000/2"

        # Get material option for this product type
        material_option = (
            context.db.query(Option)
            .filter(
                Option.name == "Material",
                Option.category == "Material",
                Option.product_families.like(f"%{product_type}%")
            )
            .first()
        )

        if not material_option or context.material_override_code not in material_option.choices:
            raise ValueError(
                f"Material {context.material_override_code} is not available for product type {product_type}"
            )

        return context.price


class BasePriceStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        price = 0.0
        material_code = context.material.code

        # For exotic materials, price is based on Stainless Steel 'S' version
        if material_code in ["U", "T"]:
            s_material_product = (
                context.db.query(Product)
                .filter(
                    Product.model_number == context.product.model_number,
                    Product.voltage == context.product.voltage,
                    Product.material == "S",
                )
                .first()
            )

            if s_material_product:
                price = s_material_product.base_price
            else:
                price = context.product.base_price
        else:
            price = context.product.base_price

        context.price = price
        return context.price


class MaterialPremiumStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        # Get material option for this product type
        product_type = context.product.model_number.split("-")[0]
        if product_type == "LS7000" and "/2" in context.product.model_number:
            product_type = "LS7000/2"

        material_option = (
            context.db.query(Option)
            .filter(
                Option.name == "Material",
                Option.category == "Material",
                Option.product_families.like(f"%{product_type}%")
            )
            .first()
        )

        if material_option and context.material.code in material_option.adders:
            context.price += material_option.adders[context.material.code]

        return context.price


class ExtraLengthStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        effective_length = float(context.effective_length_in or 0.0)
        base_length = float(context.product.base_length or 0.0)
        material_code = context.material.code
        product_type = context.product.model_number.split("-")[0]

        # For U and T materials, calculate per inch from 4"
        if material_code in ["U", "T"]:
            base_length = 4.0
            if effective_length > base_length:
                extra_length = effective_length - base_length
                adder = 40.0 if material_code == "U" else 50.0
                context.price += extra_length * adder
            return context.price

        # For S material with 10" base length, use hard-coded thresholds
        if material_code == "S" and base_length == 10.0:
            thresholds = {
                24: 45.0,   # $45 for 24"
                36: 90.0,   # $90 for 36"
                48: 135.0,  # $135 for 48"
                60: 180.0,  # $180 for 60"
                72: 225.0,  # $225 for 72"
                84: 270.0,  # $270 for 84"
                96: 315.0,  # $315 for 96"
                108: 360.0, # $360 for 108"
                120: 405.0  # $405 for 120"
            }
            
            applicable_threshold = max((t for t in thresholds.keys() if t <= effective_length), default=0)
            if applicable_threshold > 0:
                context.price += thresholds[applicable_threshold]
            return context.price

        # For other materials, calculate per foot from base length
        if effective_length <= base_length:
            return context.price

        extra_inches = effective_length - base_length
        full_feet = int(extra_inches / 12)

        if full_feet > 0:
            # Get the appropriate adder per foot
            if product_type == "LS2000":
                length_adders = {
                    "H": 110.0,  # $110/foot
                    "TS": 110.0,  # $110/foot
                }
            else:
                length_adders = {
                    "H": 110.0,  # $110/foot
                    "TS": 110.0,  # $110/foot
                }

            adder = length_adders.get(material_code, 0.0)
            context.price += full_feet * adder

        return context.price


class NonStandardLengthSurchargeStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        product_type = context.product.model_number.split("-")[0]
        effective_length = float(context.effective_length_in or 0.0)

        # Special handling for Halar material
        if context.material.code == "H":
            # Get standard lengths for Halar from configuration
            standard_lengths = (
                context.db.query(StandardLength)
                .filter(StandardLength.material_code == "H")
                .all()
            )
            standard_length_values = [sl.length for sl in standard_lengths]
            
            # Check if length is standard
            is_standard = effective_length in standard_length_values
            
            if not is_standard:
                context.price += 50.0  # $50 adder for non-standard lengths
            
            # Check Halar length limit
            if effective_length > 72:
                raise ValueError(
                    "Halar coated probes cannot exceed 72 inches. Please select Teflon Sleeve for longer lengths."
                )
            return context.price

        # For other materials, check if they have a surcharge
        material_option = (
            context.db.query(Option)
            .filter(
                Option.name == "Material",
                Option.category == "Material",
                Option.product_families.like(f"%{product_type}%")
            )
            .first()
        )

        if material_option and material_option.adders.get(context.material.code, 0) > 0:
            # For materials with adders, apply surcharge for non-standard lengths
            # Note: Teflon Sleeve (TS) is exempt from surcharges
            if context.material.code != "TS":
                context.price += 50.0  # Standard $50 surcharge for non-standard lengths

        return context.price


class ConnectionOptionStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        connection_type = context.specs.get("connection_type")
        if not connection_type:
            return context.price

        # Get connection option from database
        connection_option = (
            context.db.query(Option)
            .filter(
                Option.name == "Connection",
                Option.category == "Connection",
                Option.product_families.like(f"%{context.product.model_number.split('-')[0]}%")
            )
            .first()
        )

        if not connection_option:
            return context.price

        # Get the specific connection price based on type and size
        if connection_type == "Flange":
            rating = context.specs.get("flange_rating")
            size = context.specs.get("flange_size")
            key = f"Flange_{rating}_{size}"
        elif connection_type == "Tri-Clamp":
            size = context.specs.get("triclamp_size")
            key = f"TriClamp_{size}"
        else:
            return context.price

        if key in connection_option.adders:
            context.price += connection_option.adders[key]

        return context.price
