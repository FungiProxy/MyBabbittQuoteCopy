"""
Pricing module for calculating product prices with complex rules.

This module handles all pricing calculations for Babbitt International products,
including material-specific pricing, length-based calculations, non-standard length
surcharges, and connection options. It implements the business rules for:

- Base price calculations
- Material-specific pricing (S, H, U, T materials)
- Length-based price adjustments
- Non-standard length surcharges
- Connection option pricing
- Special customer pricing rules

The pricing logic follows the rules specified in additional_info.txt and
the standard price list.
"""
from typing import Optional, Dict, Any

from sqlalchemy.orm import Session

from src.core.models import Material, Product, StandardLength, MaterialAvailability
from src.core.models.connection_option import ConnectionOption


def calculate_product_price(
    db: Session, 
    product_id: int, 
    length: Optional[float] = None,
    material_override: Optional[str] = None,
    specs: Optional[Dict[str, Any]] = None
) -> float:
    """
    Calculate the total price for a product, including material, length, and connection options.
    
    This function implements the core pricing logic for Babbitt International products,
    handling complex rules for different materials and lengths.
    
    Args:
        db: SQLAlchemy database session
        product_id: Unique identifier of the product
        length: Length in inches (if applicable). If None, uses product's base length
        material_override: Material code to override the product's default material
                         (S=Stainless Steel, H=Halar, U=UHMWPE, T=Teflon)
        specs: Dictionary containing product specifications including connection options
              Example: {"connection_type": "Flange", "flange_rating": "150#", "flange_size": "2"}
        
    Returns:
        float: Calculated total price including all applicable adjustments
        
    Raises:
        ValueError: If the product doesn't exist, material doesn't exist, or material
                   is not available for the product
        
    Examples:
        >>> calculate_product_price(db, 1, length=24, material_override="S")
        >>> calculate_product_price(db, 2, specs={"connection_type": "Tri-Clamp", "triclamp_size": "2"})
    """
    # Get product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ValueError(f"Product with ID {product_id} not found")
    
    # If no length specified, use the base length
    if length is None:
        length = product.base_length
    
    # Determine material to use
    material_code = material_override if material_override else product.material
    
    # Get material information
    material = db.query(Material).filter(Material.code == material_code).first()
    if not material:
        raise ValueError(f"Material {material_code} not found")
    
    # Check if the material is available for this product type
    if material_override:
        # Extract the base product type (e.g., "LS2000" from "LS2000-115VAC-S-10")
        product_type = product.model_number.split('-')[0]
        
        # Special handling for dual point switches which have a format like "LS7000/2-115VAC-H-10"
        if "/" in product_type:
            product_type = product_type.split("/")[0] + "/" + product_type.split("/")[1]
        
        # Check if the material is available for this product type
        availability = db.query(MaterialAvailability).filter(
            MaterialAvailability.material_code == material_code,
            MaterialAvailability.product_type == product_type,
            MaterialAvailability.is_available == True
        ).first()
        
        if not availability:
            raise ValueError(f"Material {material_code} is not available for product type {product_type}")
    
    # Start with base price
    price = product.base_price
    
    # Material price adjustments
    if material_override and material_override != product.material:
        # For exotic materials (U and T), calculate based on S material price
        if material_override in ['U', 'T']:  # U = UHMWPE, T = Teflon
            s_material_product = db.query(Product).filter(
                Product.model_number == product.model_number,
                Product.voltage == product.voltage,
                Product.material == "S"  # S = 316 Stainless Steel
            ).first()
            
            if s_material_product:
                # Start with S material price
                price = s_material_product.base_price
                
                # Add material-specific premium based on additional_info.txt
                if material_override == 'U':  # UHMWPE
                    price += 20.0  # $20 adder to S base price
                elif material_override == 'T':  # Teflon
                    price += 60.0  # $60 adder to S base price
        elif material_override == 'H':  # H = Halar Coated
            # No base price adjustment for Halar Coated in additional_info.txt
            pass
    
    # Length price adjustments
    if length and length > product.base_length:
        extra_length = length - product.base_length
        
        # Apply material-specific length adders based on additional_info.txt
        if material_code == 'S':
            # $45/foot = $3.75/inch
            price += extra_length * 3.75
        elif material_code == 'H' or material_code == 'TS':
            # $110/foot = $9.17/inch
            price += extra_length * 9.17
        elif material_code == 'U':
            # $40/inch
            price += extra_length * 40.0
        elif material_code == 'T':
            # $50/inch
            price += extra_length * 50.0
    
    # Apply non-standard length surcharge if applicable
    if material.has_nonstandard_length_surcharge:
        # Check if length is a standard length
        is_standard = db.query(StandardLength).filter(
            StandardLength.material_code == material_code,
            StandardLength.length == length
        ).first() is not None
        
        if not is_standard:
            price += material.nonstandard_length_surcharge
    
    # Add connection option price if specs provided
    if specs:
        price += get_connection_option_price(db, specs)
    
    return price


def calculate_option_price(
    option_price: float,
    option_price_type: str,
    length: Optional[float] = None
) -> float:
    """
    Calculate the price of an option based on its type and parameters.
    
    Handles different pricing models including fixed prices, per-inch pricing,
    and per-foot pricing for product options.
    
    Args:
        option_price: Base price of the option
        option_price_type: Type of pricing calculation to apply:
                         - "fixed": Single fixed price
                         - "per_inch": Price multiplied by length in inches
                         - "per_foot": Price multiplied by length in feet
        length: Length in inches (required for per_inch and per_foot options)
        
    Returns:
        float: Calculated option price
        
    Examples:
        >>> calculate_option_price(100.0, "fixed")  # Returns 100.0
        >>> calculate_option_price(10.0, "per_inch", length=24)  # Returns 240.0
        >>> calculate_option_price(120.0, "per_foot", length=24)  # Returns 240.0
    """
    if option_price_type == "fixed":
        return option_price
    elif option_price_type == "per_inch" and length is not None:
        return option_price * length
    elif option_price_type == "per_foot" and length is not None:
        # Convert inches to feet
        return option_price * (length / 12)
    else:
        return option_price  # Default to fixed price 


def get_connection_option_price(db: Session, specs: Dict[str, Any]) -> float:
    """
    Calculate the price for connection options based on specifications.
    
    Handles pricing for different connection types including flanges and tri-clamp
    connections with various sizes and ratings.
    
    Args:
        db: SQLAlchemy database session
        specs: Dictionary containing connection specifications:
              For Flanges: {
                  "connection_type": "Flange",
                  "flange_rating": "150#" | "300#",
                  "flange_size": "1" | "2" | "3" | "4"
              }
              For Tri-Clamp: {
                  "connection_type": "Tri-Clamp",
                  "triclamp_size": "1.5" | "2" | "3"
              }
        
    Returns:
        float: Price of the connection option, 0.0 if not found or not applicable
        
    Examples:
        >>> get_connection_option_price(db, {"connection_type": "Flange", 
        ...                                 "flange_rating": "150#", 
        ...                                 "flange_size": "2"})
        >>> get_connection_option_price(db, {"connection_type": "Tri-Clamp",
        ...                                 "triclamp_size": "1.5"})
    """
    connection_type = specs.get("connection_type")
    if connection_type == "Flange":
        rating = specs.get("flange_rating")
        size = specs.get("flange_size")
        option = db.query(ConnectionOption).filter_by(type="Flange", rating=rating, size=size).first()
        return option.price if option else 0.0
    elif connection_type == "Tri-Clamp":
        size = specs.get("triclamp_size")
        option = db.query(ConnectionOption).filter_by(type="Tri-Clamp", size=size).first()
        return option.price if option else 0.0
    return 0.0 