#!/usr/bin/env python3

from src.core.database import get_db
from src.core.models.option import Option
from src.core.models.product_variant import ProductVariant


def check_lt9000_pricing():
    db = next(get_db())

    print("=== LT9000 Product Variants ===")
    variants = (
        db.query(ProductVariant).filter(ProductVariant.product_family == "LT9000").all()
    )
    for v in variants:
        print(f"{v.model_number}: ${v.base_price}")

    print("\n=== LT9000 Material Options ===")
    material_options = (
        db.query(Option)
        .filter(Option.product_families.like("%LT9000%"), Option.category == "Material")
        .all()
    )

    for opt in material_options:
        print(f"Option: {opt.name}")
        print(f"Choices: {opt.choices}")
        print(f"Adders: {opt.adders}")
        print(f"Product Families: {opt.product_families}")
        print("---")


if __name__ == "__main__":
    check_lt9000_pricing()
