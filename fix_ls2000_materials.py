#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def print_material_assignments(db, family, label):
    assignments = (
        db.query(ProductFamilyOption)
        .filter(ProductFamilyOption.product_family_id == family.id)
        .join(Option)
        .filter(Option.category == "Material")
        .all()
    )
    print(
        f"{label} materials:",
        [
            a.option.choices[0] if a.option.choices else a.option.name
            for a in assignments
        ],
    )


def find_material_option(db, material_code):
    """Find material option by checking if any choice has the given code"""
    material_options = db.query(Option).filter(Option.category == "Material").all()
    for opt in material_options:
        if opt.choices and isinstance(opt.choices, list):
            for choice in opt.choices:
                if isinstance(choice, dict) and choice.get("code") == material_code:
                    return opt
    return None


def fix_ls2000_materials():
    db = SessionLocal()
    try:
        ls2000 = db.query(ProductFamily).filter(ProductFamily.name == "LS2000").first()
        if not ls2000:
            print("Error: Could not find LS2000 product family")
            return
        print(f"LS2000 ID: {ls2000.id}")
        print_material_assignments(db, ls2000, "LS2000 (BEFORE)")

        # Remove all current material assignments for LS2000
        assignments = (
            db.query(ProductFamilyOption)
            .filter(ProductFamilyOption.product_family_id == ls2000.id)
            .join(Option)
            .filter(Option.category == "Material")
            .all()
        )
        for a in assignments:
            db.delete(a)
        db.commit()
        print("Removed all material assignments for LS2000.")

        # Add correct assignments (one per material)
        ls2000_material_codes = ["S", "H", "T", "TS", "U", "C"]
        for material_code in ls2000_material_codes:
            material_option = find_material_option(db, material_code)
            if material_option:
                db.add(
                    ProductFamilyOption(
                        product_family_id=ls2000.id,
                        option_id=material_option.id,
                        is_available=1,
                    )
                )
                print(f"  Added {material_code} to LS2000")
            else:
                print(f"  Warning: Could not find material option for {material_code}")
        db.commit()
        print("Material assignments updated successfully!")

        print_material_assignments(db, ls2000, "LS2000 (AFTER)")

        # Verify via ProductService
        from src.core.services.product_service import ProductService

        ps = ProductService()
        ls2000_options = ps.get_additional_options(db, "LS2000")
        ls2000_materials = [
            opt for opt in ls2000_options if opt.get("category") == "Material"
        ]
        print(
            f"LS2000 materials via ProductService: {[opt.get('choices', []) for opt in ls2000_materials]}"
        )
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_ls2000_materials()
