#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option


def check_material_adders():
    db = SessionLocal()
    try:
        material_options = db.query(Option).filter(Option.category == "Material").all()
        print("Material Options and Adders:")
        for opt in material_options:
            print(f"  {opt.name}:")
            print(f"    Choices: {opt.choices}")
            print(f"    Adders: {opt.adders}")
            print()
    finally:
        db.close()


if __name__ == "__main__":
    check_material_adders()
