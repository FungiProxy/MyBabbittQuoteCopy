from src.core.database import SessionLocal
from src.core.models import Material


def remove_material_pricing_from_materials_table():
    db = SessionLocal()
    try:
        # Get all materials
        materials = db.query(Material).all()

        print(f'Found {len(materials)} materials to update:')

        for material in materials:
            print(f'  {material.code}: {material.name}')
            print(f'    Current base_price_adder: ${material.base_price_adder}')
            print(
                f'    Current length_adder_per_inch: ${material.length_adder_per_inch}'
            )
            print(
                f'    Current length_adder_per_foot: ${material.length_adder_per_foot}'
            )
            print(
                f'    Current nonstandard_length_surcharge: ${material.nonstandard_length_surcharge}'
            )

            # Set all pricing to 0 since pricing will come from options table
            material.base_price_adder = 0.0
            material.length_adder_per_inch = 0.0
            material.length_adder_per_foot = 0.0
            material.nonstandard_length_surcharge = 0.0
            material.has_nonstandard_length_surcharge = False

            print('    Updated all pricing to $0.00')

        db.commit()
        print('\n✅ Successfully removed pricing from materials table!')
        print('📝 Pricing will now be calculated from the options table only.')
        print(
            '📋 Materials table will only contain material definitions and availability.'
        )

    except Exception as e:
        db.rollback()
        print(f'❌ Error removing material pricing: {e}')
        raise
    finally:
        db.close()


if __name__ == '__main__':
    remove_material_pricing_from_materials_table()
