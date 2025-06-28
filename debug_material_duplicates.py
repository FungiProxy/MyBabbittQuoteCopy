#!/usr/bin/env python3
"""
Debug why there are multiple material options for some product families.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def debug_material_duplicates():
    """Debug material option duplicates."""
    db: Session = next(get_db())

    try:
        print("=== DEBUGGING MATERIAL OPTION DUPLICATES ===\n")
        
        # Get all material options
        material_options = db.query(Option).filter(Option.category == "Material").all()
        print(f"Total material options found: {len(material_options)}")
        
        for i, opt in enumerate(material_options):
            print(f"\nMaterial Option {i+1}:")
            print(f"  ID: {opt.id}")
            print(f"  Name: {opt.name}")
            print(f"  Description: {opt.description}")
            print(f"  Choices: {opt.choices}")
            print(f"  Adders: {opt.adders}")
            
            # Get families associated with this option
            associations = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.option_id == opt.id)
                .all()
            )
            print(f"  Associated families: {len(associations)}")
            for assoc in associations:
                family = (
                    db.query(ProductFamily)
                    .filter(ProductFamily.id == assoc.product_family_id)
                    .first()
                )
                print(f"    - {family.name if family else 'Unknown'} (available: {assoc.is_available})")
        
        print("\n=== CHECKING FAMILY-SPECIFIC ASSOCIATIONS ===")
        
        # Check specific families
        test_families = ["LS2000", "LS7000", "FS10000", "LT9000"]
        
        for family_name in test_families:
            print(f"\n--- {family_name} ---")
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            
            if not family:
                print(f"  Family {family_name} not found")
                continue
                
            print(f"  Family ID: {family.id}")
            
            # Get all material options for this family
            material_associations = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.product_family_id == family.id)
                .join(Option)
                .filter(Option.category == "Material")
                .all()
            )
            
            print(f"  Material associations: {len(material_associations)}")
            for assoc in material_associations:
                option = assoc.option
                print(f"    - Option ID {option.id}: {option.name}")
                print(f"      Choices: {option.choices}")
                print(f"      Available: {assoc.is_available}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    debug_material_duplicates() 