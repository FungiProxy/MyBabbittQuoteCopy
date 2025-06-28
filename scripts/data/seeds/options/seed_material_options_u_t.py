#!/usr/bin/env python3
"""
Seed script to ensure U and T materials are available for LS2000, LS2100, LS6000, LS7000, and LS8000.
"""

from sqlalchemy import create_engine, text
from src.core.database import SessionLocal

# Material definitions
MATERIALS = [
    {"code": "U", "display_name": "U - UHMWPE Blind End", "adder": 40, "description": "UHMWPE blind end probe"},
    {"code": "T", "display_name": "T - Teflon Blind End", "adder": 50, "description": "Teflon blind end probe"},
]

# Product families to update
FAMILIES = ["LS2000", "LS2100", "LS6000", "LS7000", "LS8000"]

# Option name for material
OPTION_NAME = "Material"

# Adders dict for each material
ADDERS = {"U": 40, "T": 50}

# Choices list for each material
CHOICES = ["S", "H", "TS", "U", "T"]

# Main seeding logic
def seed_material_options():
    db = SessionLocal()
    try:
        for family in FAMILIES:
            # Check if the Material option exists for this family
            result = db.execute(text("""
                SELECT id FROM options WHERE name = :option_name AND product_families LIKE :family
            """), {"option_name": OPTION_NAME, "family": f"%{family}%"}).fetchone()
            if result:
                option_id = result[0]
                print(f"[INFO] Updating Material option for {family} (option_id={option_id})")
                # Update choices and adders to include U and T
                db.execute(text("""
                    UPDATE options
                    SET choices = :choices, adders = :adders
                    WHERE id = :option_id
                """), {
                    "choices": str(CHOICES),
                    "adders": str(ADDERS),
                    "option_id": option_id
                })
            else:
                print(f"[INFO] Inserting new Material option for {family}")
                db.execute(text("""
                    INSERT INTO options (name, description, price, price_type, category, choices, adders, product_families)
                    VALUES (:name, :description, 0.0, 'fixed', 'Material', :choices, :adders, :family)
                """), {
                    "name": OPTION_NAME,
                    "description": "Material selection for probe",
                    "choices": str(CHOICES),
                    "adders": str(ADDERS),
                    "family": family
                })
        db.commit()
        print("[SUCCESS] U and T materials seeded for all specified families.")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_material_options() 