#!/usr/bin/env python3
"""
Add Housing Options from Imported Data

This script extracts housing-related options from the internal_data_import.json
and adds them to the database as Option records.
"""

import json
import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily

DATA_FILE = "data/internal_data_import.json"

def extract_housing_options():
    """Extract housing options from the imported data."""
    housing_options = []
    
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    
    families = data.get("families", [])
    
    for family in families:
        family_name = family["name"]
        options = family.get("options", [])
        
        for option in options:
            option_name = option.get("name", "")
            
            # Check if this is a housing-related option
            if any(housing_keyword in option_name.lower() for housing_keyword in [
                "housing", "enclosure", "nema", "explosion", "receiver"
            ]):
                housing_options.append({
                    "family_name": family_name,
                    "option_name": option_name,
                    "choices": option.get("choices", []),
                    "adders": option.get("adders", {}),
                    "notes": option.get("notes", ""),
                    "rules": option.get("rules", "")
                })
    
    return housing_options

def add_housing_options_to_db():
    """Add housing options to the database."""
    db = SessionLocal()
    
    try:
        housing_options = extract_housing_options()
        
        print(f"Found {len(housing_options)} housing options to add:")
        
        for housing_opt in housing_options:
            family_name = housing_opt["family_name"]
            option_name = housing_opt["option_name"]
            
            print(f"  - {family_name}: {option_name}")
            
            # Get or create product family
            family = db.query(ProductFamily).filter_by(name=family_name).first()
            if not family:
                print(f"    Warning: Product family '{family_name}' not found, skipping...")
                continue
            
            # Check if option already exists
            existing_option = db.query(Option).filter_by(
                name=option_name,
                category="Housing"
            ).first()
            
            if existing_option:
                print(f"    Option '{option_name}' already exists, linking to family...")
                option = existing_option
            else:
                # Create new housing option
                option = Option(
                    name=option_name,
                    description=housing_opt.get("notes", f"{option_name} configuration"),
                    price=0.0,
                    price_type="fixed",
                    category="Housing",
                    choices=housing_opt.get("choices", []),
                    adders=housing_opt.get("adders", {}),
                    rules=housing_opt.get("rules", "")
                )
                db.add(option)
                db.flush()  # Get the option ID
                print(f"    Created new option: {option_name}")
            
            # Link option to product family
            existing_link = db.query(ProductFamilyOption).filter_by(
                product_family_id=family.id,
                option_id=option.id
            ).first()
            
            if not existing_link:
                link = ProductFamilyOption(
                    product_family_id=family.id,
                    option_id=option.id,
                    is_available=1
                )
                db.add(link)
                print(f"    Linked to family: {family_name}")
        
        db.commit()
        print(f"\nSuccessfully added {len(housing_options)} housing options!")
        
    except Exception as e:
        print(f"Error adding housing options: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_housing_options_to_db() 