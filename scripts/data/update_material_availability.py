import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.material_option import MaterialOption
from src.core.models.product_variant import ProductFamily

# Define material availability for each product family
MATERIAL_AVAILABILITY = {
    'LS2000': ['S', 'H', 'U', 'T', 'TS'],
    'LS2100': ['S', 'H', 'T', 'TS', 'U'],
    'LS6000': ['S', 'H', 'TS', 'CPVC'],
    'LS7000': ['S', 'H', 'TS', 'T', 'U', 'CPVC'],
    'LS7000/2': ['H', 'TS'],
    'LS8000': ['S', 'H', 'TS'],
    'LS8000/2': ['H', 'TS'],
    'LT9000': ['S', 'H', 'TS', 'T', 'U', 'CPVC'],
    'FS10000': ['S', 'H', 'TS', 'CPVC'],
    'Presence/Absence Switches': ['S'],
    'LS7500': ['S'],
    'LS8500': ['S'],
    'FT10000': ['S', 'H', 'TS', 'T', 'U', 'CPVC'],
}


def update_material_availability():
    db = SessionLocal()
    try:
        for family_name, available_materials in MATERIAL_AVAILABILITY.items():
            family = db.query(ProductFamily).filter_by(name=family_name).first()
            if not family:
                print(f'Family {family_name} not found')
                continue

            print(f'\nProcessing {family_name} (ID: {family.id})')

            # Get all material options for this family
            options = (
                db.query(MaterialOption).filter_by(product_family_id=family.id).all()
            )

            # Update availability for each material option
            for option in options:
                is_available = option.material_code in available_materials
                if option.is_available != (1 if is_available else 0):
                    option.is_available = 1 if is_available else 0
                    print(
                        f"  [UPDATE] {option.material_code} ({option.display_name}): {'Available' if is_available else 'Unavailable'}"
                    )

        db.commit()
        print('\nMaterial availability updated for all product families.')
    except Exception as e:
        print(f'Error: {e}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    update_material_availability()
