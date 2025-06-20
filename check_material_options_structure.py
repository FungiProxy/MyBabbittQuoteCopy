from src.core.database import SessionLocal
from src.core.models import Option


def check_material_options_structure():
    db = SessionLocal()
    try:
        # Get all material options
        material_options = db.query(Option).filter(Option.category == 'Materials').all()

        print(f'Found {len(material_options)} material options:')

        for option in material_options:
            print(f'\n  Product Families: {option.product_families}')
            print(f'  Choices: {option.choices}')
            print(f'  Adders: {option.adders}')
            print(f'  Rules: {option.rules}')

    except Exception as e:
        print(f'❌ Error checking material options: {e}')
        raise
    finally:
        db.close()


if __name__ == '__main__':
    check_material_options_structure()
