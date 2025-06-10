from abc import ABC, abstractmethod

from src.core.models import Product, StandardLength, MaterialAvailability, ConnectionOption
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

        product_type = context.product.model_number.split('-')[0]
        
        if "/" in product_type:
            product_type = product_type.split("/")[0] + "/" + product_type.split("/")[1]

        availability = context.db.query(MaterialAvailability).filter(
            MaterialAvailability.material_code == context.material_override_code,
            MaterialAvailability.product_type == product_type,
            MaterialAvailability.is_available == True
        ).first()

        if not availability:
            raise ValueError(f"Material {context.material_override_code} is not available for product type {product_type}")
        
        return context.price  # No price change, just validation


class BasePriceStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        price = 0.0
        material_code = context.material.code

        # For exotic materials, price is based on Stainless Steel 'S' version
        if material_code in ['U', 'T']:
            s_material_product = context.db.query(Product).filter(
                Product.model_number == context.product.model_number,
                Product.voltage == context.product.voltage,
                Product.material == "S"
            ).first()
            
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
        if context.effective_length_in > context.product.base_length:
            extra_length = context.effective_length_in - context.product.base_length
            material_code = context.material.code
            
            length_adders = {
                'S': 3.75,   # $45/foot
                'H': 9.17,   # $110/foot
                'TS': 9.17,  # $110/foot
                'U': 40.0,   # $40/inch
                'T': 50.0    # $50/inch
            }
            
            adder = length_adders.get(material_code, 0.0)
            context.price += extra_length * adder

        return context.price


class NonStandardLengthSurchargeStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        if context.material.has_nonstandard_length_surcharge:
            is_standard = context.db.query(StandardLength).filter(
                StandardLength.material_code == context.material.code,
                StandardLength.length == context.effective_length_in
            ).first() is not None
            
            if not is_standard:
                context.price += context.material.nonstandard_length_surcharge

        return context.price


class ConnectionOptionStrategy(PricingStrategy):
    def calculate(self, context: PricingContext) -> float:
        connection_type = context.specs.get("connection_type")
        price_adder = 0.0
        
        if connection_type == "Flange":
            rating = context.specs.get("flange_rating")
            size = context.specs.get("flange_size")
            option = context.db.query(ConnectionOption).filter_by(type="Flange", rating=rating, size=size).first()
            if option:
                price_adder = option.price
        elif connection_type == "Tri-Clamp":
            size = context.specs.get("triclamp_size")
            option = context.db.query(ConnectionOption).filter_by(type="Tri-Clamp", size=size).first()
            if option:
                price_adder = option.price

        context.price += price_adder
        return context.price 