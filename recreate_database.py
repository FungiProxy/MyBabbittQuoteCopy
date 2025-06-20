#!/usr/bin/env python3
"""
Comprehensive database recreation script.
This will drop all tables and recreate them with complete business data.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal, init_db, engine
from src.core.models.option import Option
from src.core.models.product_variant import ProductFamily
from src.core.models.material import Material, StandardLength
from src.core.models.connection_option import ConnectionOption
from src.core.models.voltage_option import VoltageOption
from src.core.models.material_option import MaterialOption
from src.core.models.housing_type_option import HousingTypeOption
from src.core.models.housing_type import HousingType
from src.core.models.o_ring_material_option import O_RingMaterialOption
from src.core.models.exotic_metal_option import ExoticMetalOption
from src.core.models.probe_length_option import ProbeLengthOption
from src.core.models.cable_length_option import CableLengthOption
from sqlalchemy import text


def drop_all_tables():
    """Drop all tables in the database."""
    print("Dropping all tables...")
    
    # Get all table names
    with engine.connect() as conn:
        # Get all table names
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result if row[0] != 'sqlite_sequence']
        
        # Drop all tables
        for table in tables:
            conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
            print(f"Dropped table: {table}")
        
        conn.commit()
    print("All tables dropped successfully!")


def recreate_database():
    """Recreate the database with all proper data."""
    print("Recreating database...")
    
    # Initialize database (creates all tables)
    init_db()
    print("Database tables created!")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # 1. Add Product Families
        print("Adding product families...")
        product_families = [
            ProductFamily(name='LS2000', description='LS2000 Level Switch', category='Point Level Switch'),
            ProductFamily(name='LS2100', description='LS2100 Level Switch', category='Point Level Switch'),
            ProductFamily(name='LS6000', description='LS6000 Level Switch', category='Point Level Switch'),
            ProductFamily(name='LS7000', description='LS7000 Level Switch', category='Point Level Switch'),
            ProductFamily(name='LS7000/2', description='LS7000/2 Level Switch', category='Multi-Point Level Switch'),
            ProductFamily(name='LS8000', description='LS8000 Level Switch', category='Point Level Switch'),
            ProductFamily(name='LS8000/2', description='LS8000/2 Level Switch', category='Multi-Point Level Switch'),
            ProductFamily(name='LT9000', description='LT9000 Level Switch', category='Continuous Level Transmitter'),
            ProductFamily(name='FS10000', description='FS10000 Level Switch', category='Flow Switch'),
            ProductFamily(name='LS7500', description='LS7500 Integral Flange Sensor', category='Presence/Absence Switch'),
            ProductFamily(name='LS8500', description='LS8500 Remote Mount Flange Sensor', category='Presence/Absence Switch'),
        ]
        db.add_all(product_families)
        db.commit()
        print(f"Added {len(product_families)} product families")

        # 2. Add Materials
        print("Adding materials...")
        materials = [
            Material(code='S', name='316 Stainless Steel', description='Standard 316SS probe', 
                    base_length=10.0, length_adder_per_inch=0, length_adder_per_foot=45.0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=0.0),
            Material(code='H', name='Halar Coated', description='Halar coated probe', 
                    base_length=10.0, length_adder_per_inch=0, length_adder_per_foot=110.0, 
                    has_nonstandard_length_surcharge=True, nonstandard_length_surcharge=300.0, base_price_adder=110.0),
            Material(code='TS', name='Teflon Sleeve', description='Teflon sleeve probe', 
                    base_length=10.0, length_adder_per_inch=0, length_adder_per_foot=110.0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=110.0),
            Material(code='U', name='UHMWPE Blind End', description='UHMWPE blind end probe', 
                    base_length=4.0, length_adder_per_inch=40.0, length_adder_per_foot=0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=20.0),
            Material(code='T', name='Teflon Blind End', description='Teflon blind end probe', 
                    base_length=4.0, length_adder_per_inch=50.0, length_adder_per_foot=0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=60.0),
            Material(code='C', name='Cable', description='Cable probe', 
                    base_length=12.0, length_adder_per_inch=0, length_adder_per_foot=45.0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=80.0),
            Material(code='CPVC', name='CPVC Blind End', description='CPVC blind end probe', 
                    base_length=4.0, length_adder_per_inch=50.0, length_adder_per_foot=0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=400.0),
            Material(code='A', name='Alloy 20', description='Exotic metal', 
                    base_length=10.0, length_adder_per_inch=0, length_adder_per_foot=0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=0.0),
            Material(code='HB', name='Hastelloy-B', description='Exotic metal', 
                    base_length=10.0, length_adder_per_inch=0, length_adder_per_foot=0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=0.0),
            Material(code='HC', name='Hastelloy-C-276', description='Exotic metal', 
                    base_length=10.0, length_adder_per_inch=0, length_adder_per_foot=0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=0.0),
            Material(code='TT', name='Titanium', description='Exotic metal', 
                    base_length=10.0, length_adder_per_inch=0, length_adder_per_foot=0, 
                    has_nonstandard_length_surcharge=False, nonstandard_length_surcharge=0.0, base_price_adder=0.0),
        ]
        db.add_all(materials)
        db.commit()
        print(f"Added {len(materials)} materials")

        # 3. Add Standard Lengths
        print("Adding standard lengths...")
        standard_lengths = [
            # H material standard lengths
            StandardLength(material_code='H', length=6.0),
            StandardLength(material_code='H', length=12.0),
            StandardLength(material_code='H', length=18.0),
            StandardLength(material_code='H', length=24.0),
            StandardLength(material_code='H', length=36.0),
            StandardLength(material_code='H', length=48.0),
            StandardLength(material_code='H', length=60.0),
            StandardLength(material_code='H', length=72.0),
            StandardLength(material_code='H', length=84.0),
            # S material standard lengths
            StandardLength(material_code='S', length=6.0),
            StandardLength(material_code='S', length=12.0),
            StandardLength(material_code='S', length=18.0),
            StandardLength(material_code='S', length=24.0),
            StandardLength(material_code='S', length=36.0),
            StandardLength(material_code='S', length=48.0),
            StandardLength(material_code='S', length=60.0),
            StandardLength(material_code='S', length=72.0),
            StandardLength(material_code='S', length=84.0),
        ]
        db.add_all(standard_lengths)
        db.commit()
        print(f"Added {len(standard_lengths)} standard lengths")

        # 4. Add Housing Types
        print("Adding housing types...")
        housing_types = [
            HousingType(name='Standard', description='Standard housing'),
            HousingType(name='Explosion Proof', description='Explosion proof housing'),
            HousingType(name='Weatherproof', description='Weatherproof housing'),
        ]
        db.add_all(housing_types)
        db.commit()
        print(f"Added {len(housing_types)} housing types")

        # 5. Add Complete Options with choices and adders
        print("Adding complete options...")
        options = [
            # Material Options for LS2000
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['S', 'H', 'TS', 'U', 'T', 'C'],
                adders={'S': 0, 'H': 110, 'TS': 110, 'U': 20, 'T': 60, 'C': 80},
                product_families='LS2000',
            ),
            # Material Options for LS2100
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['S', 'H', 'TS', 'U', 'T', 'C'],
                adders={'S': 0, 'H': 110, 'TS': 110, 'U': 20, 'T': 60, 'C': 80},
                product_families='LS2100',
            ),
            # Material Options for LS6000
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['S', 'H', 'TS', 'U', 'T', 'C', 'CPVC'],
                adders={'S': 0, 'H': 110, 'TS': 110, 'U': 20, 'T': 60, 'C': 80, 'CPVC': 400},
                product_families='LS6000',
            ),
            # Material Options for LS7000
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['S', 'H', 'TS', 'T', 'U', 'CPVC'],
                adders={'S': 0, 'H': 110, 'TS': 110, 'U': 20, 'T': 60, 'C': 80, 'CPVC': 400},
                product_families='LS7000',
            ),
            # Material Options for LS7000/2
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['H', 'TS'],
                adders={'H': 0, 'TS': 0},
                product_families='LS7000/2',
            ),
            # Material Options for LS8000
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['S', 'H', 'TS', 'C'],
                adders={'S': 0, 'H': 110, 'TS': 110, 'C': 80},
                product_families='LS8000',
            ),
            # Material Options for LS8000/2
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['H', 'TS'],
                adders={'H': 110, 'TS': 110},
                product_families='LS8000/2',
            ),
            # Material Options for LT9000
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['H', 'TS'],
                adders={'H': 0, 'TS': 0},
                product_families='LT9000',
            ),
            # Material Options for FS10000
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['S'],
                adders={'S': 0},
                product_families='FS10000',
            ),
            # Material Options for Presence/Absence Switches
            Option(
                name='Material',
                description='Probe material selection',
                price=0.0,
                price_type='fixed',
                category='Material',
                choices=['S'],
                adders={'S': 0},
                product_families='LS7500,LS8500',
            ),
            # O-Ring Materials
            Option(
                name='O-Rings',
                description='O-Ring material selection',
                price=0.0,
                price_type='fixed',
                category='O-ring Material',
                choices=['Viton', 'Silicon', 'Buna-N', 'EPDM', 'PTFE', 'Kalrez'],
                adders={'Viton': 0, 'Silicon': 0, 'Buna-N': 0, 'EPDM': 0, 'PTFE': 0, 'Kalrez': 295},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            # Exotic Metals
            Option(
                name='Exotic Metal',
                description='Exotic metal material selection',
                price=0.0,
                price_type='fixed',
                category='Exotic Metal',
                choices=['None', 'Alloy 20', 'Hastelloy-C-276', 'Hastelloy-B', 'Titanium'],
                adders={'None': 0, 'Alloy 20': 0, 'Hastelloy-C-276': 0, 'Hastelloy-B': 0, 'Titanium': 0},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            # Voltage Options for LS2000
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['115VAC', '24VDC'],
                adders={'115VAC': 0, '24VDC': 0},
                product_families='LS2000',
            ),
            # Voltage Options for LS2100
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['24VDC'],
                adders={'24VDC': 0},
                product_families='LS2100',
            ),
            # Voltage Options for LS6000
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['115VAC', '230VAC', '12VDC', '24VDC'],
                adders={'115VAC': 0, '230VAC': 0, '12VDC': 0, '24VDC': 0},
                product_families='LS6000',
            ),
            # Voltage Options for LS7000
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['115VAC', '230VAC', '12VDC', '24VDC'],
                adders={'115VAC': 0, '230VAC': 0, '12VDC': 0, '24VDC': 0},
                product_families='LS7000',
            ),
            # Voltage Options for LS7000/2
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['115VAC', '230VAC', '12VDC', '24VDC'],
                adders={'115VAC': 0, '230VAC': 0, '12VDC': 0, '24VDC': 0},
                product_families='LS7000/2',
            ),
            # Voltage Options for LS8000
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['115VAC', '230VAC', '12VDC', '24VDC'],
                adders={'115VAC': 0, '230VAC': 0, '12VDC': 0, '24VDC': 0},
                product_families='LS8000',
            ),
            # Voltage Options for LS8000/2
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['115VAC', '230VAC', '12VDC', '24VDC'],
                adders={'115VAC': 0, '230VAC': 0, '12VDC': 0, '24VDC': 0},
                product_families='LS8000/2',
            ),
            # Voltage Options for LT9000
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['115VAC', '230VAC', '24VDC'],
                adders={'115VAC': 0, '230VAC': 0, '24VDC': 0},
                product_families='LT9000',
            ),
            # Voltage Options for FS10000
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['115VAC', '230VAC'],
                adders={'115VAC': 0, '230VAC': 0},
                product_families='FS10000',
            ),
            # Voltage Options for LS7500, LS8500
            Option(
                name='Voltage',
                description='Supply voltage selection',
                price=0.0,
                price_type='fixed',
                category='Electrical',
                choices=['115VAC', '230VAC', '12VDC', '24VDC'],
                adders={'115VAC': 0, '230VAC': 0, '12VDC': 0, '24VDC': 0},
                product_families='LS7500,LS8500',
            ),
            # Connection Types
            Option(
                name='Connection Type',
                description='Primary connection type selection',
                price=0.0,
                price_type='fixed',
                category='Mechanical',
                choices=['NPT', 'Flange', 'Tri-clamp'],
                adders={'NPT': 0, 'Flange': 0, 'Tri-clamp': 0},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            # NPT Sizes for LS2000, LS2100
            Option(
                name='NPT Size',
                description='NPT connection size selection',
                price=0.0,
                price_type='fixed',
                category='Mechanical',
                choices=['3/4"'],
                adders={'3/4"': 0},
                product_families='LS2000,LS2100',
            ),
            # NPT Sizes for LS6000, LS7000
            Option(
                name='NPT Size',
                description='NPT connection size selection',
                price=0.0,
                price_type='fixed',
                category='Mechanical',
                choices=['1"', '3/4"'],
                adders={'1"': 0, '3/4"': 0},
                product_families='LS6000,LS7000',
            ),
            # Flange Types
            Option(
                name='Flange Type',
                description='Flange type selection',
                price=0.0,
                price_type='fixed',
                category='Mechanical',
                choices=['150#', '300#'],
                adders={'150#': 0, '300#': 0},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            # Flange Sizes
            Option(
                name='Flange Size',
                description='Flange size selection',
                price=0.0,
                price_type='fixed',
                category='Mechanical',
                choices=['1"', '1-1/2"', '2"', '3"', '4"'],
                adders={'1"': 0, '1-1/2"': 0, '2"': 0, '3"': 0, '4"': 0},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            # Tri-clamp
            Option(
                name='Tri-clamp',
                description='Tri-clamp selection',
                price=0.0,
                price_type='fixed',
                category='Mechanical',
                choices=['1-1/2" Tri-clamp Process Connection', '1-1/2" Tri-clamp Spud', '2" Tri-clamp Process Connection', '2" Tri-clamp Spud'],
                adders={'1-1/2" Tri-clamp Process Connection': 280.0, '1-1/2" Tri-clamp Spud': 170.0, '2" Tri-clamp Process Connection': 330.0, '2" Tri-clamp Spud': 220.0},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            # Insulator Options
            Option(
                name='Insulator',
                description='Insulator material selection',
                price=0.0,
                price_type='fixed',
                category='Mechanical',
                choices=['Delrin', 'Teflon', 'PEEK', 'Ceramic'],
                adders={'Delrin': 0, 'Teflon': 40, 'PEEK': 340, 'Ceramic': 470},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            # Miscellaneous Options
            Option(
                name='Extra Static Protection',
                description='Additional static protection for plastic pellets and resins',
                price=30.0,
                price_type='fixed',
                category='Electrical',
                choices=['Yes', 'No'],
                adders={'Yes': 30, 'No': 0},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            Option(
                name='Bent Probe',
                description='Bent probe configuration',
                price=50.0,
                price_type='fixed',
                category='Mechanical',
                choices=['Yes', 'No'],
                adders={'Yes': 50, 'No': 0},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            Option(
                name='Stainless Steel Tag',
                description='Stainless steel identification tag',
                price=30.0,
                price_type='fixed',
                category='Mechanical',
                choices=['Yes', 'No'],
                adders={'Yes': 30, 'No': 0},
                product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
            ),
            Option(
                name='3/4" Diameter Probe',
                description='3/4" diameter probe x 10"',
                price=175.0,
                price_type='fixed',
                category='Mechanical',
                choices=['Yes', 'No'],
                adders={'Yes': 175, 'No': 0},
                product_families='LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000',
            ),
            Option(
                name='Twisted Shielded Pair',
                description='22 AWG, twisted shielded pair',
                price=0.0,
                price_type='per_unit',
                category='Electrical',
                choices=['Yes', 'No'],
                adders={'Yes': 0.70, 'No': 0},
                product_families='LS8000,LS8000/2',
            ),
            Option(
                name='NEMA 4 Enclosure',
                description='8" x 6" x 3.5" NEMA 4 metal enclosure for receiver',
                price=245.0,
                price_type='fixed',
                category='Mechanical',
                choices=['Yes', 'No'],
                adders={'Yes': 245, 'No': 0},
                product_families='LS8000,LS8000/2',
            ),
            Option(
                name='Additional Coaxial Cable',
                description='Additional coaxial cable',
                price=0.0,
                price_type='per_unit',
                category='Electrical',
                choices=['Yes', 'No'],
                adders={'Yes': 6.0, 'No': 0},
                product_families='FS10000',
            ),
            Option(
                name='GRK Exp Proof Enclosure',
                description='GRK explosion proof enclosure for receiver',
                price=1030.0,
                price_type='fixed',
                category='Mechanical',
                choices=['Yes', 'No'],
                adders={'Yes': 1030, 'No': 0},
                product_families='LS8000,LS8000/2,FS10000',
            ),
        ]

        # Add all options
        for option in options:
            db.add(option)

        db.commit()
        print(f"Added {len(options)} complete options with choices and adders")

        print("\nDatabase recreation completed successfully!")
        print("The database now contains:")
        print(f"- {len(product_families)} product families")
        print(f"- {len(materials)} materials")
        print(f"- {len(standard_lengths)} standard lengths")
        print(f"- {len(housing_types)} housing types")
        print(f"- {len(options)} complete options with choices and adders")

    except Exception as e:
        db.rollback()
        print(f'Error recreating database: {e}')
        raise
    finally:
        db.close()


if __name__ == '__main__':
    print("Starting database recreation...")
    drop_all_tables()
    recreate_database()
    print("Database recreation completed!") 