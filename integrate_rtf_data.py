#!/usr/bin/env python3
"""
Database Integration Script for RTF Template Data

This script integrates the extracted RTF template data into the product database.
It processes the extracted JSON data and creates/updates product families, options,
and specifications in the database.
"""

import json
import re
import sys
import os
from typing import Dict, List, Any, Optional

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.base_model import BaseModel


def clean_rtf_artifacts(text: str) -> str:
    """Clean RTF formatting artifacts from extracted text."""
    if not text:
        return ""
    
    # Remove RTF control sequences and artifacts
    text = re.sub(r'\\[a-z]+\d*', '', text)
    text = re.sub(r'\\[{}]', '', text)
    text = re.sub(r'\\\'[0-9a-f]{2}', '', text)
    text = re.sub(r'\\\*\\[a-z]+', '', text)
    text = re.sub(r'\\[a-z]+\s*\{[^}]*\}', '', text)
    text = re.sub(r'{\\?[^}]*}', '', text)
    text = re.sub(r'\\[a-z]+', '', text)
    
    # Remove extra whitespace and clean up
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def extract_clean_specifications(rtf_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and clean specifications from RTF data."""
    cleaned = {}
    
    # Clean basic fields
    for field in ['supply_voltage', 'output_type', 'process_connection', 
                  'insulator_material', 'probe_material', 'housing_type', 
                  'delivery_info', 'terms', 'application_notes']:
        if rtf_data.get(field):
            cleaned[field] = clean_rtf_artifacts(rtf_data[field])
    
    # Clean special notes
    if rtf_data.get('special_notes'):
        cleaned['special_notes'] = [clean_rtf_artifacts(note) for note in rtf_data['special_notes']]
    
    # Keep numeric fields as-is
    for field in ['insulator_length', 'insulator_temp_rating', 'probe_diameter',
                  'base_price', 'length_adder_per_foot', 'max_pressure', 
                  'warranty_period']:
        if rtf_data.get(field) is not None:
            cleaned[field] = rtf_data[field]
    
    # Keep list fields
    if rtf_data.get('optional_items'):
        cleaned['optional_items'] = rtf_data['optional_items']
    
    return cleaned


def create_or_update_product_family(db, family_name: str, category: str = None) -> ProductFamily:
    """Create or get existing product family."""
    family = db.query(ProductFamily).filter_by(name=family_name).first()
    
    if not family:
        # Determine category based on product family
        if not category:
            if family_name.startswith('LS'):
                category = "Point Level Switch"
            elif family_name.startswith('LT'):
                category = "Continuous Level Transmitter"
            elif family_name.startswith('FS'):
                category = "Flow Switch"
            else:
                category = "Level Switch"
        
        family = ProductFamily(
            name=family_name,
            description=f"{family_name} from RTF templates",
            category=category
        )
        db.add(family)
        db.flush()
        print(f"Created product family: {family_name}")
    else:
        print(f"Found existing product family: {family_name}")
    
    return family


def create_insulator_option(db, insulator_spec: str) -> Optional[Option]:
    """Create insulator material option based on specification."""
    if not insulator_spec:
        return None
    
    # Extract material name from specification
    material_match = re.search(r'([A-Za-z]+)', insulator_spec)
    if not material_match:
        return None
    
    material_name = material_match.group(1)
    
    # Check if option already exists
    option = db.query(Option).filter_by(
        name="Insulator Material",
        category="Connections"
    ).first()
    
    if option:
        # Add new material to existing choices if not present
        if option.choices is None:
            option.choices = []
        if option.adders is None:
            option.adders = {}
        if material_name not in option.choices:
            option.choices.append(material_name)
            option.adders[material_name] = 0
            db.flush()
        return option
    else:
        # Create new option
        option = Option(
            name="Insulator Material",
            description="Insulator material selection",
            price=0.0,
            price_type="fixed",
            category="Connections",
            choices=[material_name],
            adders={material_name: 0}
        )
        db.add(option)
        db.flush()
        print(f"Created insulator option: {material_name}")
        return option


def create_length_adder_option(db, adder_amount: float) -> Optional[Option]:
    """Create length adder option if applicable."""
    if not adder_amount or adder_amount <= 0:
        return None
    
    # Check if option already exists
    option = db.query(Option).filter_by(
        name="Length Adder",
        category="Pricing"
    ).first()
    
    if option:
        if option.choices is None:
            option.choices = []
        if option.adders is None:
            option.adders = {}
        # Update existing option
        if "Extended" not in option.choices:
            option.choices.append("Extended")
        option.adders["Extended"] = adder_amount
        db.flush()
        return option
    else:
        # Create new option
        option = Option(
            name="Length Adder",
            description="Additional cost per foot for longer probes",
            price=adder_amount,
            price_type="per_foot",
            category="Pricing",
            choices=["Standard", "Extended"],
            adders={"Standard": 0, "Extended": adder_amount}
        )
        db.add(option)
        db.flush()
        print(f"Created length adder option: ${adder_amount}/ft")
        return option


def create_process_connection_option(db, connection_spec: str) -> Optional[Option]:
    """Create process connection option based on specification."""
    if not connection_spec:
        return None
    
    # Extract connection type from specification
    connection_match = re.search(r'(\d+(?:/\d+)?)\s*["\']?\s*(NPT|Flange|Tri-clamp)', connection_spec, re.IGNORECASE)
    if not connection_match:
        return None
    
    size = connection_match.group(1)
    conn_type = connection_match.group(2).upper()
    
    # Check if option already exists
    option = db.query(Option).filter_by(
        name="Process Connection",
        category="Connections"
    ).first()
    
    connection_value = f"{size}\" {conn_type}"
    
    if option:
        if option.choices is None:
            option.choices = []
        if option.adders is None:
            option.adders = {}
        # Add new connection to existing choices if not present
        if connection_value not in option.choices:
            option.choices.append(connection_value)
            option.adders[connection_value] = 0
            db.flush()
        return option
    else:
        # Create new option
        option = Option(
            name="Process Connection",
            description="Process connection type and size",
            price=0.0,
            price_type="fixed",
            category="Connections",
            choices=[connection_value],
            adders={connection_value: 0}
        )
        db.add(option)
        db.flush()
        print(f"Created process connection option: {connection_value}")
        return option


def associate_option_with_family(db, family: ProductFamily, option: Option):
    """Associate an option with a product family."""
    if not option:
        return
    
    # Always check if association already exists (even after flush)
    family_option = db.query(ProductFamilyOption).filter_by(
        product_family_id=family.id,
        option_id=option.id
    ).first()
    
    if not family_option:
        family_option = ProductFamilyOption(
            product_family_id=family.id,
            option_id=option.id,
            is_available=1
        )
        db.add(family_option)
        db.flush()
        print(f"Associated {option.name} with {family.name}")
    else:
        print(f"Association already exists: {option.name} with {family.name}")


def integrate_rtf_data():
    """Integrate extracted RTF data into the database."""
    db = SessionLocal()
    
    try:
        # Load extracted RTF data
        with open("extracted_rtf_data.json", "r", encoding="utf-8") as f:
            rtf_data = json.load(f)
        
        print("Integrating RTF template data into database...")
        print(f"Processing {len(rtf_data)} product specifications")
        
        # Process each product specification
        for spec_data in rtf_data:
            family_name = spec_data['product_family']
            material = spec_data.get('material_type')
            variant = spec_data.get('variant_type')
            
            # Clean the specifications
            cleaned_specs = extract_clean_specifications(spec_data)
            
            # Create or get product family
            family = create_or_update_product_family(db, family_name)
            
            # Create base model
            model_suffix = ""
            if material:
                model_suffix += f"-{material[:1].upper()}"
            if variant:
                model_suffix += f"-{variant.replace(' ', '')[:1].upper()}"
            
            model_number = f"{family_name}{model_suffix}-XX"
            
            base_model = db.query(BaseModel).filter_by(
                product_family_id=family.id,
                model_number=model_number
            ).first()
            
            if not base_model:
                description = f"{family_name}"
                if material:
                    description += f" {material}"
                if variant:
                    description += f" {variant}"
                description += " specification from RTF template"
                
                base_model = BaseModel(
                    product_family_id=family.id,
                    model_number=model_number,
                    description=description,
                    base_price=cleaned_specs.get('base_price', 0.0),
                    voltage=cleaned_specs.get('supply_voltage') if cleaned_specs.get('supply_voltage') else "115VAC",
                    material=material if material else "S",
                    base_length=cleaned_specs.get('insulator_length') or 10.0
                )
                db.add(base_model)
                print(f"Created base model: {model_number}")
            
            # Create and associate options based on specifications
            
            # Insulator material option
            if cleaned_specs.get('insulator_material'):
                insulator_option = create_insulator_option(db, cleaned_specs['insulator_material'])
                associate_option_with_family(db, family, insulator_option)
            
            # Length adder option
            if cleaned_specs.get('length_adder_per_foot'):
                length_option = create_length_adder_option(db, cleaned_specs['length_adder_per_foot'])
                associate_option_with_family(db, family, length_option)
            
            # Process connection option
            if cleaned_specs.get('process_connection'):
                connection_option = create_process_connection_option(db, cleaned_specs['process_connection'])
                associate_option_with_family(db, family, connection_option)
            
            # Create housing option if specified
            if cleaned_specs.get('housing_type'):
                housing_option = db.query(Option).filter_by(
                    name="Housing Type",
                    category="Housing"
                ).first()
                
                if not housing_option:
                    housing_option = Option(
                        name="Housing Type",
                        description="Housing type and ratings",
                        price=0.0,
                        price_type="fixed",
                        category="Housing",
                        choices=["Cast Aluminum"],
                        adders={"Cast Aluminum": 0}
                    )
                    db.add(housing_option)
                    db.flush()
                
                associate_option_with_family(db, family, housing_option)
        
        db.commit()
        print("RTF data integration completed successfully!")
        
        # Print summary
        print("\nIntegration Summary:")
        families = db.query(ProductFamily).all()
        print(f"Total product families: {len(families)}")
        
        options = db.query(Option).all()
        print(f"Total options: {len(options)}")
        
        family_options = db.query(ProductFamilyOption).all()
        print(f"Total family-option associations: {len(family_options)}")
        
    except Exception as e:
        print(f"Error during integration: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    integrate_rtf_data() 