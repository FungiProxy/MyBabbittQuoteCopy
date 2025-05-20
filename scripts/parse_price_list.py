"""
Parse price list and populate the database with all products.

This script reads the price list text file and extracts product information,
then populates the database with that information.
"""
import os
import re
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.core.models import ProductFamily, ProductVariant


def parse_price_list(price_list_path):
    """Parse the price list file and extract product information."""
    with open(price_list_path, "r") as file:
        content = file.read()
    
    # Split content into sections for each product family
    # This is a simplified approach and would need refinement for the actual price list format
    family_sections = re.split(r"\n\n+", content)
    
    product_data = []
    current_family = None
    
    for section in family_sections:
        lines = section.strip().split("\n")
        
        # Skip empty sections
        if not lines:
            continue
        
        # Check if this is a new product family header
        if lines[0].strip().endswith("LEVEL SWITCH") or lines[0].strip().endswith("TRANSMITTER") or "FLOW SWITCH" in lines[0]:
            current_family = {
                "name": lines[0].strip().split()[0],
                "description": lines[0].strip(),
                "category": "Level Switch" if "LEVEL SWITCH" in lines[0] else 
                             "Level Transmitter" if "TRANSMITTER" in lines[0] else
                             "Flow Switch" if "FLOW SWITCH" in lines[0] else "Other",
                "variants": []
            }
            product_data.append(current_family)
            lines = lines[1:]  # Skip the header line
        
        # If we have a current family, process variant lines
        if current_family:
            for line in lines:
                # Look for model number and price pattern: MODEL-VOLTAGE-MATERIAL-LENGTH $PRICE
                match = re.search(r"([A-Z0-9/]+)-([0-9A-Z]+)-([A-Z]+)-([0-9]+\")\s+\$([0-9,.]+)", line)
                if match:
                    model_base = match.group(1)
                    voltage = match.group(2)
                    material = match.group(3)
                    length = match.group(4).replace('"', '')
                    price = float(match.group(5).replace(",", ""))
                    
                    variant = {
                        "model_number": f"{model_base}-{voltage}-{material}-{length}\"",
                        "voltage": voltage,
                        "material": material,
                        "base_length": float(length),
                        "base_price": price,
                        "description": f"{current_family['name']} with {voltage} power and {length}\" {material} probe"
                    }
                    
                    current_family["variants"].append(variant)
    
    return product_data


def populate_products_from_data(db: Session, product_data):
    """Populate the database with product data extracted from the price list."""
    for family_data in product_data:
        # Create product family
        family = ProductFamily(
            name=family_data["name"],
            description=family_data["description"],
            category=family_data["category"]
        )
        db.add(family)
        db.flush()  # Flush to get the family ID
        
        # Create product variants
        for variant_data in family_data["variants"]:
            variant = ProductVariant(
                product_family_id=family.id,
                model_number=variant_data["model_number"],
                description=variant_data["description"],
                base_price=variant_data["base_price"],
                base_length=variant_data["base_length"],
                voltage=variant_data["voltage"],
                material=variant_data["material"]
            )
            db.add(variant)
        
        print(f"Added family {family.name} with {len(family_data['variants'])} variants")
    
    db.commit()


def main():
    """Parse price list and populate the database."""
    price_list_path = Path("data/price_list.txt")
    
    if not price_list_path.exists():
        print(f"Price list file not found at {price_list_path}")
        return
    
    # Parse price list
    print(f"Parsing price list from {price_list_path}")
    product_data = parse_price_list(price_list_path)
    
    # Populate database
    db = SessionLocal()
    try:
        populate_products_from_data(db, product_data)
        print("Products populated from price list")
    finally:
        db.close()


if __name__ == "__main__":
    main() 