#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def add_ls8000_materials():
    db = SessionLocal()
    try:
        print('Adding U and T materials to LS8000...')

        # Get LS8000 family
        family = db.query(ProductFamily).filter(ProductFamily.name == 'LS8000').first()
        if not family:
            print('❌ LS8000 product family not found!')
            return

        print(f'✅ Found LS8000 family (ID: {family.id})')

        # Materials to add with their standard adders
        materials_to_add = [
            ('U', 20.0),  # UHMWPE Blind End
            ('T', 60.0),  # Teflon Blind End
        ]

        for material_code, adder in materials_to_add:
            print(f'\nAdding {material_code} material (adder: ${adder:.2f})...')

            # Find the material option that contains this code
            material_option = None
            all_material_options = (
                db.query(Option).filter(Option.category == 'Material').all()
            )
            for opt in all_material_options:
                if opt.choices and isinstance(opt.choices, list):
                    for choice in opt.choices:
                        if (
                            isinstance(choice, dict)
                            and choice.get('code') == material_code
                        ):
                            material_option = opt
                            break
                    if material_option:
                        break

            if material_option:
                # Check if this material is already assigned to LS8000
                existing_assignment = (
                    db.query(ProductFamilyOption)
                    .filter(ProductFamilyOption.product_family_id == family.id)
                    .filter(ProductFamilyOption.option_id == material_option.id)
                    .first()
                )

                if existing_assignment:
                    print(f'  ⚠️  {material_code} material already assigned to LS8000')
                else:
                    # Create the assignment
                    assignment = ProductFamilyOption(
                        product_family_id=family.id,
                        option_id=material_option.id,
                        is_available=1,
                    )
                    db.add(assignment)
                    print(f'  ✅ Added {material_code} material to LS8000')
            else:
                print(f'  ❌ Material option for {material_code} not found!')

        db.commit()
        print('\n✅ Successfully added materials to LS8000')

        # Verify the changes
        print('\n=== VERIFICATION ===')
        material_assignments = (
            db.query(ProductFamilyOption)
            .filter(ProductFamilyOption.product_family_id == family.id)
            .join(Option)
            .filter(Option.category == 'Material')
            .all()
        )

        current_materials = []
        for assignment in material_assignments:
            option = assignment.option
            if option.choices and isinstance(option.choices, list):
                for choice in option.choices:
                    if isinstance(choice, dict):
                        current_materials.append(choice.get('code'))

        print(f'LS8000 now has materials: {sorted(current_materials)}')

        # Test ProductService output
        from src.core.services.product_service import ProductService

        product_service = ProductService()
        additional_options = product_service.get_additional_options(db, 'LS8000')
        material_options = [
            opt for opt in additional_options if opt.get('category') == 'Material'
        ]

        print(f'\nProductService returns {len(material_options)} material options:')
        for opt in material_options:
            print(
                f"  - {opt.get('name')}: choices={opt.get('choices')}, adders={opt.get('adders')}"
            )

    except Exception as e:
        print(f'Error: {e}')
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    add_ls8000_materials()
