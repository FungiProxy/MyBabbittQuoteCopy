from src.core.database import SessionLocal
from src.core.models import Option

def add_exotic_metal_codes():
    db = SessionLocal()
    try:
        # Find the materials option
        materials_option = db.query(Option).filter(
            Option.name == 'Material',
            Option.category == 'Materials'
        ).first()
        
        if materials_option:
            print(f"Current materials: {materials_option.choices}")
            print(f"Current adders: {materials_option.adders}")
            
            # Add exotic metal codes to existing choices
            exotic_metal_codes = ['A', 'HB', 'HC', 'TT']
            
            # Get current choices and adders
            current_choices = materials_option.choices
            current_adders = materials_option.adders.copy()
            
            # Add exotic metal codes if they don't exist
            for code in exotic_metal_codes:
                if code not in current_choices:
                    current_choices.append(code)
                    current_adders[code] = 0  # Set to 0 as requested
                    print(f"Added exotic metal code: {code}")
            
            materials_option.choices = current_choices
            materials_option.adders = current_adders
            
            print(f"Updated materials choices: {current_choices}")
            print(f"Updated materials adders: {current_adders}")
            
            db.commit()
            print('Exotic metal codes (A, HB, HC, TT) successfully added to materials!')
        else:
            print('No materials option found in database')
            
    except Exception as e:
        db.rollback()
        print(f'Error adding exotic metal codes: {e}')
        raise
    finally:
        db.close()

if __name__ == '__main__':
    add_exotic_metal_codes() 