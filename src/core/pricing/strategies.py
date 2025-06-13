from abc import ABC, abstractmethod

from src.core.models import (
    ConnectionOption,
    MaterialAvailability,
    Product,
    StandardLength,
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
            return context.price  # No override, no check needed

        # Extract product type from model number
        product_type = context.product.model_number.split('-')[0]

        # Handle special cases for dual point switches
        if product_type == 'LS7000' and '/2' in context.product.model_number:
            product_type = 'LS7000/2'

        availability = (
            context.db.query(MaterialAvailability)
            .filter(
                MaterialAvailability.material_code == context.material_override_code,
                MaterialAvailability.product_type == product_type,
                MaterialAvailability.is_available,
            )
            .first()
        )

        if not availability:
            raise ValueError(
                f'Material {context.material_override_code} is not available for product type {product_type}'
            )

        return context.price  # No price change, just validation


class BasePriceStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        price = 0.0
        material_code = context.material.code

        # For exotic materials, price is based on Stainless Steel 'S' version
        if material_code in ['U', 'T']:
            s_material_product = (
                context.db.query(Product)
                .filter(
                    Product.model_number == context.product.model_number,
                    Product.voltage == context.product.voltage,
                    Product.material == 'S',
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
        # Only applies if base price was calculated from 'S' material
        if context.material.code == 'U':  # UHMWPE
            context.price += 20.0  # $20 adder to S base price
        elif context.material.code == 'T':  # Teflon
            context.price += 60.0  # $60 adder to S base price

        return context.price


class ExtraLengthStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        effective_length = float(context.effective_length_in or 0.0)
        base_length = float(context.product.base_length or 0.0)

        if effective_length > base_length:
            extra_length = effective_length - base_length
            material_code = context.material.code
            product_type = context.product.model_number.split('-')[0]

            # LS2000 specific pricing
            if product_type == 'LS2000':
                length_adders = {
                    'S': 3.75,  # $45/foot
                    'H': 9.17,  # $110/foot
                    'TS': 9.17,  # $110/foot
                    'U': 40.0,  # $40/inch
                    'T': 50.0,  # $50/inch
                }

                # For U and T materials, calculate per inch from 4"
                if material_code in ['U', 'T']:
                    base_length = 4.0
                    if effective_length > base_length:
                        extra_length = effective_length - base_length
                else:
                    # For S, H, and TS, calculate per foot from 10"
                    base_length = 10.0
                    if effective_length > base_length:
                        extra_length = effective_length - base_length

                adder = length_adders.get(material_code, 0.0)
                context.price += extra_length * adder
            else:
                # Default pricing for other products
                length_adders = {
                    'S': 3.75,  # $45/foot
                    'H': 9.17,  # $110/foot
                    'TS': 9.17,  # $110/foot
                    'U': 40.0,  # $40/inch
                    'T': 50.0,  # $50/inch
                }
                adder = length_adders.get(material_code, 0.0)
                context.price += extra_length * adder

        return context.price


class NonStandardLengthSurchargeStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        product_type = context.product.model_number.split('-')[0]
        effective_length = float(context.effective_length_in or 0.0)

        # LS2000 specific rules
        if product_type == 'LS2000':
            # Define standard lengths for LS2000
            standard_lengths = [6, 8, 10, 12, 16, 24, 36, 48, 60, 72]

            # Check if length is standard
            is_standard = effective_length in standard_lengths

            # Apply surcharge if not standard length and not Teflon Sleeve
            if not is_standard and context.material.code != 'TS':
                context.price += 300.0  # $300 adder for non-standard lengths

            # Check Halar length limit
            if context.material.code == 'H' and effective_length > 72:
                raise ValueError(
                    'Halar coated probes cannot exceed 72 inches. Please select Teflon Sleeve for longer lengths.'
                )
        else:
            # Default behavior for other products
            if context.material.has_nonstandard_length_surcharge:
                is_standard = (
                    context.db.query(StandardLength)
                    .filter(
                        StandardLength.material_code == context.material.code,
                        StandardLength.length == effective_length,
                    )
                    .first()
                    is not None
                )

                if not is_standard:
                    context.price += context.material.nonstandard_length_surcharge

        return context.price


class ConnectionOptionStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        connection_type = context.specs.get('connection_type')
        price_adder = 0.0

        if connection_type == 'Flange':
            rating = context.specs.get('flange_rating')
            size = context.specs.get('flange_size')
            option = (
                context.db.query(ConnectionOption)
                .filter_by(type='Flange', rating=rating, size=size)
                .first()
            )
            if option:
                price_adder = option.price
        elif connection_type == 'Tri-Clamp':
            size = context.specs.get('triclamp_size')
            option = (
                context.db.query(ConnectionOption)
                .filter_by(type='Tri-Clamp', size=size)
                .first()
            )
            if option:
                price_adder = option.price

        context.price += price_adder
        return context.price
