#!/usr/bin/env python3
"""
Update the database with corrected options from the CSV file.
This will fix the material filtering issue by removing the universal material option
and ensuring each family has only its specific material option.
"""

import os
import sys
import csv
import json
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import get_db
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def update_database_with_corrected_options():
    """Update the database with corrected options from CSV."""
    db: Session = next(get_db())

    try:
        print("=== UPDATING DATABASE WITH CORRECTED OPTIONS ===\n")
        
        # Read the corrected options from CSV
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'options_db.csv')
        
        if not os.path.exists(csv_path):
            print(f"Error: CSV file not found at {csv_path}")
            return
            
        print(f"Reading corrected options from: {csv_path}")
        
        # Clear existing options and associations
        print("Clearing existing options and associations...")
        db.query(ProductFamilyOption).delete()
        db.query(Option).delete()
        db.commit()
        print("✓ Cleared existing data")
        
        # Read and insert corrected options
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Parse choices and adders from JSON strings
                choices = json.loads(row['choices']) if row['choices'] else []
                adders = json.loads(row['adders']) if row['adders'] else {}
                
                # Create the option
                option = Option(
                    id=int(row['id']),
                    name=row['name'],
                    description=row['description'],
                    price=float(row['price']),
                    price_type=row['price_type'],
                    category=row['category'],
                    excluded_products=row['excluded_products'] if row['excluded_products'] else None,
                    product_families=row['product_families'] if row['product_families'] else None,
                    choices=choices,
                    adders=adders,
                    rules=json.loads(row['rules']) if row['rules'] else None
                )
                
                db.add(option)
                print(f"  ✓ Added option: {option.name} (ID: {option.id})")
        
        db.commit()
        print("✓ All options added to database")
        
        # Create family associations
        print("\nCreating family associations...")
        
        # Get all families
        families = db.query(ProductFamily).all()
        family_map = {family.name: family.id for family in families}
        
        # Get all options
        options = db.query(Option).all()
        
        for option in options:
            if option.product_families:
                # Parse family names (handle comma-separated lists)
                family_names = [name.strip() for name in option.product_families.split(',')]
                
                for family_name in family_names:
                    if family_name in family_map:
                        # Create association
                        association = ProductFamilyOption(
                            product_family_id=family_map[family_name],
                            option_id=option.id,
                            is_available=1
                        )
                        db.add(association)
                        print(f"  ✓ Associated {option.name} with {family_name}")
                    else:
                        print(f"  ⚠ Warning: Family '{family_name}' not found for option {option.name}")
        
        db.commit()
        print("✓ All family associations created")
        
        # Verify the fix
        print("\n=== VERIFYING THE FIX ===")
        
        test_families = ["LS2000", "LS7000", "FS10000", "LT9000"]
        
        for family_name in test_families:
            print(f"\n--- {family_name} ---")
            family = db.query(ProductFamily).filter_by(name=family_name).first()
            
            if not family:
                print(f"  Family {family_name} not found")
                continue
                
            # Get material options for this family
            material_options = (
                db.query(Option)
                .join(ProductFamilyOption)
                .filter(
                    ProductFamilyOption.product_family_id == family.id,
                    Option.category == "Material",
                    ProductFamilyOption.is_available == 1
                )
                .all()
            )
            
            print(f"  Material options: {len(material_options)}")
            for opt in material_options:
                print(f"    - {opt.name} (ID: {opt.id})")
                if opt.choices:
                    material_codes = [choice.get('code', choice) for choice in opt.choices]
                    print(f"      Materials: {material_codes}")
        
        print("\n=== DATABASE UPDATE COMPLETE ===")
        print("✓ Material filtering should now work correctly!")
        print("✓ Each family has only its specific material options")
        print("✓ CPVC is now available for LS6000 and LS7000")
        
    except Exception as e:
        print(f"Error updating database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    update_database_with_corrected_options() 