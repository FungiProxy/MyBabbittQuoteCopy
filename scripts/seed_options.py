import os
import sys
from sqlalchemy import text
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def seed_options(db: Session):
    """
    Seeds the database with consolidated and corrected product options.
    This script uses an "upsert" logic: it updates existing options or creates them if they don't exist.
    """
    print("Starting to seed product options...")

    # --- Cleanup Phase ---
    # Delete old, fragmented material-related options to prevent conflicts and duplicates.
    print("Cleaning up old material-related options...")
    db.query(Option).filter(Option.category == "Exotic Metal").delete(
        synchronize_session=False
    )
    db.query(Option).filter(
        Option.name == "CPVC", Option.category == "Material"
    ).delete(synchronize_session=False)
    # Also delete any old top-level material option that might conflict with our new unified one.
    db.query(Option).filter(
        Option.name == "Material", Option.category == "specifications"
    ).delete(synchronize_session=False)
    db.commit()
    print("Cleanup complete.")

    # --- Data Definition Phase ---
    # Define all product options in a structured way.
    options_data = [
        {
            "name": "Material",
            "description": "Defines the wetted materials of the probe and housing.",
            "price": 0.0,
            "price_type": "fixed",
            "category": "Material",
            "excluded_products": "",  # Remove exclusions - all families should have material pricing
            "choices": [
                {"code": "S", "display_name": "S - 316 Stainless Steel"},
                {"code": "H", "display_name": "H - Halar Coated"},
                {"code": "TS", "display_name": "TS - Teflon Sleeve"},
                {"code": "T", "display_name": "T - Teflon"},
                {"code": "U", "display_name": "U - UHMWPE"},
                {"code": "CPVC", "display_name": "CPVC"},
                {
                    "code": "HC",
                    "display_name": "HC - Hastelloy C-276 (Consult Factory)",
                },
                {"code": "HB", "display_name": "HB - Hastelloy B (Consult Factory)"},
                {"code": "TI", "display_name": "TI - Titanium (Consult Factory)"},
                {"code": "A20", "display_name": "A20 - Alloy 20 (Consult Factory)"},
                {"code": "M", "display_name": "M - Monel (Consult Factory)"},
                {"code": "I", "display_name": "I - Inconel (Consult Factory)"},
            ],
            "adders": {
                "S": 0.0,
                "H": 110.0,
                "TS": 110.0,
                "T": 60.0,
                "U": 20.0,
                "CPVC": 400.0,
                "HC": 0.0,  # Price requires factory consultation
                "HB": 0.0,  # Price requires factory consultation
                "TI": 0.0,  # Price requires factory consultation
                "A20": 0.0,  # Price requires factory consultation
                "M": 0.0,  # Price requires factory consultation
                "I": 0.0,  # Price requires factory consultation
            },
        },
        {
            "name": "O-Rings",
            "description": "O-Ring material selection",
            "price": 0.0,
            "price_type": "fixed",
            "category": "O-ring Material",
            "choices": ["Viton", "Silicon", "Buna-N", "EPDM", "PTFE", "Kalrez"],
            "adders": {
                "Viton": 0.0,
                "Silicon": 0.0,
                "Buna-N": 0.0,
                "EPDM": 0.0,
                "PTFE": 0.0,
                "Kalrez": 295.0,
            },
        },
    ]

    # --- Upsert Phase ---
    print("Upserting core product options...")
    for data in options_data:
        option = (
            db.query(Option)
            .filter_by(name=data["name"], category=data["category"])
            .first()
        )
        if option:
            print(f"Updating existing option: {data['name']}")
            option.description = data["description"]
            option.price = data["price"]
            option.price_type = data["price_type"]
            option.choices = data["choices"]
            option.adders = data["adders"]
        else:
            print(f"Creating new option: {data['name']}")
            option = Option(**data)
            db.add(option)
    db.commit()
    print("Upsert complete.")

    # --- Association Phase ---
    # This ensures that the core options are available for all product families.
    print("Associating options with product families...")
    all_families = db.query(ProductFamily).all()
    material_option = db.query(Option).filter_by(name="Material").first()
    oring_option = db.query(Option).filter_by(name="O-Rings").first()

    for family in all_families:
        # Associate Material option
        if material_option:
            assoc_exists = (
                db.query(ProductFamilyOption)
                .filter_by(product_family_id=family.id, option_id=material_option.id)
                .first()
            )
            if not assoc_exists:
                db.add(
                    ProductFamilyOption(
                        product_family_id=family.id, option_id=material_option.id
                    )
                )
                print(f"  Associated 'Material' with '{family.name}'")

        # Associate O-Rings option
        if oring_option:
            assoc_exists = (
                db.query(ProductFamilyOption)
                .filter_by(product_family_id=family.id, option_id=oring_option.id)
                .first()
            )
            if not assoc_exists:
                db.add(
                    ProductFamilyOption(
                        product_family_id=family.id, option_id=oring_option.id
                    )
                )
                print(f"  Associated 'O-Rings' with '{family.name}'")

    db.commit()
    print("Successfully seeded and associated product options.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        if db.bind.dialect.name == "sqlite":
            db.execute(text("PRAGMA foreign_keys = ON;"))
        seed_options(db)
    finally:
        db.close()
