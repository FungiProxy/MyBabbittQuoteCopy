from src.core.database import SessionLocal
from src.core.models import Option

def integrate_exotic_metals():
    db = SessionLocal()
    try:
        # Find the exotic metals option
        exotic_metals_option = db.query(Option).filter(
            Option.name == 'Material',
            Option.category == 'Materials'
        ).first()
        
        if exotic_metals_option:
            print(f"Found materials option: {exotic_metals_option.choices}")
            
            # Update the choices to include exotic metals with correct codes
            # Map the current exotic metals to the specified codes
            exotic_metal_mapping = {
                'Alloy 20': 'A',
                'Hastelloy-C-276': 'HC', 
                'Hastelloy-B': 'HB',
                'Titanium': 'TT'
            }
            
            # Get current choices and adders
            current_choices = exotic_metals_option.choices
            current_adders = exotic_metals_option.adders
            
            # Update choices to use the new codes
            new_choices = []
            new_adders = {}
            
            for choice in current_choices:
                if choice in exotic_metal_mapping:
                    # Replace exotic metal name with code
                    new_code = exotic_metal_mapping[choice]
                    new_choices.append(new_code)
                    new_adders[new_code] = 0  # Set to 0 as requested
                elif choice == 'None':
                    # Keep 'None' as is
                    new_choices.append(choice)
                    new_adders[choice] = current_adders.get(choice, 0)
                else:
                    # Keep other materials as is
                    new_choices.append(choice)
                    new_adders[choice] = current_adders.get(choice, 0)
            
            exotic_metals_option.choices = new_choices
            exotic_metals_option.adders = new_adders
            
            print(f"Updated materials choices: {new_choices}")
            print(f"Updated materials adders: {new_adders}")
            
            db.commit()
            print('Exotic metals successfully updated with correct codes (A, HB, HC, TT)!')
        else:
            print('No materials option found in database')
            
    except Exception as e:
        db.rollback()
        print(f'Error updating exotic metals: {e}')
        raise
    finally:
        db.close()

if __name__ == '__main__':
    integrate_exotic_metals() 