import json

from src.core.database import SessionLocal
from src.core.models.option import Option
from src.core.models.product_variant import ProductFamily, ProductVariant
from src.core.models.spare_part import SparePart
from src.core.services.product_service import ProductService

REQUIRED_FAMILY_FIELDS = ['name', 'base_model', 'options']
REQUIRED_BASE_MODEL_FIELDS = [
    'model_number',
    'description',
    'base_price',
    'base_length',
    'voltage',
    'material',
]
REQUIRED_OPTION_FIELDS = ['name', 'choices']
REQUIRED_SPARE_PART_FIELDS = ['name', 'price']


def is_number(value):
    return isinstance(value, (int, float))


def validate_json(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    families = data.get('families', [])
    errors = []
    for i, family in enumerate(families):
        fname = family.get('name', f'index {i}')
        # Family fields
        for field in REQUIRED_FAMILY_FIELDS:
            if field not in family:
                errors.append(f"Family '{fname}' missing field: {field}")
        # Base model fields
        base_model = family.get('base_model', {})
        for field in REQUIRED_BASE_MODEL_FIELDS:
            if field not in base_model:
                errors.append(f"Family '{fname}' base_model missing field: {field}")
        # Options
        options = family.get('options', [])
        if not isinstance(options, list) or not options:
            errors.append(f"Family '{fname}' has no options or options is not a list.")
        for opt in options:
            for field in REQUIRED_OPTION_FIELDS:
                if field not in opt:
                    errors.append(f"Family '{fname}' option missing field: {field}")
            # Choices
            if 'choices' in opt and (
                not isinstance(opt['choices'], list) or not opt['choices']
            ):
                errors.append(
                    f"Family '{fname}' option '{opt.get('name')}' has invalid or empty choices."
                )
            # Adders
            if 'adders' in opt:
                if not isinstance(opt['adders'], dict):
                    errors.append(
                        f"Family '{fname}' option '{opt.get('name')}' adders is not a dict."
                    )
                else:
                    for k, v in opt['adders'].items():
                        if v is not None and not is_number(v):
                            errors.append(
                                f"Family '{fname}' option '{opt.get('name')}' adder for '{k}' is not a number or null."
                            )
            # Notes/rules
            if 'notes' in opt and not isinstance(opt['notes'], str):
                errors.append(
                    f"Family '{fname}' option '{opt.get('name')}' notes is not a string."
                )
            if 'rules' in opt and not isinstance(opt['rules'], str):
                errors.append(
                    f"Family '{fname}' option '{opt.get('name')}' rules is not a string."
                )
        # Compatibility rules and notes
        for field in ['compatibility_rules', 'notes']:
            if field in family and not isinstance(family[field], list):
                errors.append(f"Family '{fname}' {field} is not a list.")
            elif field in family:
                for idx, item in enumerate(family[field]):
                    if not isinstance(item, str):
                        errors.append(
                            f"Family '{fname}' {field}[{idx}] is not a string."
                        )
        # Spare parts
        spare_parts = family.get('spare_parts', [])
        if not isinstance(spare_parts, list):
            errors.append(f"Family '{fname}' spare_parts is not a list.")
        for part in spare_parts:
            for field in REQUIRED_SPARE_PART_FIELDS:
                if field not in part:
                    errors.append(f"Family '{fname}' spare part missing field: {field}")
            if 'price' in part and not is_number(part['price']):
                errors.append(
                    f"Family '{fname}' spare part '{part.get('name')}' price is not a number."
                )
    return errors, families


# --- CLEAR DUPLICATES ---


def clear_product_data():
    db = SessionLocal()
    try:
        db.query(SparePart).delete()
        db.query(Option).delete()
        db.query(ProductVariant).delete()
        db.query(ProductFamily).delete()
        db.commit()
        print('All product families, variants, options, and spare parts deleted.')
    finally:
        db.close()


if __name__ == '__main__':
    # clear_product_data()  # <-- Commented out to prevent clearing on every run
    # print("Database cleared. You can now re-import your data using the import script.")

    errors, families = validate_json('data/internal_data_import.json')
    if errors:
        print('Validation errors found:')
        for error in errors:
            print(' -', error)
    else:
        print('JSON structure and content are valid.\n')
        print(f'Found {len(families)} product families.\n')
        for family in families:
            print(f"Family: {family.get('name')}")
            print(f"  Base Model: {family.get('base_model', {}).get('model_number')}")
            print(
                f"  Options: {[opt.get('name') for opt in family.get('options', [])]}"
            )
            print(
                f"  Spare Parts: {[part.get('name') for part in family.get('spare_parts', [])]}"
            )
            print()

    db = SessionLocal()
    families = ProductService().get_product_families(db)
    print('Product Families in database:')
    for f in families:
        print(f['name'])
    db.close()
