from src.core.database import SessionLocal
from src.core.models import Option

def update_option_categories():
    category_map = {
        'Material': 'Materials',
        'O-Ring Materials': 'O-Ring Materials',
        'O-Ring Material': 'O-Ring Materials',
        'Electrical': 'Voltages',  # Only for voltage options, see below
        'Mechanical': 'Accessories',  # Default, but see below for connections
        'Connections': 'Connections',
        'Pricing': 'Pricing',
        'Exotic Metal': 'Exotic Metals',
        'Exotic Metals': 'Exotic Metals',
    }
    # Special case names for connections
    connection_names = [
        'Connection Type', 'NPT Size', 'Flange Type', 'Flange Size', 'Tri-clamp', 'Insulator'
    ]
    # Accessories (mechanical or electrical, not connections)
    accessories_names = [
        'Bent Probe', 'Stainless Steel Tag', '3/4" Diameter Probe', 'NEMA 4 Enclosure',
        'GRK Exp Proof Enclosure', 'Twisted Shielded Pair', 'Additional Coaxial Cable', 'Extra Static Protection'
    ]
    db = SessionLocal()
    try:
        options = db.query(Option).all()
        for opt in options:
            old_cat = opt.category
            new_cat = None
            if opt.name in connection_names:
                new_cat = 'Connections'
            elif opt.name == 'Voltage':
                new_cat = 'Voltages'
            elif opt.name in accessories_names:
                new_cat = 'Accessories'
            elif old_cat in category_map:
                new_cat = category_map[old_cat]
            else:
                new_cat = old_cat  # fallback
            if old_cat != new_cat:
                print(f"Updating {opt.name}: {old_cat} -> {new_cat}")
                opt.category = new_cat
        db.commit()
        print('Option categories updated successfully!')
    except Exception as e:
        db.rollback()
        print(f'Error updating option categories: {e}')
        raise
    finally:
        db.close()

if __name__ == '__main__':
    update_option_categories() 