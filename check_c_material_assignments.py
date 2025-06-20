#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def check_c_material_assignments():
    db = SessionLocal()
    try:
        print('=== CHECKING C MATERIAL ASSIGNMENTS ===\n')

        # Check all product families that have C material assigned
        c_material_option = (
            db.query(Option)
            .filter(
                Option.category == 'Material', Option.choices.contains([{'code': 'C'}])
            )
            .first()
        )

        if not c_material_option:
            print('❌ C material option not found!')
            return

        print(f'C Material Option ID: {c_material_option.id}')
        print(f'C Material Adders: {c_material_option.adders}')

        # Find all families that have C material assigned
        c_assignments = (
            db.query(ProductFamilyOption)
            .filter(ProductFamilyOption.option_id == c_material_option.id)
            .all()
        )

        print(f'\nC Material Assignments: {len(c_assignments)}')

        for assignment in c_assignments:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.id == assignment.product_family_id)
                .first()
            )
            print(f'  - {family.name} (ID: {family.id})')

        # Check for duplicate assignments
        print('\n=== CHECKING FOR DUPLICATE ASSIGNMENTS ===')
        for assignment in c_assignments:
            family = (
                db.query(ProductFamily)
                .filter(ProductFamily.id == assignment.product_family_id)
                .first()
            )

            # Count how many times this family has C material assigned
            c_count = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.product_family_id == family.id)
                .filter(ProductFamilyOption.option_id == c_material_option.id)
                .count()
            )

            if c_count > 1:
                print(f'  ❌ {family.name} has {c_count} C material assignments!')
            else:
                print(f'  ✅ {family.name} has {c_count} C material assignment')

        # Check if there are multiple material options with C code
        print('\n=== CHECKING FOR MULTIPLE C MATERIAL OPTIONS ===')
        all_c_options = db.query(Option).filter(Option.category == 'Material').all()

        c_options = []
        for opt in all_c_options:
            if opt.choices and isinstance(opt.choices, list):
                for choice in opt.choices:
                    if isinstance(choice, dict) and choice.get('code') == 'C':
                        c_options.append(opt)
                        break

        print(f'Found {len(c_options)} material options with C code:')
        for i, opt in enumerate(c_options):
            print(f'  {i+1}. ID: {opt.id}, Name: {opt.name}, Adders: {opt.adders}')

    except Exception as e:
        print(f'Error: {e}')
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == '__main__':
    check_c_material_assignments()
