"""
Test database initialization.

This script initializes the database with just the reference data
for testing purposes.
"""
import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from sqlalchemy import inspect

from src.core.database import SessionLocal, init_db, engine
from src.core.models import (
    Customer,
    Material,
    Option,
    ProductFamily,
    ProductVariant,
    Quote,
    QuoteItem,
    QuoteItemOption,
    StandardLength,
)

# Import database initialization functions
from scripts.init_db import (
    populate_materials,
    populate_options,
    populate_product_families,
    populate_product_variants,
    populate_sample_customers,
    populate_standard_lengths,
)


def verify_database_tables():
    """Verify that all expected tables exist in the database."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    expected_tables = [
        "customers",
        "materials",
        "options",
        "product_families",
        "product_variants",
        "quote_items",
        "quote_item_options",
        "quotes",
        "standard_lengths",
    ]
    
    print("\nVerifying database tables:")
    for table in expected_tables:
        if table in tables:
            print(f"✓ Table {table} exists")
        else:
            print(f"✗ Table {table} does not exist")


def count_records(db, model):
    """Count records in a table."""
    return db.query(model).count()


def verify_data(db):
    """Verify that data was correctly inserted into the database."""
    print("\nVerifying data:")
    print(f"✓ {count_records(db, Material)} materials")
    print(f"✓ {count_records(db, StandardLength)} standard lengths")
    print(f"✓ {count_records(db, ProductFamily)} product families")
    print(f"✓ {count_records(db, ProductVariant)} product variants")
    print(f"✓ {count_records(db, Option)} options")
    print(f"✓ {count_records(db, Customer)} customers")


def clear_database(db):
    """Clear all data from the database."""
    print("\nClearing database data...")
    # Order matters due to foreign key constraints
    db.query(QuoteItemOption).delete()
    db.query(QuoteItem).delete()
    db.query(Quote).delete()
    db.query(ProductVariant).delete()
    db.query(ProductFamily).delete()
    db.query(StandardLength).delete()
    db.query(Material).delete()
    db.query(Option).delete()
    db.query(Customer).delete()
    db.commit()
    print("Database cleared.")


def main():
    """Initialize and test the database."""
    # Create database schema
    print("Creating database schema...")
    init_db()
    
    # Verify tables were created
    verify_database_tables()
    
    # Open database session
    db = SessionLocal()
    
    try:
        # Check if we need to populate the database
        if count_records(db, Material) == 0:
            # Populate reference data
            print("\nPopulating reference data...")
            populate_materials(db)
            populate_standard_lengths(db)
            populate_options(db)
            populate_product_families(db)
            populate_product_variants(db)
            populate_sample_customers(db)
            print("Database populated.")
        else:
            print("\nDatabase already contains data.")
        
        # Verify data
        verify_data(db)
        
        print("\nDatabase initialization successful!")
    finally:
        db.close()


if __name__ == "__main__":
    # Clear the database before initializing
    clear_database(SessionLocal())
    main() 