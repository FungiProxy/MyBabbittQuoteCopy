import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.database import SessionLocal
from src.core.models.material_option import MaterialOption
from src.core.models.product_variant import ProductFamily

# Standard material codes and display names
STANDARD_MATERIALS = {
    'S': 'S - 316 Stainless Steel',
    'H': 'H - Halar Coated',
    'TS': 'TS - Teflon Sleeve',
    'T': 'T - Teflon',
    'U': 'U - UHMWPE',
    'CPVC': 'CPVC',
}


def standardize_material_options():
    db = SessionLocal()
    try:
        families = db.query(ProductFamily).all()
        for fam in families:
            print(f'Processing {fam.name} (ID: {fam.id})')
            # Get all material options for this family
            options = db.query(MaterialOption).filter_by(product_family_id=fam.id).all()
            seen_codes = set()
            for opt in options:
                # If code is not standard, try to map it
                code = opt.material_code
                # If code is a display name, try to reverse map
                if code not in STANDARD_MATERIALS:
                    # Try to match by display name
                    for std_code, std_name in STANDARD_MATERIALS.items():
                        if opt.display_name == std_name or code == std_name:
                            code = std_code
                            break
                # Update code and display name
                if code in STANDARD_MATERIALS:
                    opt.material_code = code
                    opt.display_name = STANDARD_MATERIALS[code]
                    seen_codes.add(code)
                else:
                    print(
                        f'  [WARN] Unknown material code/display: {opt.material_code} / {opt.display_name}'
                    )
            # Add missing standard materials for this family if needed
            for code, display in STANDARD_MATERIALS.items():
                if code not in seen_codes:
                    new_opt = MaterialOption(
                        product_family_id=fam.id,
                        material_code=code,
                        display_name=display,
                        base_price=0.0,
                        is_available=0,  # Mark as unavailable by default
                    )
                    db.add(new_opt)
                    print(f'  [ADD] {code} ({display}) added as unavailable')
        db.commit()
        print('Material options standardized for all product families.')
    except Exception as e:
        print(f'Error: {e}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    standardize_material_options()
