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

def create_material_options():
    """Create material options for all product families if they don't exist."""
    db = SessionLocal()
    try:
        families = db.query(ProductFamily).all()
        for family in families:
            print(f'\nProcessing {family.name} (ID: {family.id})')
            
            # Get existing material options for this family
            existing_options = {
                opt.material_code: opt 
                for opt in db.query(MaterialOption).filter_by(product_family_id=family.id).all()
            }
            
            # Create missing material options
            for code, display_name in STANDARD_MATERIALS.items():
                if code not in existing_options:
                    new_option = MaterialOption(
                        product_family_id=family.id,
                        material_code=code,
                        display_name=display_name,
                        base_price=0.0,
                        is_available=1
                    )
                    db.add(new_option)
                    print(f"  [CREATE] {code} ({display_name})")
                else:
                    # Update display name if it doesn't match standard
                    if existing_options[code].display_name != display_name:
                        existing_options[code].display_name = display_name
                        print(f"  [UPDATE] {code} display name to {display_name}")
            
            # Set availability based on product family
            if family.name in ['LS7000/2', 'LS8000/2']:
                # Dual point switches don't support U and T materials
                for code in ['U', 'T']:
                    if code in existing_options:
                        existing_options[code].is_available = 0
                        print(f"  [UPDATE] {code} set to unavailable for dual point switch")
            
        db.commit()
        print('\nMaterial options created/updated for all product families.')
    except Exception as e:
        print(f'Error: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    create_material_options() 