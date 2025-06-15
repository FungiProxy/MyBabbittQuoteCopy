import os
import sys

from sqlalchemy import text
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.core.models.option import Option


def seed_options(db: Session):
    """Seeds the database with product options."""

    options_data = [
        # O-Ring Materials
        {
            "name": "Viton",
            "description": "Viton O-ring",
            "price": 0.0,
            "price_type": "fixed",
            "category": "O-ring Material",
            "choices": ["Viton"],
            "adders": {},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        {
            "name": "Silicon",
            "description": "Silicon O-ring",
            "price": 0.0,
            "price_type": "fixed",
            "category": "O-ring Material",
            "choices": ["Silicon"],
            "adders": {},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        {
            "name": "Buna-N",
            "description": "Buna-N O-ring",
            "price": 0.0,
            "price_type": "fixed",
            "category": "O-ring Material",
            "choices": ["Buna-N"],
            "adders": {},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        {
            "name": "EPDM",
            "description": "EPDM O-ring",
            "price": 0.0,
            "price_type": "fixed",
            "category": "O-ring Material",
            "choices": ["EPDM"],
            "adders": {},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        {
            "name": "PTFE",
            "description": "PTFE O-ring",
            "price": 0.0,
            "price_type": "fixed",
            "category": "O-ring Material",
            "choices": ["PTFE"],
            "adders": {},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        {
            "name": "Kalrez",
            "description": "Kalrez O-ring",
            "price": 295.0,
            "price_type": "fixed",
            "category": "O-ring Material",
            "choices": ["Kalrez"],
            "adders": {"Kalrez": 295.0},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        # Exotic Metals
        {
            "name": "None",
            "description": "No exotic metal",
            "price": 0.0,
            "price_type": "fixed",
            "category": "Exotic Metal",
            "choices": ["None"],
            "adders": {},
            
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        {
            "name": "Alloy 20",
            "description": "Alloy 20 (Consult Factory)",
            "price": 0.0,
            "price_type": "fixed",
            "category": "Exotic Metal",
            "choices": ["Alloy 20"],
            "adders": {},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        {
            "name": "Hastelloy-C-276",
            "description": "Hastelloy-C-276 (Consult Factory)",
            "price": 0.0,
            "price_type": "fixed",
            "category": "Exotic Metal",
            "choices": ["Hastelloy-C-276"],
            "adders": {},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        {
            "name": "Hastelloy-B",
            "description": "Hastelloy-B (Consult Factory)",
            "price": 0.0,
            "price_type": "fixed",
            "category": "Exotic Metal",
            "choices": ["Hastelloy-B"],
            "adders": {},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        {
            "name": "Titanium",
            "description": "Titanium (Consult Factory)",
            "price": 0.0,
            "price_type": "fixed",
            "category": "Exotic Metal",
            "choices": ["Titanium"],
            "adders": {},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        # O-Rings
        {
            "name": "O-Rings",
            "description": "O-Ring material selection",
            "price": 0.0,
            "price_type": "fixed",
            "category": "O-ring Material",
            "choices": ["Viton", "Silicon", "Buna-N", "EPDM", "PTFE", "Kalrez"],
            "adders": {
                "Viton": 0,
                "Silicon": 0,
                "Buna-N": 0,
                "EPDM": 0,
                "PTFE": 0,
                "Kalrez": 295,
            },
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        # CPVC Option
        {
            "name": "CPVC",
            "description": "CPVC Material Option",
            "price": 400.0,
            "price_type": "fixed",
            "category": "Material",
            "choices": ["CPVC"],
            "adders": {"CPVC": 400.0},
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
    ]

    for data in options_data:
        # Check if an option with the same name and category already exists
        exists = (
            db.query(Option)
            .filter_by(name=data["name"], category=data["category"])
            .first()
        )
        if not exists:
            option = Option(**data)
            db.add(option)

    db.commit()
    print("Successfully seeded product options.")

    # Remove duplicate material options for LS2100, LS6000, and LS7000
    for model in ["LS2100", "LS6000", "LS7000"]:
        duplicate_materials = [
            {
                "name": "Material",
                "description": "Probe material",
                "price": 0.0,
                "price_type": "adder",
                "category": "specifications",
                "choices": ["316SS", "Hastelloy C276", "Titanium", "Monel", "Inconel 600", "Inconel 625"],
                "adders": {
                    "316SS": 0.0,
                    "Hastelloy C276": 0.0,
                    "Titanium": 0.0,
                    "Monel": 0.0,
                    "Inconel 600": 0.0,
                    "Inconel 625": 0.0
                },
                "product_families": [model]
            }
        ]
        for material in duplicate_materials:
            db.query(Option).filter_by(name=material["name"], product_families=model).delete()

    # Remove duplicate probe length options for LS2100, LS6000, and LS7000
    for model in ["LS2100", "LS6000", "LS7000"]:
        duplicate_lengths = [
            {
                "name": "Probe Length",
                "description": "Probe length in inches",
                "price": 0.0,
                "price_type": "adder",
                "category": "specifications",
                "choices": ["1", "2", "3", "4", "5", "6"],
                "adders": {
                    "1": 0.0,
                    "2": 0.0,
                    "3": 0.0,
                    "4": 0.0,
                    "5": 0.0,
                    "6": 0.0
                },
                "product_families": [model]
            }
        ]
        for length in duplicate_lengths:
            db.query(Option).filter_by(name=length["name"], product_families=model).delete()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        # For SQLite, it's helpful to enable foreign key constraints
        if db.bind.dialect.name == "sqlite":
            db.execute(text("PRAGMA foreign_keys = ON;"))
        seed_options(db)
    finally:
        db.close()
