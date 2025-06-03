"""
Database population service.
Populates the database with initial data from the price list.
"""
import os
import logging
from pathlib import Path

from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.core.models import (
    Material,
    StandardLength,
    MaterialAvailability,
    ProductFamily,
    ProductVariant,
    Option,
    Customer,
    SparePart,
    ConnectionOption
)

# Set up logging
logger = logging.getLogger(__name__)

def populate_materials(db: Session):
    """Populate materials table with initial data."""
    # Check if materials already exist
    existing_count = db.query(Material).count()
    if existing_count > 0:
        logger.info(f"Materials table already has {existing_count} records. Skipping population.")
        return
    
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
    logger.info(f"Added {len(materials)} materials")

def populate_standard_lengths(db: Session):
    """Populate standard lengths for materials with non-standard length surcharges."""
    # Check if standard lengths already exist
    existing_count = db.query(StandardLength).count()
    if existing_count > 0:
        logger.info(f"StandardLength table already has {existing_count} records. Skipping population.")
        return
        
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
    logger.info(f"Added {len(standard_lengths)} standard lengths")

def populate_material_availability(db: Session):
    """Populate material availability for different product types."""
    # Check if material availability records already exist
    existing_count = db.query(MaterialAvailability).count()
    if existing_count > 0:
        logger.info(f"MaterialAvailability table already has {existing_count} records. Skipping population.")
        return
    
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
    logger.info(f"Added {len(availability_records)} material availability records")

def populate_from_price_list(db: Session):
    """Populate the database with data from the price list."""
    # This function would parse the price_list.txt file and populate the database
    # For now, we'll just populate with sample data
    
    # Check if product families already exist
    existing_count = db.query(ProductFamily).count()
    if existing_count > 0:
        logger.info(f"ProductFamily table already has {existing_count} records. Skipping population.")
        return

    # Sample product families
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
    logger.info(f"Added {len(families)} product families")
    
    # Add a few sample product variants for LS2000
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
    ]
    
    # Add variants to database
    db.add_all(variants)
    db.commit()
    logger.info(f"Added {len(variants)} product variants")

def populate_options(db: Session):
    """Populate options table with initial data."""
    # Check if options already exist
    existing_count = db.query(Option).count()
    if existing_count > 0:
        logger.info(f"Option table already has {existing_count} records. Skipping population.")
        return
        
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
    ]
    
    # Add options to database
    db.add_all(options)
    db.commit()
    logger.info(f"Added {len(options)} options")

def populate_sample_customers(db: Session):
    """Populate customers table with sample data."""
    # Check if customers already exist
    existing_count = db.query(Customer).count()
    if existing_count > 0:
        logger.info(f"Customer table already has {existing_count} records. Skipping population.")
        return
        
    customers = [
        Customer(
            name="Acme Industries",
            contact_name="John Doe",
            email="john.doe@acme.com",
            phone="555-123-4567",
            address="123 Main St, Anytown, USA",
        ),
        Customer(
            name="XYZ Corporation",
            contact_name="Jane Smith",
            email="jane.smith@xyz.com",
            phone="555-987-6543",
            address="456 Oak Ave, Somecity, USA",
        ),
    ]
    
    # Add customers to database
    db.add_all(customers)
    db.commit()
    logger.info(f"Added {len(customers)} sample customers")

def remove_obsolete_products(db: Session):
    """
    Remove ultrasonic and radar products from the database as they are no longer offered.
    This reflects the information from additional_info.txt that states 
    "We no longer offer Ultrasonic or Radar".
    """
    # Find and remove all product families with ultrasonic or radar in their name or description
    obsolete_families = db.query(ProductFamily).filter(
        (ProductFamily.name.ilike("%ultrasonic%")) |
        (ProductFamily.description.ilike("%ultrasonic%")) |
        (ProductFamily.name.ilike("%radar%")) |
        (ProductFamily.description.ilike("%radar%")) |
        (ProductFamily.category.ilike("%ultrasonic%")) |
        (ProductFamily.category.ilike("%radar%"))
    ).all()
    
    # Log the families to be removed
    for family in obsolete_families:
        logger.info(f"Removing obsolete product family: {family.name} - {family.description}")
        
        # Delete associated product variants first
        variants = db.query(ProductVariant).filter(
            ProductVariant.product_family_id == family.id
        ).all()
        
        for variant in variants:
            logger.info(f"Removing obsolete product variant: {variant.model_number}")
            db.delete(variant)
        
        # Now delete the family
        db.delete(family)
    
    # Commit changes
    db.commit()
    logger.info(f"Removed {len(obsolete_families)} obsolete product families and their variants")

def populate_spare_parts(db: Session):
    """Populate spare parts table with initial data."""
    # Check if spare parts already exist
    existing_count = db.query(SparePart).count()
    if existing_count > 0:
        logger.info(f"SparePart table already has {existing_count} records. Skipping population.")
        return
        
    # Get product families to associate spare parts with
    product_families = db.query(ProductFamily).all()
    product_family_map = {family.name: family.id for family in product_families}
    
    # Spare parts data structured by product family and category
    spare_parts_data = [
        # LS2000 spare parts
        {
            "product_family": "LS2000",
            "part_number": "LS2000-ELECTRONICS",
            "name": "Electronics Assembly",
            "description": "Electronics circuit board assembly for LS2000",
            "price": 265.0,
            "category": "electronics"
        },
        {
            "product_family": "LS2000",
            "part_number": "LS2000-S-PROBE-10",
            "name": "Stainless Steel Probe Assembly - 10\"",
            "description": "10\" 316 Stainless Steel probe assembly for LS2000",
            "price": 195.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LS2000",
            "part_number": "LS2000-U-PROBE-4",
            "name": "UHMWPE Blind End Probe Assembly - 4\"",
            "description": "4\" UHMWPE blind end probe assembly for LS2000",
            "price": 210.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LS2000",
            "part_number": "LS2000-T-PROBE-4",
            "name": "Teflon Blind End Probe Assembly - 4\"",
            "description": "4\" Teflon blind end probe assembly for LS2000",
            "price": 250.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LS2000",
            "part_number": "LS2000-H-PROBE-10",
            "name": "Halar Coated Probe Assembly - 10\"",
            "description": "10\" Halar coated probe assembly for LS2000",
            "price": 320.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LS2000",
            "part_number": "LS2000-HOUSING",
            "name": "Standard Housing",
            "description": "Standard housing for LS2000",
            "price": 100.0,
            "category": "housing"
        },
        # LS2100 spare parts
        {
            "product_family": "LS2100",
            "part_number": "LS2100-ELECTRONICS",
            "name": "Loop Powered Electronics Assembly",
            "description": "Loop powered electronics circuit board assembly for LS2100",
            "price": 225.0,
            "category": "electronics"
        },
        {
            "product_family": "LS2100",
            "part_number": "LS2100-S-PROBE-10",
            "name": "Stainless Steel Probe Assembly - 10\"",
            "description": "10\" 316 Stainless Steel probe assembly for LS2100",
            "price": 220.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LS2100",
            "part_number": "LS2100-H-PROBE-10",
            "name": "Halar Coated Probe Assembly - 10\"",
            "description": "10\" Halar coated probe assembly for LS2100",
            "price": 330.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LS2100",
            "part_number": "LS2100-HOUSING",
            "name": "Standard Housing",
            "description": "Standard housing for LS2100",
            "price": 120.0,
            "category": "housing"
        },
        # LS6000 spare parts
        {
            "product_family": "LS6000",
            "part_number": "LS6000-ELECTRONICS",
            "name": "Electronics Assembly",
            "description": "Electronics circuit board assembly for LS6000",
            "price": 295.0,
            "category": "electronics"
        },
        {
            "product_family": "LS6000",
            "part_number": "LS6000-S-PROBE-10",
            "name": "Stainless Steel Probe Assembly - 10\"",
            "description": "10\" 316 Stainless Steel probe assembly for LS6000",
            "price": 240.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LS6000",
            "part_number": "LS6000-H-PROBE-10",
            "name": "Halar Coated Probe Assembly - 10\"",
            "description": "10\" Halar coated probe assembly for LS6000",
            "price": 370.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LS6000",
            "part_number": "LS6000-HOUSING",
            "name": "Standard Housing",
            "description": "Standard housing for LS6000",
            "price": 140.0,
            "category": "housing"
        },
        
        # LS7000 spare parts
        {
            "product_family": "LS7000",
            "part_number": "LS7000-PS",
            "name": "Power Supply",
            "description": "Power supply for LS7000 (specify voltage when ordering)",
            "price": 230.0,
            "category": "electronics"
        },
        {
            "product_family": "LS7000",
            "part_number": "LS7000/2-DP",
            "name": "Dual Point Card",
            "description": "Dual point electronics card for LS7000/2",
            "price": 255.0,
            "category": "electronics"
        },
        {
            "product_family": "LS7000",
            "part_number": "LS7000-H-PROBE-10",
            "name": "Halar Coated Probe Assembly - 10\"",
            "description": "10\" Halar coated probe assembly for LS7000",
            "price": 370.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LS7000",
            "part_number": "LS7000-HOUSING",
            "name": "Standard Housing",
            "description": "Standard housing for LS7000",
            "price": 140.0,
            "category": "housing"
        },
        {
            "product_family": "LS7000",
            "part_number": "FUSE-1/2AMP",
            "name": "Fuse - 1/2 AMP",
            "description": "Replacement 1/2 AMP fuse for LS7000",
            "price": 10.0,
            "category": "electronics"
        },
        
        # LT9000 spare parts
        {
            "product_family": "LT9000",
            "part_number": "LT9000-MA",
            "name": "MA Plug-in Card",
            "description": "Milliamp output plug-in card for LT9000",
            "price": 295.0,
            "category": "electronics"
        },
        {
            "product_family": "LT9000",
            "part_number": "LT9000-BB",
            "name": "Power Supply",
            "description": "Power supply for LT9000 (specify voltage when ordering)",
            "price": 295.0,
            "category": "electronics"
        },
        {
            "product_family": "LT9000",
            "part_number": "LT9000-H-PROBE-10",
            "name": "Halar Coated Probe Assembly - 10\"",
            "description": "10\" Halar coated probe assembly for LT9000",
            "price": 370.0,
            "category": "probe_assembly"
        },
        {
            "product_family": "LT9000",
            "part_number": "LT9000-HOUSING",
            "name": "Standard Housing",
            "description": "Standard housing for LT9000",
            "price": 140.0,
            "category": "housing"
        },
        {
            "product_family": "LT9000",
            "part_number": "FUSE-1/2AMP",
            "name": "Fuse - 1/2 AMP",
            "description": "Replacement 1/2 AMP fuse for LT9000",
            "price": 10.0,
            "category": "electronics"
        },
    ]
    
    # Create spare parts objects
    spare_parts = []
    for part_data in spare_parts_data:
        product_family_id = product_family_map.get(part_data["product_family"])
        
        if product_family_id is None:
            logger.warning(f"Product family {part_data['product_family']} not found for spare part {part_data['part_number']}")
            continue
            
        spare_part = SparePart(
            part_number=part_data["part_number"],
            name=part_data["name"],
            description=part_data["description"],
            price=part_data["price"],
            product_family_id=product_family_id,
            category=part_data["category"]
        )
        spare_parts.append(spare_part)
    
    # Add spare parts to database
    db.add_all(spare_parts)
    db.commit()
    logger.info(f"Added {len(spare_parts)} spare parts")

def populate_connection_options(db: Session):
    """Populate connection options table with detailed flange and Tri-Clamp options."""
    existing_count = db.query(ConnectionOption).count()
    if existing_count > 0:
        logger.info(f"ConnectionOption table already has {existing_count} records. Skipping population.")
        return

    options = [
        # Flange 150#
        {"type": "Flange", "rating": "150#", "size": '1"', "price": 0.0, "product_families": "LS2000,LS6000"},
        {"type": "Flange", "rating": "150#", "size": '1.5"', "price": 0.0, "product_families": "LS2000,LS6000"},
        {"type": "Flange", "rating": "150#", "size": '2"', "price": 0.0, "product_families": "LS2000,LS6000"},
        {"type": "Flange", "rating": "150#", "size": '3"', "price": 0.0, "product_families": "LS2000,LS6000"},
        {"type": "Flange", "rating": "150#", "size": '4"', "price": 0.0, "product_families": "LS2000,LS6000"},
        # Flange 300#
        {"type": "Flange", "rating": "300#", "size": '1"', "price": 0.0, "product_families": "LS2000,LS6000"},
        {"type": "Flange", "rating": "300#", "size": '1.5"', "price": 0.0, "product_families": "LS2000,LS6000"},
        {"type": "Flange", "rating": "300#", "size": '2"', "price": 0.0, "product_families": "LS2000,LS6000"},
        {"type": "Flange", "rating": "300#", "size": '3"', "price": 0.0, "product_families": "LS2000,LS6000"},
        {"type": "Flange", "rating": "300#", "size": '4"', "price": 0.0, "product_families": "LS2000,LS6000"},
        # Tri-Clamp
        {"type": "Tri-Clamp", "rating": None, "size": '1.5"', "price": 280.0, "product_families": "LS2000,LS6000"},
        {"type": "Tri-Clamp", "rating": None, "size": '2"', "price": 330.0, "product_families": "LS2000,LS6000"},
    ]
    db.add_all([ConnectionOption(**opt) for opt in options])
    db.commit()
    logger.info(f"Added {len(options)} connection options")

def populate_database():
    """Populate the database with initial data."""
    db = SessionLocal()
    try:
        populate_materials(db)
        populate_standard_lengths(db)
        populate_material_availability(db)
        populate_from_price_list(db)
        populate_options(db)
        populate_sample_customers(db)
        remove_obsolete_products(db)
        populate_spare_parts(db)
        populate_connection_options(db)
        logger.info("Database population completed successfully")
    except Exception as e:
        logger.error(f"Error populating database: {e}")
    finally:
        db.close() 