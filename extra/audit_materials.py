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
    codes = []
    for a in assignments:
        if a.option.choices and isinstance(a.option.choices, list):
            for choice in a.option.choices:
                if isinstance(choice, dict) and "code" in choice:
                    codes.append(choice["code"])
    print(f"{label} material codes: {codes}")


def audit_ls2000_materials():
    db = SessionLocal()
    try:
        ls2000 = db.query(ProductFamily).filter(ProductFamily.name == "LS2000").first()
        if not ls2000:
            print("Error: Could not find LS2000 product family")
            return
        print(f"LS2000 ID: {ls2000.id}")
        print_material_assignments(db, ls2000, "LS2000 (direct DB)")
        from src.core.services.product_service import ProductService

        ps = ProductService()
        ls2000_options = ps.get_additional_options(db, "LS2000")
        ls2000_materials = [
            opt for opt in ls2000_options if opt.get("category") == "Material"
        ]
        codes = []
        for opt in ls2000_materials:
            for choice in opt.get("choices", []):
                if isinstance(choice, dict) and "code" in choice:
                    codes.append(choice["code"])
        print(f"LS2000 materials via ProductService (codes): {codes}")
    finally:
        db.close()


if __name__ == "__main__":
    audit_ls2000_materials()
