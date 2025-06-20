import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.material_option import MaterialOption
from src.core.models.product_variant import ProductFamily, ProductVariant


def create_missing_variants():
    db = SessionLocal()
    try:
        # Models to process
        models = ['LS7000/2', 'LS8000', 'LS8000/2', 'LT9000', 'FS10000']

        for model_name in models:
            print(f'\nProcessing {model_name}...')

            # Get the product family
            family = db.query(ProductFamily).filter_by(name=model_name).first()
            if not family:
                print(f'  {model_name} family not found')
                continue

            # Get available material options
            materials = (
                db.query(MaterialOption)
                .filter_by(product_family_id=family.id, is_available=1)
                .all()
            )

            if not materials:
                print(f'  No available material options found for {model_name}')
                continue

            print(f'  Found {len(materials)} available material options')

            # Get existing variants
            existing_variants = (
                db.query(ProductVariant).filter_by(product_family_id=family.id).all()
            )

            print(f'  Found {len(existing_variants)} existing variants')

            # Define standard configurations
            voltages = ['115VAC', '24VDC', '12VDC', '240VAC']
            base_lengths = [10.0]  # Standard length

            # Create missing variants
            new_variants = []
            for voltage in voltages:
                for material in materials:
                    for length in base_lengths:
                        model_number = f'{model_name}-{voltage}-{material.material_code}-{int(length)}"'

                        # Check if variant already exists
                        if not any(
                            v.model_number == model_number for v in existing_variants
                        ):
                            variant = ProductVariant(
                                product_family_id=family.id,
                                model_number=model_number,
                                description=f'{model_name} level switch with {voltage} power and {int(length)}" {material.display_name} probe',
                                base_price=material.base_price,
                                base_length=length,
                                voltage=voltage,
                                material=material.material_code,
                            )
                            new_variants.append(variant)
                            print(f'  Will create: {model_number}')

            if new_variants:
                print(f'  Creating {len(new_variants)} new variants...')
                db.add_all(new_variants)
                db.commit()
                print(f'  Successfully created new variants for {model_name}')
            else:
                print(f'  No new variants needed for {model_name}')

    except Exception as e:
        print(f'Error: {e!s}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    create_missing_variants()
