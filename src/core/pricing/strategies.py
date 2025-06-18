from abc import ABC, abstractmethod

from src.core.models import (
    Option,
    Product,
    StandardLength,
    MaterialOption,
    Material,
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
                Option.product_families.like(f"%{product_type}%"),
            )
            .first()
        )

        if (
            not material_option
            or context.material_override_code not in material_option.choices
        ):
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

        # Get the material option for this product family and material
        material_option = (
            context.db.query(MaterialOption)
            .filter(
                MaterialOption.product_family_id == context.product.product_family_id,
                MaterialOption.material_code == context.material.code,
                MaterialOption.is_available == 1,
            )
            .first()
        )

        if material_option:
            context.price += material_option.base_price

        return context.price


class ExtraLengthStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        effective_length = float(context.effective_length_in or 0.0)
        base_length = float(context.product.base_length or 0.0)
        material_code = context.material.code

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
            if effective_length <= base_length:
                return context.price

            extra_length = effective_length - base_length
            adder = 3.75  # $3.75 per inch for S material
            context.price += extra_length * adder
            return context.price

        # For other materials, calculate per foot from base length
        if effective_length <= base_length:
            return context.price

        extra_inches = effective_length - base_length
        full_feet = int(extra_inches / 12)

        if full_feet > 0:
            # Get the appropriate adder per foot
            if context.product.model_number.startswith("LS2000"):
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
        effective_length = float(context.effective_length_in or 0.0)
        material_code = context.material.code

        # Special handling for Halar material
        if material_code == "H":
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
        material = (
            context.db.query(Material).filter(Material.code == material_code).first()
        )

        if material and material.has_nonstandard_length_surcharge:
            # Check if length is standard
            standard_lengths = (
                context.db.query(StandardLength)
                .filter(StandardLength.material_code == material_code)
                .all()
            )
            standard_length_values = [sl.length for sl in standard_lengths]

            if effective_length not in standard_length_values:
                context.price += material.nonstandard_length_surcharge

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
                Option.product_families.like(
                    f"%{context.product.model_number.split('-')[0]}%"
                ),
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
