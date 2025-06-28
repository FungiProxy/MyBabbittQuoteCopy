#!/usr/bin/env python3
"""
Clean Database Rebuild Script

This script completely rebuilds the database from scratch with the correct schema
and fresh data. It does NOT rely on any existing scripts or data files that may
be outdated or corrupted.

WARNING: This will completely destroy and recreate the database.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.core.database import Base, engine, get_db
from src.core.models import (
    BaseModel, Customer, Material, MaterialAvailability, MaterialOption,
    Option, ProductFamily, Quote, QuoteItem, QuoteItemOption,
    SparePart, StandardLength, VoltageOption, ConnectionOption,
    CableLengthOption, HousingType, HousingTypeOption, O_RingMaterialOption
)

# Import additional models that aren't in __init__.py
from src.core.models.exotic_metal_option import ExoticMetalOption
from src.core.models.probe_length_option import ProbeLengthOption
from src.core.models.product import Product

def drop_all_tables():
    """Drop all existing tables."""
    print("Dropping all existing tables...")
    
    # Drop all tables in the correct order to avoid foreign key constraints
    drop_queries = [
        "DROP TABLE IF EXISTS quote_item_options",
        "DROP TABLE IF EXISTS quote_items", 
        "DROP TABLE IF EXISTS quotes",
        "DROP TABLE IF EXISTS customers",
        "DROP TABLE IF EXISTS base_models",
        "DROP TABLE IF EXISTS product_families",
        "DROP TABLE IF EXISTS spare_parts",
        "DROP TABLE IF EXISTS material_availability",
        "DROP TABLE IF EXISTS material_options",
        "DROP TABLE IF EXISTS voltage_options",
        "DROP TABLE IF EXISTS connection_options",
        "DROP TABLE IF EXISTS exotic_metal_options",
        "DROP TABLE IF EXISTS probe_length_options",
        "DROP TABLE IF EXISTS housing_type_options",
        "DROP TABLE IF EXISTS cable_length_options",
        "DROP TABLE IF EXISTS o_ring_material_options",
        "DROP TABLE IF EXISTS standard_lengths",
        "DROP TABLE IF EXISTS materials",
        "DROP TABLE IF EXISTS options",
        "DROP TABLE IF EXISTS products",
        "DROP TABLE IF EXISTS alembic_version"
    ]
    
    with engine.connect() as conn:
        for query in drop_queries:
            conn.execute(text(query))
        conn.commit()
    
    print("All tables dropped successfully.")

def create_all_tables():
    """Create all tables with the correct schema."""
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")

def seed_product_families():
    """Seed product families with correct data."""
    print("Seeding product families...")
    
    families = [
        {
            "name": "LS2000",
            "description": "Level Switch Series 2000",
            "category": "Level Switch"
        },
        {
            "name": "LS7000",
            "description": "Level Switch Series 7000", 
            "category": "Level Switch"
        },
        {
            "name": "LS8000",
            "description": "Level Switch Series 8000",
            "category": "Level Switch"
        },
        {
            "name": "LS8000/2",
            "description": "Level Switch Series 8000/2",
            "category": "Level Switch"
        },
        {
            "name": "FS10000",
            "description": "Flow Switch Series 10000",
            "category": "Flow Switch"
        },
        {
            "name": "LT9000",
            "description": "Level Transmitter Series 9000",
            "category": "Level Transmitter"
        }
    ]
    
    db = next(get_db())
    try:
        for family_data in families:
            family = ProductFamily(**family_data)
            db.add(family)
        db.commit()
        print(f"Created {len(families)} product families")
    finally:
        db.close()

def seed_base_models():
    """Seed base models for each product family."""
    print("Seeding base models...")
    
    base_models = [
        {
            "product_family_id": 1,  # LS2000
            "model_number": "LS2000-115VAC-S-10",
            "description": "LS2000 Level Switch - Base Configuration",
            "base_price": 425.0,
            "base_length": 10.0,
            "voltage": "115VAC",
            "material": "S"
        },
        {
            "product_family_id": 2,  # LS7000
            "model_number": "LS7000-115VAC-S-10",
            "description": "LS7000 Level Switch - Base Configuration", 
            "base_price": 550.0,
            "base_length": 10.0,
            "voltage": "115VAC",
            "material": "S"
        },
        {
            "product_family_id": 3,  # LS8000
            "model_number": "LS8000-115VAC-S-10",
            "description": "LS8000 Level Switch - Base Configuration",
            "base_price": 650.0,
            "base_length": 10.0,
            "voltage": "115VAC",
            "material": "S"
        },
        {
            "product_family_id": 4,  # LS8000/2
            "model_number": "LS8000/2-115VAC-S-10",
            "description": "LS8000/2 Level Switch - Base Configuration",
            "base_price": 750.0,
            "base_length": 10.0,
            "voltage": "115VAC",
            "material": "S"
        },
        {
            "product_family_id": 5,  # FS10000
            "model_number": "FS10000-115VAC-S-6",
            "description": "FS10000 Flow Switch - Base Configuration",
            "base_price": 425.0,
            "base_length": 6.0,
            "voltage": "115VAC",
            "material": "S"
        },
        {
            "product_family_id": 6,  # LT9000
            "model_number": "LT9000-24VDC-S-10",
            "description": "LT9000 Level Transmitter - Base Configuration",
            "base_price": 850.0,
            "base_length": 10.0,
            "voltage": "24VDC",
            "material": "S"
        }
    ]
    
    db = next(get_db())
    try:
        for model_data in base_models:
            base_model = BaseModel(**model_data)
            db.add(base_model)
        db.commit()
        print(f"Created {len(base_models)} base models")
    finally:
        db.close()

def seed_materials():
    """Seed materials with correct pricing rules."""
    print("Seeding materials...")
    
    materials = [
        {
            "code": "S",
            "name": "316 Stainless Steel",
            "description": "Standard 316 stainless steel construction",
            "base_length": 10.0,
            "length_adder_per_inch": None,
            "length_adder_per_foot": None,
            "has_nonstandard_length_surcharge": False,
            "nonstandard_length_surcharge": None,
            "base_price_adder": 0.0
        },
        {
            "code": "H",
            "name": "Halar Coated",
            "description": "Halar coated for chemical resistance",
            "base_length": 10.0,
            "length_adder_per_inch": None,
            "length_adder_per_foot": None,
            "has_nonstandard_length_surcharge": False,
            "nonstandard_length_surcharge": None,
            "base_price_adder": 110.0
        },
        {
            "code": "U",
            "name": "UHMWPE",
            "description": "Ultra-high molecular weight polyethylene",
            "base_length": 10.0,
            "length_adder_per_inch": None,
            "length_adder_per_foot": None,
            "has_nonstandard_length_surcharge": False,
            "nonstandard_length_surcharge": None,
            "base_price_adder": 85.0
        },
        {
            "code": "T",
            "name": "Teflon",
            "description": "Teflon construction for extreme chemical resistance",
            "base_length": 10.0,
            "length_adder_per_inch": None,
            "length_adder_per_foot": None,
            "has_nonstandard_length_surcharge": False,
            "nonstandard_length_surcharge": None,
            "base_price_adder": 150.0
        }
    ]
    
    db = next(get_db())
    try:
        for material_data in materials:
            material = Material(**material_data)
            db.add(material)
        db.commit()
        print(f"Created {len(materials)} materials")
    finally:
        db.close()

def seed_material_options():
    """Seed material options for each product family."""
    print("Seeding material options...")
    
    material_options = [
        # LS2000 - all materials available
        {"product_family_id": 1, "material_code": "S", "display_name": "S - 316 Stainless Steel", "base_price": 0.0, "is_available": 1},
        {"product_family_id": 1, "material_code": "H", "display_name": "H - Halar Coated", "base_price": 110.0, "is_available": 1},
        {"product_family_id": 1, "material_code": "U", "display_name": "U - UHMWPE", "base_price": 85.0, "is_available": 1},
        {"product_family_id": 1, "material_code": "T", "display_name": "T - Teflon", "base_price": 150.0, "is_available": 1},
        
        # LS7000 - all materials available
        {"product_family_id": 2, "material_code": "S", "display_name": "S - 316 Stainless Steel", "base_price": 0.0, "is_available": 1},
        {"product_family_id": 2, "material_code": "H", "display_name": "H - Halar Coated", "base_price": 110.0, "is_available": 1},
        {"product_family_id": 2, "material_code": "U", "display_name": "U - UHMWPE", "base_price": 85.0, "is_available": 1},
        {"product_family_id": 2, "material_code": "T", "display_name": "T - Teflon", "base_price": 150.0, "is_available": 1},
        
        # LS8000 - all materials available
        {"product_family_id": 3, "material_code": "S", "display_name": "S - 316 Stainless Steel", "base_price": 0.0, "is_available": 1},
        {"product_family_id": 3, "material_code": "H", "display_name": "H - Halar Coated", "base_price": 110.0, "is_available": 1},
        {"product_family_id": 3, "material_code": "U", "display_name": "U - UHMWPE", "base_price": 85.0, "is_available": 1},
        {"product_family_id": 3, "material_code": "T", "display_name": "T - Teflon", "base_price": 150.0, "is_available": 1},
        
        # LS8000/2 - all materials available
        {"product_family_id": 4, "material_code": "S", "display_name": "S - 316 Stainless Steel", "base_price": 0.0, "is_available": 1},
        {"product_family_id": 4, "material_code": "H", "display_name": "H - Halar Coated", "base_price": 110.0, "is_available": 1},
        {"product_family_id": 4, "material_code": "U", "display_name": "U - UHMWPE", "base_price": 85.0, "is_available": 1},
        {"product_family_id": 4, "material_code": "T", "display_name": "T - Teflon", "base_price": 150.0, "is_available": 1},
        
        # FS10000 - all materials available
        {"product_family_id": 5, "material_code": "S", "display_name": "S - 316 Stainless Steel", "base_price": 0.0, "is_available": 1},
        {"product_family_id": 5, "material_code": "H", "display_name": "H - Halar Coated", "base_price": 110.0, "is_available": 1},
        {"product_family_id": 5, "material_code": "U", "display_name": "U - UHMWPE", "base_price": 85.0, "is_available": 1},
        {"product_family_id": 5, "material_code": "T", "display_name": "T - Teflon", "base_price": 150.0, "is_available": 1},
        
        # LT9000 - all materials available
        {"product_family_id": 6, "material_code": "S", "display_name": "S - 316 Stainless Steel", "base_price": 0.0, "is_available": 1},
        {"product_family_id": 6, "material_code": "H", "display_name": "H - Halar Coated", "base_price": 110.0, "is_available": 1},
        {"product_family_id": 6, "material_code": "U", "display_name": "U - UHMWPE", "base_price": 85.0, "is_available": 1},
        {"product_family_id": 6, "material_code": "T", "display_name": "T - Teflon", "base_price": 150.0, "is_available": 1}
    ]
    
    db = next(get_db())
    try:
        for option_data in material_options:
            option = MaterialOption(**option_data)
            db.add(option)
        db.commit()
        print(f"Created {len(material_options)} material options")
    finally:
        db.close()

def seed_voltage_options():
    """Seed voltage options for each product family."""
    print("Seeding voltage options...")
    
    voltage_options = [
        # LS2000 voltages
        {"product_family": "LS2000", "voltage": "115VAC", "is_available": 1},
        {"product_family": "LS2000", "voltage": "230VAC", "is_available": 1},
        {"product_family": "LS2000", "voltage": "24VDC", "is_available": 1},
        
        # LS7000 voltages
        {"product_family": "LS7000", "voltage": "115VAC", "is_available": 1},
        {"product_family": "LS7000", "voltage": "230VAC", "is_available": 1},
        {"product_family": "LS7000", "voltage": "24VDC", "is_available": 1},
        
        # LS8000 voltages
        {"product_family": "LS8000", "voltage": "115VAC", "is_available": 1},
        {"product_family": "LS8000", "voltage": "230VAC", "is_available": 1},
        {"product_family": "LS8000", "voltage": "24VDC", "is_available": 1},
        
        # LS8000/2 voltages
        {"product_family": "LS8000/2", "voltage": "115VAC", "is_available": 1},
        {"product_family": "LS8000/2", "voltage": "230VAC", "is_available": 1},
        {"product_family": "LS8000/2", "voltage": "24VDC", "is_available": 1},
        
        # FS10000 voltages
        {"product_family": "FS10000", "voltage": "115VAC", "is_available": 1},
        {"product_family": "FS10000", "voltage": "230VAC", "is_available": 1},
        {"product_family": "FS10000", "voltage": "24VDC", "is_available": 1},
        
        # LT9000 voltages
        {"product_family": "LT9000", "voltage": "24VDC", "is_available": 1}
    ]
    
    db = next(get_db())
    try:
        for option_data in voltage_options:
            option = VoltageOption(**option_data)
            db.add(option)
        db.commit()
        print(f"Created {len(voltage_options)} voltage options")
    finally:
        db.close()

def seed_options():
    """Seed product options with correct structure."""
    print("Seeding product options...")
    
    options = [
        {
            "name": "Material",
            "description": "Material selection for the probe",
            "price": 0.0,
            "price_type": "fixed",
            "category": "material",
            "product_families": "LS2000,LS7000,LS8000,LS8000/2,FS10000,LT9000",
            "excluded_products": "",
            "choices": ["S", "H", "U", "T"],
            "adders": {"S": 0, "H": 110, "U": 85, "T": 150},
            "rules": None
        },
        {
            "name": "Voltage",
            "description": "Voltage configuration",
            "price": 0.0,
            "price_type": "fixed",
            "category": "voltage",
            "product_families": "LS2000,LS7000,LS8000,LS8000/2,FS10000,LT9000",
            "excluded_products": "",
            "choices": ["115VAC", "230VAC", "24VDC"],
            "adders": {"115VAC": 0, "230VAC": 0, "24VDC": 0},
            "rules": None
        },
        {
            "name": "Probe Length",
            "description": "Probe length in inches",
            "price": 0.0,
            "price_type": "per_inch",
            "category": "length",
            "product_families": "LS2000,LS7000,LS8000,LS8000/2,FS10000,LT9000",
            "excluded_products": "",
            "choices": [],
            "adders": {},
            "rules": None
        }
    ]
    
    db = next(get_db())
    try:
        for option_data in options:
            option = Option(**option_data)
            db.add(option)
        db.commit()
        print(f"Created {len(options)} product options")
    finally:
        db.close()

def main():
    """Main rebuild process."""
    print("=== CLEAN DATABASE REBUILD ===")
    print("This will completely destroy and recreate your database.")
    print("All existing data will be lost.")
    
    response = input("Are you sure you want to continue? (yes/no): ")
    if response.lower() != "yes":
        print("Rebuild cancelled.")
        return
    
    try:
        # Step 1: Drop all tables
        drop_all_tables()
        
        # Step 2: Create all tables
        create_all_tables()
        
        # Step 3: Seed data in correct order
        seed_product_families()
        seed_base_models()
        seed_materials()
        seed_material_options()
        seed_voltage_options()
        seed_options()
        
        print("\n=== DATABASE REBUILD COMPLETE ===")
        print("All tables have been created and populated with fresh data.")
        print("The database is now ready for use.")
        
    except Exception as e:
        print(f"Error during rebuild: {e}")
        print("Database rebuild failed. Please check the error and try again.")
        return

if __name__ == "__main__":
    main() 