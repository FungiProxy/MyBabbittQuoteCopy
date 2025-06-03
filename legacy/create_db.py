"""
Create and populate the complete database.

This script creates the database structure and populates it with:
1. Basic reference data (materials, standard lengths)
2. Product catalog from the price list
3. Sample data for testing

Run this script during development to create a pre-populated database.
"""
import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.database import init_db

# Import database initialization functions
from scripts.init_db import (
    populate_materials,
    populate_options,
    populate_product_families,
    populate_product_variants,
    populate_sample_customers,
    populate_standard_lengths,
)

# Import price list parsing functions
from scripts.parse_price_list import parse_price_list, populate_products_from_data

from src.core.database import SessionLocal


def main():
    """Create and populate the complete database."""
    # Create database schema
    print("Creating database schema...")
    init_db()
    
    # Open database session
    db = SessionLocal()
    
    try:
        # Populate reference data
        print("Populating reference data...")
        populate_materials(db)
        populate_standard_lengths(db)
        populate_options(db)
        
        # Check if we should parse the price list
        price_list_path = Path("data/price_list.txt")
        if price_list_path.exists():
            print("Parsing price list and populating products...")
            product_data = parse_price_list(price_list_path)
            populate_products_from_data(db, product_data)
        else:
            print("Price list not found, using sample product data...")
            populate_product_families(db)
            populate_product_variants(db)
        
        # Add sample customers
        print("Adding sample customer data...")
        populate_sample_customers(db)
        
        print("Database creation complete!")
        
    finally:
        db.close()


if __name__ == "__main__":
    main() 