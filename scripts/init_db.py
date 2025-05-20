"""
Database initialization and seeding script.

This script creates the database and populates it with initial data.
Run this script during development to create a pre-populated database.
"""
import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session

from src.core.database import SessionLocal, init_db
from src.core.models import (
    Customer,
    Material,
    Option,
    ProductFamily,
    ProductVariant,
    StandardLength,
    MaterialAvailability,
)


def populate_materials(db: Session):
    """Populate materials table with initial data."""
    materials = [
        Material(
            code="S",
            name="316 Stainless Steel",
            description="Standard 316 stainless steel probe",
            base_length=10.0,
            length_adder_per_inch=None,
            length_adder_per_foot=45.0,
            has_nonstandard_length_surcharge=False,
        ),
        Material(
            code="H",
            name="Halar Coated",
            description="Halar coated probe",
            base_length=10.0,
            length_adder_per_inch=None,
            length_adder_per_foot=110.0,
            has_nonstandard_length_surcharge=True,
            nonstandard_length_surcharge=300.0,
        ),
        Material(
            code="U",
            name="UHMWPE Blind End",
            description="UHMWPE blind end probe",
            base_length=4.0,
            length_adder_per_inch=40.0,
            base_price_adder=20.0,  # $20 adder to S base price
        ),
        Material(
            code="T",
            name="Teflon Blind End",
            description="Teflon blind end probe",
            base_length=4.0,
            length_adder_per_inch=50.0,
            base_price_adder=60.0,  # $60 adder to S base price
        ),
        Material(
            code="TS",
            name="Teflon Sleeve",
            description="Teflon sleeve probe",
            base_length=10.0,
            length_adder_per_foot=110.0,  # Same as Halar
            has_nonstandard_length_surcharge=False,
        ),
        Material(
            code="CPVC",
            name="CPVC Blind End",
            description="CPVC blind end probe with integrated NPT nipple",
            base_length=4.0,
            length_adder_per_inch=50.0,
        ),
    ]
    
    # Add materials to database
    db.add_all(materials)
    db.commit()
    print(f"Added {len(materials)} materials")


def populate_standard_lengths(db: Session):
    """Populate standard lengths for materials with non-standard length surcharges."""
    # Standard lengths for H material (Halar Coated)
    standard_lengths = [
        StandardLength(material_code="H", length=6.0),
        StandardLength(material_code="H", length=8.0),
        StandardLength(material_code="H", length=10.0),
        StandardLength(material_code="H", length=12.0),
        StandardLength(material_code="H", length=16.0),
        StandardLength(material_code="H", length=24.0),
        StandardLength(material_code="H", length=36.0),
        StandardLength(material_code="H", length=48.0),
        StandardLength(material_code="H", length=60.0),
        StandardLength(material_code="H", length=72.0),
    ]
    
    # Add standard lengths to database
    db.add_all(standard_lengths)
    db.commit()
    print(f"Added {len(standard_lengths)} standard lengths")


def populate_material_availability(db: Session):
    """Populate material availability for different product types."""
    # Define all product types
    product_types = [
        "LS2000", "LS2100", "LS6000", "LS7000", "LS7000/2", 
        "LS8000", "LS8000/2", "LT9000", "FS10000"
    ]
    
    # Define all materials
    materials = ["S", "H", "U", "T", "TS", "CPVC"]
    
    # Create availability records
    availability_records = []
    
    # For most product types, all materials are available
    for product_type in product_types:
        for material in materials:
            is_available = True
            notes = None
            
            # Special cases based on additional_info.txt
            if product_type in ["LS7000/2", "FS10000"] and material in ["U", "T"]:
                is_available = False
                notes = "U and T materials are not available for dual point switches and FS10000"
                
            availability_records.append(
                MaterialAvailability(
                    material_code=material,
                    product_type=product_type,
                    is_available=is_available,
                    notes=notes
                )
            )
    
    # Add availability records to database
    db.add_all(availability_records)
    db.commit()
    print(f"Added {len(availability_records)} material availability records")


def populate_product_families(db: Session):
    """Populate product families table with initial data."""
    families = [
        ProductFamily(
            name="LS2000",
            description="LS 2000 LEVEL SWITCH",
            category="Level Switch",
        ),
        ProductFamily(
            name="LS2100",
            description="LS 2100 LOOP POWERED LEVEL SWITCH",
            category="Level Switch",
        ),
        ProductFamily(
            name="LS6000",
            description="LS 6000 LEVEL SWITCH",
            category="Level Switch",
        ),
        ProductFamily(
            name="LS7000",
            description="LS 7000 LEVEL SWITCH",
            category="Level Switch",
        ),
        ProductFamily(
            name="LS7000/2",
            description="LS 7000/2 DUAL POINT LEVEL SWITCH",
            category="Level Switch",
        ),
        ProductFamily(
            name="LS8000",
            description="LS 8000 REMOTE MOUNTED LEVEL SWITCH",
            category="Level Switch",
        ),
        ProductFamily(
            name="LS8000/2",
            description="LS 8000/2 REMOTE MOUNTED DUAL POINT LEVEL SWITCH",
            category="Level Switch",
        ),
        ProductFamily(
            name="LT9000",
            description="LT 9000 LEVEL TRANSMITTER",
            category="Level Transmitter",
        ),
        ProductFamily(
            name="FS10000",
            description="FS 10000 DRY MATERIAL FLOW SWITCH",
            category="Flow Switch",
        ),
    ]
    
    # Add families to database
    db.add_all(families)
    db.commit()
    print(f"Added {len(families)} product families")


def populate_product_variants(db: Session):
    """Populate product variants table with initial data."""
    # This is a simplified version - the actual implementation would parse the price list
    # and create variants for each product family with different materials and voltages
    
    # Get product family IDs
    ls2000 = db.query(ProductFamily).filter(ProductFamily.name == "LS2000").first()
    
    variants = [
        ProductVariant(
            product_family_id=ls2000.id,
            model_number="LS2000-115VAC-S-10\"",
            description="LS 2000 level switch with 115VAC power and 10\" 316SS probe",
            base_price=425.0,
            base_length=10.0,
            voltage="115VAC",
            material="S",
        ),
        ProductVariant(
            product_family_id=ls2000.id,
            model_number="LS2000-115VAC-H-10\"",
            description="LS 2000 level switch with 115VAC power and 10\" Halar coated probe",
            base_price=535.0,
            base_length=10.0,
            voltage="115VAC",
            material="H",
        ),
        ProductVariant(
            product_family_id=ls2000.id,
            model_number="LS2000-115VAC-U-4\"",
            description="LS 2000 level switch with 115VAC power and 4\" UHMWPE blind end probe",
            base_price=445.0,
            base_length=4.0,
            voltage="115VAC",
            material="U",
        ),
        ProductVariant(
            product_family_id=ls2000.id,
            model_number="LS2000-115VAC-T-4\"",
            description="LS 2000 level switch with 115VAC power and 4\" Teflon blind end probe",
            base_price=485.0,
            base_length=4.0,
            voltage="115VAC",
            material="T",
        ),
    ]
    
    # Add variants to database
    db.add_all(variants)
    db.commit()
    print(f"Added {len(variants)} product variants")


def populate_options(db: Session):
    """Populate options table with initial data."""
    options = [
        Option(
            name="TEFLON INSULATOR",
            description="Teflon insulator instead of UHMWPE",
            price=40.0,
            price_type="fixed",
            category="material",
            product_families="LS2000,LS6000",
        ),
        Option(
            name="EXTRA STATIC PROTECTION",
            description="Extra static protection",
            price=30.0,
            price_type="fixed",
            category="feature",
            product_families="LS2000",
        ),
        Option(
            name="CABLE PROBE",
            description="Cable probe",
            price=80.0,
            price_type="fixed",
            category="feature",
            product_families="LS2000,LS2100,LS6000,LS7000,LS8000",
        ),
        Option(
            name="BENT PROBE",
            description="Bent probe",
            price=50.0,
            price_type="fixed",
            category="feature",
            product_families="LS2000,LS2100,LS6000,LS7000,LS8000",
        ),
        Option(
            name="STAINLESS STEEL TAG",
            description="Stainless steel tag",
            price=30.0,
            price_type="fixed",
            category="feature",
            product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        ),
    ]
    
    # Add options to database
    db.add_all(options)
    db.commit()
    print(f"Added {len(options)} options")


def populate_sample_customers(db: Session):
    """Populate customers table with sample data."""
    customers = [
        Customer(
            name="John Smith",
            company="Acme Industries",
            email="john.smith@acme.com",
            phone="555-123-4567",
            address="123 Main St",
            city="Springfield",
            state="IL",
            zip_code="62701",
        ),
        Customer(
            name="Jane Doe",
            company="Tech Solutions",
            email="jane.doe@techsolutions.com",
            phone="555-987-6543",
            address="456 Oak Ave",
            city="Riverdale",
            state="NY",
            zip_code="10471",
        ),
    ]
    
    # Add customers to database
    db.add_all(customers)
    db.commit()
    print(f"Added {len(customers)} sample customers")


def populate_db():
    """Populate the database with initial data."""
    # Initialize database schema
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Populate tables
        populate_materials(db)
        populate_standard_lengths(db)
        populate_material_availability(db)
        populate_product_families(db)
        populate_product_variants(db)
        populate_options(db)
        populate_sample_customers(db)
        
        print("Database population complete.")
    except Exception as e:
        print(f"Error populating database: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    populate_db() 