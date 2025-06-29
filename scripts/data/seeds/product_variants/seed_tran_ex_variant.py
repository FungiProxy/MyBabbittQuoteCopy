"""
Seed script for TRAN-EX product family (LS8000/2-TRAN-EX).
- Only S and H materials
- Base price $540 for LS8000/2-TRAN-EX-S-10"
- H material: $110 base adder + $110 per foot length
- All other options same as LS8000/2 (except voltage, which is fixed at 115VAC)
- Ensures core options (Material, Probe Length, etc.) are present for TRAN-EX
"""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily
from src.core.models.option import Option

def seed_tran_ex():
    db = SessionLocal()
    try:
        # 1. Add TRAN-EX product family
        tran_ex_family = db.query(ProductFamily).filter_by(name="TRAN-EX").first()
        if not tran_ex_family:
            tran_ex_family = ProductFamily(
                name="TRAN-EX",
                description="TRAN-EX Probe for LS8000/2 (fixed 115VAC, S/H material only)",
                category="Multi-Point Level Switch"
            )
            db.add(tran_ex_family)
            db.commit()
            print("Added TRAN-EX product family.")
        else:
            print("TRAN-EX product family already exists.")

        # 2. Remove any accessory-style TRAN-EX options
        accessory_opts = db.query(Option).filter(
            Option.product_families.like("%TRAN-EX%"),
            Option.category == "Accessories",
            Option.name.in_(["TRAN-EX", "TRAN-EX Material", "TRAN-EX Length"])
        ).all()
        for opt in accessory_opts:
            db.delete(opt)
        if accessory_opts:
            db.commit()
            print("Removed accessory-style TRAN-EX options.")

        # 3. Add Material core option (S and H only)
        material_option = db.query(Option).filter_by(name="Material", product_families="TRAN-EX").first()
        if not material_option:
            material_option = Option(
                name="Material",
                description="Probe material selection (TRAN-EX only S/H)",
                price=0.0,
                price_type="fixed",
                category="Material",
                choices=["S", "H"],
                adders={
                    "S": 0,
                    "H": 110  # base adder, per-foot handled in pricing logic
                },
                product_families="TRAN-EX"
            )
            db.add(material_option)
            db.commit()
            print("Added Material option for TRAN-EX.")
        else:
            print("Material option for TRAN-EX already exists.")

        # 4. Copy all other core options from LS8000/2 (except voltage and material)
        ls8000_2_options = db.query(Option).filter(Option.product_families.like("%LS8000/2%")).all()
        for opt in ls8000_2_options:
            if opt.category == "Voltages" or opt.name == "Voltage":
                continue  # Skip voltage
            if opt.name == "Material":
                continue  # Already handled above
            # Only copy core options (not Accessories)
            if opt.category == "Accessories":
                continue
            # Check if already exists for TRAN-EX
            exists = db.query(Option).filter_by(name=opt.name, product_families="TRAN-EX").first()
            if exists:
                continue
            new_opt = Option(
                name=opt.name,
                description=opt.description,
                price=opt.price,
                price_type=opt.price_type,
                category=opt.category,
                choices=opt.choices,
                adders=opt.adders,
                product_families="TRAN-EX"
            )
            db.add(new_opt)
        db.commit()
        print("Copied core options from LS8000/2 to TRAN-EX (excluding voltage/material/accessories).")

    except Exception as e:
        print(f"Error seeding TRAN-EX: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_tran_ex() 