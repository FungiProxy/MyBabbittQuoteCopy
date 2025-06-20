#!/usr/bin/env python3
"""
Create family-specific material options with only the materials each family should have.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def fix_family_specific_materials():
    """Create family-specific material options."""
    db: Session = next(get_db())

    try:
        # Define which materials each family should have
        family_materials = {
            "LS2000": ["S", "H", "U", "T", "TS"],
            "LS2100": ["S", "H", "U", "T", "TS"],
            "LS6000": ["S", "H", "U", "T", "TS"],
            "LS7000": ["S", "H", "U", "T", "TS"],
            "LS7000/2": ["S", "H", "U", "T", "TS"],
            "LS8000": ["S", "H", "U", "T", "TS", "C", "CPVC", "A", "HC", "HB", "TT"],
            "LS8000/2": ["S", "H", "U", "T", "TS", "C", "CPVC", "A", "HC", "HB", "TT"],
            "LT9000": ["S", "H", "U", "T", "TS"],
            "FS10000": ["S", "H", "U", "T", "TS"],
            "LS7500": ["S", "H", "U", "T", "TS"],
            "LS8500": ["S", "H", "U", "T", "TS"],
        }

        # Material descriptions and adders
        material_descriptions = {
            "S": "S - 316 Stainless Steel",
            "H": "H - Halar Coated",
            "TS": "TS - Teflon Sleeve",
            "U": "U - UHMWPE Blind End",
            "T": "T - Teflon Blind End",
            "C": "C - Cable",
            "CPVC": "CPVC - CPVC Blind End",
            "A": "A - Alloy 20",
            "HC": "HC - Hastelloy-C-276",
            "HB": "HB - Hastelloy-B",
            "TT": "TT - Titanium",
        }

        material_adders = {
            "C": 80.0,
            "A": 0,
            "HC": 0,
            "HB": 0,
            "TT": 0,
            "H": 110.0,
            "S": 0.0,
            "T": 60.0,
            "TS": 110.0,
            "U": 20.0,
            "CPVC": 400.0,
        }

        # Remove the old universal material option associations
        print("Removing old material option associations...")
        old_associations = (
            db.query(ProductFamilyOption)
            .join(Option)
            .filter(Option.name == "Material")
            .all()
        )
        for assoc in old_associations:
            db.delete(assoc)

        # Create family-specific material options
        for family_name, materials in family_materials.items():
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.name == family_name)
                .first()
            )
            if not family:
                print(f"Family {family_name} not found")
                continue

            print(
                f"Creating material option for {family_name} with materials: {materials}"
            )

            # Create choices list for this family
            choices = []
            adders = {}

            for material in materials:
                choices.append(
                    {
                        "code": material,
                        "display_name": material_descriptions.get(material, material),
                    }
                )
                if material in material_adders:
                    adders[material] = material_adders[material]

            # Create the material option for this family
            material_option = Option(
                name="Material",
                description=f"Material options for {family_name}",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=choices,
                adders=adders,
                excluded_products=None,
            )
            db.add(material_option)
            db.flush()  # Get the ID

            # Create association
            association = ProductFamilyOption(
                product_family_id=family.id,
                option_id=material_option.id,
                is_available=1,
            )
            db.add(association)

            print(
                f"  Created option ID {material_option.id} with {len(choices)} materials"
            )

        db.commit()
        print("Family-specific material options created successfully!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    fix_family_specific_materials()
