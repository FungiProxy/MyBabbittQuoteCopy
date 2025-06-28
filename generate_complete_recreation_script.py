#!/usr/bin/env python3
"""
Generate a complete, self-contained database recreation script with all core business data embedded.
"""
import json
import os

def load_json_data(filename):
    """Load JSON data from file"""
    with open(f'db_snapshot/{filename}', 'r') as f:
        return json.load(f)

def format_python_data(data, var_name):
    """Format JSON data as Python list/dict"""
    return f"{var_name} = {repr(data)}"

def main():
    print("Generating complete database recreation script...")
    
    # Load all data
    options_data = load_json_data('options.json')
    product_families_data = load_json_data('product_families.json')
    product_family_options_data = load_json_data('product_family_options.json')
    base_models_data = load_json_data('base_models.json')
    materials_data = load_json_data('materials.json')
    length_adder_rules_data = load_json_data('length_adder_rules.json')
    spare_parts_data = load_json_data('spare_parts.json')
    standard_lengths_data = load_json_data('standard_lengths.json')
    
    # Generate the complete script
    script_content = f'''#!/usr/bin/env python3
"""
Recreate the full Babbitt database schema and data as of this snapshot.
This script is self-contained: it creates all relevant tables and inserts all data.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Text, Boolean, JSON, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from src.core.database import engine

# Embedded data from db_snapshot/*.json
{format_python_data(options_data, 'options_data')}

{format_python_data(product_families_data, 'product_families_data')}

{format_python_data(product_family_options_data, 'product_family_options_data')}

{format_python_data(base_models_data, 'base_models_data')}

{format_python_data(materials_data, 'materials_data')}

{format_python_data(length_adder_rules_data, 'length_adder_rules_data')}

{format_python_data(spare_parts_data, 'spare_parts_data')}

{format_python_data(standard_lengths_data, 'standard_lengths_data')}

def main():
    print("=== RECREATING FULL DATABASE ===")
    metadata = MetaData()
    
    # Drop all relevant tables
    with engine.connect() as conn:
        for table in [
            'options', 'product_families', 'product_family_options', 'base_models',
            'materials', 'length_adder_rules', 'spare_parts', 'standard_lengths']:
            conn.execute(text(f'DROP TABLE IF EXISTS {{table}}'))
        conn.commit()
    
    # Define all tables
    options = Table('options', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('description', Text),
        Column('price', Float, nullable=False),
        Column('price_type', String),
        Column('category', String),
        Column('excluded_products', String),
        Column('product_families', String),
        Column('choices', JSON),
        Column('adders', JSON),
        Column('rules', JSON),
    )
    
    product_families = Table('product_families', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('description', Text),
        Column('category', String),
        Column('base_model_number', String),
        Column('base_price', Float),
    )
    
    product_family_options = Table('product_family_options', metadata,
        Column('product_family_id', Integer, ForeignKey('product_families.id'), primary_key=True),
        Column('option_id', Integer, ForeignKey('options.id'), primary_key=True),
        Column('is_available', Integer),
        Column('family_specific_price', Float),
        Column('notes', Text),
    )
    
    base_models = Table('base_models', metadata,
        Column('id', Integer, primary_key=True),
        Column('product_family_id', Integer, ForeignKey('product_families.id'), nullable=False),
        Column('model_number', String, nullable=False),
        Column('description', Text, nullable=False),
        Column('base_price', Float, nullable=False),
        Column('base_length', Float, nullable=False),
        Column('voltage', String, nullable=False),
        Column('material', String, nullable=False),
    )
    
    materials = Table('materials', metadata,
        Column('id', Integer, primary_key=True),
        Column('code', String, nullable=False),
        Column('name', String, nullable=False),
        Column('description', Text),
        Column('base_length', Float, nullable=False),
        Column('length_adder_per_inch', Float),
        Column('length_adder_per_foot', Float),
        Column('has_nonstandard_length_surcharge', Boolean),
        Column('nonstandard_length_surcharge', Float),
        Column('base_price_adder', Float),
    )
    
    length_adder_rules = Table('length_adder_rules', metadata,
        Column('id', Integer, primary_key=True),
        Column('product_family', String, nullable=False),
        Column('material_code', String, nullable=False),
        Column('adder_type', String, nullable=False),
        Column('first_threshold', Float, nullable=False),
        Column('adder_amount', Float, nullable=False),
        Column('description', Text),
    )
    
    spare_parts = Table('spare_parts', metadata,
        Column('id', Integer, primary_key=True),
        Column('part_number', String, nullable=False),
        Column('name', String, nullable=False),
        Column('description', Text),
        Column('price', Float, nullable=False),
        Column('product_family_id', Integer, ForeignKey('product_families.id')),
        Column('category', String),
    )
    
    standard_lengths = Table('standard_lengths', metadata,
        Column('id', Integer, primary_key=True),
        Column('material_code', String, nullable=False),
        Column('length', Float, nullable=False),
    )
    
    # Create all tables
    metadata.create_all(engine)
    
    # Insert all data
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        print("Inserting options...")
        session.execute(options.insert(), options_data)
        
        print("Inserting product families...")
        session.execute(product_families.insert(), product_families_data)
        
        print("Inserting product family options...")
        session.execute(product_family_options.insert(), product_family_options_data)
        
        print("Inserting base models...")
        session.execute(base_models.insert(), base_models_data)
        
        print("Inserting materials...")
        session.execute(materials.insert(), materials_data)
        
        print("Inserting length adder rules...")
        session.execute(length_adder_rules.insert(), length_adder_rules_data)
        
        print("Inserting spare parts...")
        session.execute(spare_parts.insert(), spare_parts_data)
        
        print("Inserting standard lengths...")
        session.execute(standard_lengths.insert(), standard_lengths_data)
        
        session.commit()
        print("Database recreation complete!")
        print(f"Inserted:")
        print(f"  - {len(options_data)} options")
        print(f"  - {len(product_families_data)} product families")
        print(f"  - {len(product_family_options_data)} product family options")
        print(f"  - {len(base_models_data)} base models")
        print(f"  - {len(materials_data)} materials")
        print(f"  - {len(length_adder_rules_data)} length adder rules")
        print(f"  - {len(spare_parts_data)} spare parts")
        print(f"  - {len(standard_lengths_data)} standard lengths")
        
    except Exception as e:
        print(f"Error during data insertion: {{e}}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == '__main__':
    main()
'''
    
    # Write the complete script
    with open('recreate_full_database.py', 'w') as f:
        f.write(script_content)
    
    print(f"Complete database recreation script generated: recreate_full_database.py")
    print(f"Total data records: {len(options_data) + len(product_families_data) + len(product_family_options_data) + len(base_models_data) + len(materials_data) + len(length_adder_rules_data) + len(spare_parts_data) + len(standard_lengths_data)}")

if __name__ == '__main__':
    main() 