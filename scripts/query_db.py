"""
Query database contents.

This script queries the database and displays its contents.
"""
import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.database import SessionLocal
from src.core.models import (
    Customer,
    Material,
    Option,
    Product,
    ProductFamily,
    ProductVariant,
    StandardLength,
    MaterialAvailability,
)


def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)


def print_materials(db):
    """Print all materials in the database."""
    print_separator("Materials")
    materials = db.query(Material).all()
    
    if not materials:
        print("No materials found.")
        return
    
    print(f"{'Code':<5} {'Name':<25} {'Base Length':<12} {'Length Adder':<15} {'Special Rules'}")
    print("-" * 80)
    
    for material in materials:
        length_adder = f"${material.length_adder_per_inch}/inch" if material.length_adder_per_inch else \
                       f"${material.length_adder_per_foot}/foot" if material.length_adder_per_foot else "N/A"
        
        special_rules = []
        if material.has_nonstandard_length_surcharge:
            special_rules.append(f"${material.nonstandard_length_surcharge} surcharge for non-standard length")
        if material.base_price_adder:
            special_rules.append(f"${material.base_price_adder} adder to S base price")
        
        special_rules_str = ", ".join(special_rules) if special_rules else "None"
        
        print(f"{material.code:<5} {material.name:<25} {material.base_length:<12} {length_adder:<15} {special_rules_str}")


def print_standard_lengths(db):
    """Print all standard lengths in the database."""
    print_separator("Standard Lengths")
    standard_lengths = db.query(StandardLength).all()
    
    if not standard_lengths:
        print("No standard lengths found.")
        return
    
    # Group by material code
    lengths_by_material = {}
    for length in standard_lengths:
        if length.material_code not in lengths_by_material:
            lengths_by_material[length.material_code] = []
        lengths_by_material[length.material_code].append(length.length)
    
    for material_code, lengths in lengths_by_material.items():
        print(f"{material_code} standard lengths: {', '.join(str(int(length)) if length.is_integer() else str(length) for length in sorted(lengths))}")


def print_product_families(db):
    """Print all product families in the database."""
    print_separator("Product Families")
    families = db.query(ProductFamily).all()
    
    if not families:
        print("No product families found.")
        return
    
    print(f"{'Name':<15} {'Category':<20} {'Description'}")
    print("-" * 80)
    
    for family in families:
        print(f"{family.name:<15} {family.category:<20} {family.description}")


def print_product_variants(db):
    """Print product variants in the database."""
    print_separator("Product Variants")
    variants = db.query(ProductVariant).all()
    
    if not variants:
        print("No product variants found.")
        return
    
    print(f"{'Model':<25} {'Material':<10} {'Voltage':<10} {'Base Length':<12} {'Base Price'}")
    print("-" * 80)
    
    for variant in variants:
        print(f"{variant.model_number:<25} {variant.material:<10} {variant.voltage:<10} {variant.base_length:<12} ${variant.base_price:.2f}")


def print_options(db):
    """Print all options in the database."""
    print_separator("Options")
    options = db.query(Option).all()
    
    if not options:
        print("No options found.")
        return
    
    print(f"{'Name':<30} {'Category':<15} {'Price':<15} {'Compatible With'}")
    print("-" * 80)
    
    for option in options:
        price_str = f"${option.price:.2f}"
        if option.price_type != "fixed":
            price_str += f" ({option.price_type})"
        
        compatible_with = option.product_families if option.product_families else "All"
        
        print(f"{option.name:<30} {option.category:<15} {price_str:<15} {compatible_with}")


def print_customers(db):
    """Print all customers in the database."""
    print_separator("Customers")
    customers = db.query(Customer).all()
    
    if not customers:
        print("No customers found.")
        return
    
    print(f"{'Name':<20} {'Company':<25} {'Email':<30} {'Phone'}")
    print("-" * 80)
    
    for customer in customers:
        print(f"{customer.name:<20} {customer.company or 'N/A':<25} {customer.email or 'N/A':<30} {customer.phone or 'N/A'}")


def print_material_availability(db):
    """Print material availability for different product types."""
    print_separator("Material Availability")
    
    # Get all product types
    product_types = db.query(MaterialAvailability.product_type).distinct().all()
    product_types = [pt[0] for pt in product_types]
    
    if not product_types:
        print("No product types found.")
        return
    
    # For each product type, show available and unavailable materials
    for product_type in product_types:
        print(f"\nProduct Type: {product_type}")
        
        # Get availability records for this product type
        availability_records = db.query(MaterialAvailability).filter(
            MaterialAvailability.product_type == product_type
        ).all()
        
        available = [r.material_code for r in availability_records if r.is_available]
        unavailable = [r.material_code for r in availability_records if not r.is_available]
        
        if available:
            print(f"  Available materials: {', '.join(available)}")
        if unavailable:
            print(f"  Unavailable materials: {', '.join(unavailable)}")
            
            # Show notes for unavailable materials
            for record in availability_records:
                if not record.is_available and record.notes:
                    print(f"    Note for {record.material_code}: {record.notes}")


def main():
    """Query and display database contents."""
    db = SessionLocal()
    
    try:
        print_materials(db)
        print_standard_lengths(db)
        print_product_families(db)
        print_product_variants(db)
        print_options(db)
        print_customers(db)
        print_material_availability(db)
        
        print("\nQuery complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main() 