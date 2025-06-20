import math
from abc import ABC, abstractmethod

from src.core.models import (
    Option,
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
            return context.price

        # Get product type from model number
        product_type = context.product.model_number.split('-')[0]

        # Handle special cases for dual point switches
        if product_type == 'LS7000' and '/2' in context.product.model_number:
            product_type = 'LS7000/2'

        # Get material option for this product type
        material_option = (
            context.db.query(Option)
            .filter(
                Option.name == 'Material',
                Option.category == 'Material',
                Option.product_families.like(f'%{product_type}%'),
            )
            .first()
        )

        if (
            not material_option
            or context.material_override_code not in material_option.choices
        ):
            raise ValueError(
                f'Material {context.material_override_code} is not available for product type {product_type}'
            )

        return context.price


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
        # Get material option for this product type
        product_type = context.product.model_number.split('-')[0]
        if product_type == 'LS7000' and '/2' in context.product.model_number:
            product_type = 'LS7000/2'

        material_option = (
            context.db.query(Option)
            .filter(
                Option.name == 'Material',
                Option.category == 'Material',
                Option.product_families.like(f'%{product_type}%'),
            )
            .first()
        )

        if material_option and context.material.code in material_option.adders:
            context.price += material_option.adders[context.material.code]

        return context.price


class ExtraLengthStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        effective_length = float(context.effective_length_in or 0.0)
        material_code = context.material.code
        product_family = context.product.model_number.split('-')[0]
        
        # Get length adder rules from database
        from src.core.database import SessionLocal
        from sqlalchemy import text
        
        with SessionLocal() as session:
            # Query for length adder rules
            query = text("""
                SELECT adder_type, first_threshold, adder_amount, description
                FROM length_adder_rules 
                WHERE product_family = :product_family 
                AND material_code = :material_code
            """)
            
            result = session.execute(query, {
                'product_family': product_family,
                'material_code': material_code
            }).fetchone()
            
            if not result:
                # No specific rule found, return base price
                return context.price
            
            adder_type = result.adder_type
            first_threshold = result.first_threshold
            adder_amount = result.adder_amount
            
            # Handle per-inch adders (U, T, CPVC materials)
            if adder_type == 'per_inch':
                if effective_length > first_threshold:
                    extra_length = effective_length - first_threshold
                    context.price += extra_length * adder_amount
                return context.price
            
            # Handle per-foot adders (S, H, TS, C materials)
            elif adder_type == 'per_foot':
                if effective_length >= first_threshold:
                    # Calculate how many 12-inch increments starting AT the threshold
                    extra_inches = effective_length - first_threshold
                    increments = math.floor(extra_inches / 12) + 1  # +1 because threshold itself counts
                    context.price += increments * adder_amount
                return context.price
            
            return context.price


class NonStandardLengthSurchargeStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        effective_length = float(context.effective_length_in or 0.0)

        # Special handling for Halar material ONLY
        if context.material.code == 'H':
            # Standard lengths for Halar material: 6, 10, 12, 18, 24, 36, 48, 60, 72, 84, 96
            standard_lengths = [6, 10, 12, 18, 24, 36, 48, 60, 72, 84, 96]

            # Check if length is standard
            is_standard = effective_length in standard_lengths

            if not is_standard:
                context.price += 300.0  # $300 adder for non-standard lengths

            # Check Halar length limit
            if effective_length > 96:
                raise ValueError(
                    'Halar coated probes cannot exceed 96 inches. Please select Teflon Sleeve for longer lengths.'
                )
            return context.price

        # No surcharge for other materials
        return context.price


class ConnectionOptionStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        connection_type = context.specs.get('connection_type')
        if not connection_type:
            return context.price

        # Get connection option from database
        connection_option = (
            context.db.query(Option)
            .filter(
                Option.name == 'Connection',
                Option.category == 'Connection',
                Option.product_families.like(
                    f"%{context.product.model_number.split('-')[0]}%"
                ),
            )
            .first()
        )

        if not connection_option:
            return context.price

        # Get the specific connection price based on type and size
        if connection_type == 'Flange':
            rating = context.specs.get('flange_rating')
            size = context.specs.get('flange_size')
            key = f'Flange_{rating}_{size}'
        elif connection_type == 'Tri-Clamp':
            size = context.specs.get('triclamp_size')
            key = f'TriClamp_{size}'
        else:
            return context.price

        if key in connection_option.adders:
            context.price += connection_option.adders[key]

        return context.price
