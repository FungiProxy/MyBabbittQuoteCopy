#!/usr/bin/env python3
"""
Fix Housing Option Families

This script ensures all housing options have the correct product_families field set
for each associated product family, so they show up in the UI.
"""

import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily

def fix_housing_option_families():
    db = SessionLocal()
    try:
        housing_options = db.query(Option).filter(Option.category == "Housing").all()
        for option in housing_options:
            # Find all families linked via ProductFamilyOption
            family_links = db.query(ProductFamilyOption).filter(ProductFamilyOption.option_id == option.id).all()
            family_names = []
            for link in family_links:
                family = db.query(ProductFamily).filter(ProductFamily.id == link.product_family_id).first()
                if family is not None:
                    family_names.append(family.name)
            if family_names:
                pf_string = ",".join(sorted(set(family_names)))
                if str(option.product_families) != pf_string:
                    print(f"Updating {option.name}: {option.product_families} -> {pf_string}")
                    option.product_families = pf_string
        db.commit()
        print("Housing option product_families fields updated.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_housing_option_families() 