from src.core.database import SessionLocal
from src.core.models.material_option import MaterialOption
from src.core.models.product_variant import ProductFamily


def add_missing_material_options():
    db = SessionLocal()
    try:
        # Get the LS7000/2 family
        family = db.query(ProductFamily).filter_by(name="LS7000/2").first()
        if not family:
            print("LS7000/2 family not found")
            return

        # Add missing material options
        new_options = [
            MaterialOption(
                product_family_id=family.id,
                material_code="S",
                display_name="S - 316 Stainless Steel",
                base_price=0.0,
                is_available=1,
            ),
            MaterialOption(
                product_family_id=family.id,
                material_code="CPVC",
                display_name="CPVC",
                base_price=400.0,
                is_available=1,
            ),
        ]

        # Add and commit the new options
        for option in new_options:
            db.add(option)
        db.commit()
        print("Successfully added missing material options for LS7000/2")

    except Exception as e:
        print(f"Error adding material options: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_missing_material_options()
