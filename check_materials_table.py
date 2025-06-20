from src.core.database import SessionLocal
from src.core.models import Material

def check_materials_table():
    db = SessionLocal()
    try:
        # Check current materials
        materials = db.query(Material).all()
        print('Current materials in materials table:')
        for m in materials:
            print(f'  {m.code}: {m.name} - Base Length: {m.base_length}", Length Adder: ${m.length_adder_per_foot}/ft, Non-standard: ${m.nonstandard_length_surcharge}')
        
        # Define exotic metals to add
        exotic_metals = [
            {'code': 'A', 'name': 'Alloy 20', 'base_length': 10.0, 'length_adder_per_foot': 0, 'nonstandard_length_surcharge': 0},
            {'code': 'HB', 'name': 'Hastelloy-B', 'base_length': 10.0, 'length_adder_per_foot': 0, 'nonstandard_length_surcharge': 0},
            {'code': 'HC', 'name': 'Hastelloy-C-276', 'base_length': 10.0, 'length_adder_per_foot': 0, 'nonstandard_length_surcharge': 0},
            {'code': 'TT', 'name': 'Titanium', 'base_length': 10.0, 'length_adder_per_foot': 0, 'nonstandard_length_surcharge': 0},
        ]
        
        # Check which exotic metals are missing
        existing_codes = [m.code for m in materials]
        missing_metals = [metal for metal in exotic_metals if metal['code'] not in existing_codes]
        
        if missing_metals:
            print(f'\nAdding {len(missing_metals)} missing exotic metals:')
            for metal in missing_metals:
                new_material = Material(
                    code=metal['code'],
                    name=metal['name'],
                    base_length=metal['base_length'],
                    length_adder_per_foot=metal['length_adder_per_foot'],
                    nonstandard_length_surcharge=metal['nonstandard_length_surcharge'],
                    has_nonstandard_length_surcharge=False
                )
                db.add(new_material)
                print(f'  Added: {metal["code"]} ({metal["name"]})')
            
            db.commit()
            print('Exotic metals added to materials table successfully!')
        else:
            print('\nAll exotic metals already exist in materials table.')
            
    except Exception as e:
        db.rollback()
        print(f'Error checking/updating materials table: {e}')
        raise
    finally:
        db.close()

if __name__ == '__main__':
    check_materials_table() 