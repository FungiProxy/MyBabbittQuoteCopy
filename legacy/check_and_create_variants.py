from src.core.database import SessionLocal
from src.core.models.product_variant import ProductVariant, ProductFamily
from src.core.models.material_option import MaterialOption


def check_and_create_variants():
    db = SessionLocal()
    try:
        # Get the LS7000/2 family
        family = db.query(ProductFamily).filter_by(name="LS7000/2").first()
        if not family:
            print("LS7000/2 family not found")
            return

        # Get all material options
        materials = (
            db.query(MaterialOption).filter_by(product_family_id=family.id).all()
        )
        print(f"Found {len(materials)} material options:")
        for m in materials:
            print(f"- {m.material_code} ({m.display_name})")

        # Get existing variants
        existing_variants = (
            db.query(ProductVariant).filter_by(product_family_id=family.id).all()
        )
        print(f"\nFound {len(existing_variants)} existing variants:")
        for v in existing_variants:
            print(f'- {v.model_number} ({v.voltage}, {v.material}, {v.base_length}")')

        # Define standard configurations
        voltages = ["12VDC", "24VDC", "115VAC", "240VAC"]
        base_lengths = [10.0]  # Standard length for LS7000/2

        # Create missing variants
        new_variants = []
        for voltage in voltages:
            for material in materials:
                for length in base_lengths:
                    model_number = (
                        f'LS7000/2-{voltage}-{material.material_code}-{int(length)}"'
                    )

                    # Check if variant already exists
                    if not any(
                        v.model_number == model_number for v in existing_variants
                    ):
                        variant = ProductVariant(
                            product_family_id=family.id,
                            model_number=model_number,
                            voltage=voltage,
                            material=material.material_code,
                            base_length=length,
                            base_price=material.base_price,
                        )
                        new_variants.append(variant)
                        print(f"Will create: {model_number}")

        if new_variants:
            print(f"\nCreating {len(new_variants)} new variants...")
            db.add_all(new_variants)
            db.commit()
            print("Successfully created new variants")
        else:
            print("\nNo new variants needed to be created")

    except Exception as e:
        print(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    check_and_create_variants()
