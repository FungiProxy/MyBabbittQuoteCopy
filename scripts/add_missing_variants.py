#!/usr/bin/env python3
"""
Script to add missing key product variants from the price list.
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.database import SessionLocal
from core.models.product_variant import ProductFamily, ProductVariant


def parse_price_list_variants():
    """Parse the price list to extract key variants and their prices."""

    # Key variants from the price list with their base prices
    variants_data = [
        # LS2000 variants
        (
            'LS2000',
            'LS2000-115VAC-S-10',
            'LS2000 Level Switch - 115VAC, 316SS, 10"',
            425.00,
            10.0,
            '115VAC',
            'S',
        ),
        (
            'LS2000',
            'LS2000-115VAC-H-10',
            'LS2000 Level Switch - 115VAC, Halar Coated, 10"',
            535.00,
            10.0,
            '115VAC',
            'H',
        ),
        (
            'LS2000',
            'LS2000-115VAC-U-4',
            'LS2000 Level Switch - 115VAC, UHMWPE Blind End, 4"',
            445.00,
            4.0,
            '115VAC',
            'U',
        ),
        (
            'LS2000',
            'LS2000-115VAC-T-4',
            'LS2000 Level Switch - 115VAC, Teflon Blind End, 4"',
            485.00,
            4.0,
            '115VAC',
            'T',
        ),
        # LS2100 variants
        (
            'LS2100',
            'LS2100-24VDC-S-10',
            'LS2100 Level Switch - 24VDC, 316SS, 10"',
            460.00,
            10.0,
            '24VDC',
            'S',
        ),
        (
            'LS2100',
            'LS2100-24VDC-H-10',
            'LS2100 Level Switch - 24VDC, Halar Coated, 10"',
            570.00,
            10.0,
            '24VDC',
            'H',
        ),
        # LS6000 variants
        (
            'LS6000',
            'LS6000-115VAC-S-10',
            'LS6000 Level Switch - 115VAC, 316SS, 10"',
            550.00,
            10.0,
            '115VAC',
            'S',
        ),
        (
            'LS6000',
            'LS6000-115VAC-H-10',
            'LS6000 Level Switch - 115VAC, Halar Coated, 10"',
            660.00,
            10.0,
            '115VAC',
            'H',
        ),
        # LS7000 variants
        (
            'LS7000',
            'LS7000-115VAC-S-10',
            'LS7000 Level Switch - 115VAC, 316SS, 10"',
            680.00,
            10.0,
            '115VAC',
            'S',
        ),
        (
            'LS7000',
            'LS7000-115VAC-H-10',
            'LS7000 Level Switch - 115VAC, Halar Coated, 10"',
            790.00,
            10.0,
            '115VAC',
            'H',
        ),
        # LS7000/2 variants
        (
            'LS7000/2',
            'LS7000/2-115VAC-H-10',
            'LS7000/2 Dual Point Level Switch - 115VAC, Halar Coated, 10"',
            770.00,
            10.0,
            '115VAC',
            'H',
        ),
        # LS8000 variants
        (
            'LS8000',
            'LS8000-115VAC-S-10',
            'LS8000 Remote Mounted Level Switch - 115VAC, 316SS, 10"',
            715.00,
            10.0,
            '115VAC',
            'S',
        ),
        (
            'LS8000',
            'LS8000-115VAC-H-10',
            'LS8000 Remote Mounted Level Switch - 115VAC, Halar Coated, 10"',
            825.00,
            10.0,
            '115VAC',
            'H',
        ),
        # LS8000/2 variants
        (
            'LS8000/2',
            'LS8000/2-115VAC-H-10',
            'LS8000/2 Remote Mounted Dual Point Level Switch - 115VAC, Halar Coated, 10"',
            850.00,
            10.0,
            '115VAC',
            'H',
        ),
        # LT9000 variants
        (
            'LT9000',
            'LT9000-115VAC-H-10',
            'LT9000 Level Transmitter - 115VAC, Halar Coated, 10"',
            855.00,
            10.0,
            '115VAC',
            'H',
        ),
        # Additional variants with different voltages
        (
            'LS2000',
            'LS2000-24VDC-S-10',
            'LS2000 Level Switch - 24VDC, 316SS, 10"',
            425.00,
            10.0,
            '24VDC',
            'S',
        ),
        (
            'LS2000',
            'LS2000-24VDC-H-10',
            'LS2000 Level Switch - 24VDC, Halar Coated, 10"',
            535.00,
            10.0,
            '24VDC',
            'H',
        ),
        (
            'LS2000',
            'LS2000-24VDC-U-4',
            'LS2000 Level Switch - 24VDC, UHMWPE Blind End, 4"',
            445.00,
            4.0,
            '24VDC',
            'U',
        ),
        (
            'LS2000',
            'LS2000-24VDC-T-4',
            'LS2000 Level Switch - 24VDC, Teflon Blind End, 4"',
            485.00,
            4.0,
            '24VDC',
            'T',
        ),
        (
            'LS6000',
            'LS6000-24VDC-S-10',
            'LS6000 Level Switch - 24VDC, 316SS, 10"',
            550.00,
            10.0,
            '24VDC',
            'S',
        ),
        (
            'LS6000',
            'LS6000-24VDC-H-10',
            'LS6000 Level Switch - 24VDC, Halar Coated, 10"',
            660.00,
            10.0,
            '24VDC',
            'H',
        ),
        (
            'LS6000',
            'LS6000-12VDC-S-10',
            'LS6000 Level Switch - 12VDC, 316SS, 10"',
            550.00,
            10.0,
            '12VDC',
            'S',
        ),
        (
            'LS6000',
            'LS6000-12VDC-H-10',
            'LS6000 Level Switch - 12VDC, Halar Coated, 10"',
            660.00,
            10.0,
            '12VDC',
            'H',
        ),
        (
            'LS6000',
            'LS6000-240VAC-S-10',
            'LS6000 Level Switch - 240VAC, 316SS, 10"',
            550.00,
            10.0,
            '240VAC',
            'S',
        ),
        (
            'LS6000',
            'LS6000-240VAC-H-10',
            'LS6000 Level Switch - 240VAC, Halar Coated, 10"',
            660.00,
            10.0,
            '240VAC',
            'H',
        ),
        (
            'LS7000',
            'LS7000-24VDC-S-10',
            'LS7000 Level Switch - 24VDC, 316SS, 10"',
            680.00,
            10.0,
            '24VDC',
            'S',
        ),
        (
            'LS7000',
            'LS7000-24VDC-H-10',
            'LS7000 Level Switch - 24VDC, Halar Coated, 10"',
            790.00,
            10.0,
            '24VDC',
            'H',
        ),
        (
            'LS7000',
            'LS7000-12VDC-S-10',
            'LS7000 Level Switch - 12VDC, 316SS, 10"',
            680.00,
            10.0,
            '12VDC',
            'S',
        ),
        (
            'LS7000',
            'LS7000-12VDC-H-10',
            'LS7000 Level Switch - 12VDC, Halar Coated, 10"',
            790.00,
            10.0,
            '12VDC',
            'H',
        ),
        (
            'LS7000',
            'LS7000-240VAC-S-10',
            'LS7000 Level Switch - 240VAC, 316SS, 10"',
            680.00,
            10.0,
            '240VAC',
            'S',
        ),
        (
            'LS7000',
            'LS7000-240VAC-H-10',
            'LS7000 Level Switch - 240VAC, Halar Coated, 10"',
            790.00,
            10.0,
            '240VAC',
            'H',
        ),
        (
            'LS7000/2',
            'LS7000/2-24VDC-H-10',
            'LS7000/2 Dual Point Level Switch - 24VDC, Halar Coated, 10"',
            770.00,
            10.0,
            '24VDC',
            'H',
        ),
        (
            'LS7000/2',
            'LS7000/2-12VDC-H-10',
            'LS7000/2 Dual Point Level Switch - 12VDC, Halar Coated, 10"',
            770.00,
            10.0,
            '12VDC',
            'H',
        ),
        (
            'LS7000/2',
            'LS7000/2-240VAC-H-10',
            'LS7000/2 Dual Point Level Switch - 240VAC, Halar Coated, 10"',
            770.00,
            10.0,
            '240VAC',
            'H',
        ),
        (
            'LS8000',
            'LS8000-24VDC-S-10',
            'LS8000 Remote Mounted Level Switch - 24VDC, 316SS, 10"',
            715.00,
            10.0,
            '24VDC',
            'S',
        ),
        (
            'LS8000',
            'LS8000-24VDC-H-10',
            'LS8000 Remote Mounted Level Switch - 24VDC, Halar Coated, 10"',
            825.00,
            10.0,
            '24VDC',
            'H',
        ),
        (
            'LS8000',
            'LS8000-12VDC-S-10',
            'LS8000 Remote Mounted Level Switch - 12VDC, 316SS, 10"',
            715.00,
            10.0,
            '12VDC',
            'S',
        ),
        (
            'LS8000',
            'LS8000-12VDC-H-10',
            'LS8000 Remote Mounted Level Switch - 12VDC, Halar Coated, 10"',
            825.00,
            10.0,
            '12VDC',
            'H',
        ),
        (
            'LS8000',
            'LS8000-240VAC-S-10',
            'LS8000 Remote Mounted Level Switch - 240VAC, 316SS, 10"',
            715.00,
            10.0,
            '240VAC',
            'S',
        ),
        (
            'LS8000',
            'LS8000-240VAC-H-10',
            'LS8000 Remote Mounted Level Switch - 240VAC, Halar Coated, 10"',
            825.00,
            10.0,
            '240VAC',
            'H',
        ),
        (
            'LS8000/2',
            'LS8000/2-24VDC-H-10',
            'LS8000/2 Remote Mounted Dual Point Level Switch - 24VDC, Halar Coated, 10"',
            850.00,
            10.0,
            '24VDC',
            'H',
        ),
        (
            'LS8000/2',
            'LS8000/2-12VDC-H-10',
            'LS8000/2 Remote Mounted Dual Point Level Switch - 12VDC, Halar Coated, 10"',
            850.00,
            10.0,
            '12VDC',
            'H',
        ),
        (
            'LS8000/2',
            'LS8000/2-240VAC-H-10',
            'LS8000/2 Remote Mounted Dual Point Level Switch - 240VAC, Halar Coated, 10"',
            850.00,
            10.0,
            '240VAC',
            'H',
        ),
        (
            'LT9000',
            'LT9000-24VDC-H-10',
            'LT9000 Level Transmitter - 24VDC, Halar Coated, 10"',
            855.00,
            10.0,
            '24VDC',
            'H',
        ),
        (
            'LT9000',
            'LT9000-230VAC-H-10',
            'LT9000 Level Transmitter - 230VAC, Halar Coated, 10"',
            855.00,
            10.0,
            '230VAC',
            'H',
        ),
        # FS10000 variants
        (
            'FS10000',
            'FS10000-115VAC-S-6',
            'FS10000 Dry Material Flow Switch - 115VAC, 316SS, 6"',
            1885.00,
            6.0,
            '115VAC',
            'S',
        ),
        (
            'FS10000',
            'FS10000-230VAC-S-6',
            'FS10000 Dry Material Flow Switch - 230VAC, 316SS, 6"',
            1885.00,
            6.0,
            '230VAC',
            'S',
        ),
    ]

    return variants_data


def add_missing_variants():
    """Add missing key product variants to the database."""
    db = SessionLocal()

    try:
        print('=' * 60)
        print('ADDING MISSING PRODUCT VARIANTS')
        print('=' * 60)

        # Get product family mapping
        families = {f.name: f.id for f in db.query(ProductFamily).all()}
        print(f'Found {len(families)} product families')

        # Get existing variants to avoid duplicates
        existing_variants = {v.model_number for v in db.query(ProductVariant).all()}
        print(f'Found {len(existing_variants)} existing variants')

        # Parse variants from price list
        variants_data = parse_price_list_variants()
        print(f'Price list contains {len(variants_data)} key variants')

        # Track statistics
        added_count = 0
        skipped_count = 0
        missing_family_count = 0

        for (
            family_name,
            model_number,
            description,
            base_price,
            base_length,
            voltage,
            material,
        ) in variants_data:

            # Check if variant already exists
            if model_number in existing_variants:
                print(f'⏭️  Skipping existing: {model_number}')
                skipped_count += 1
                continue

            # Check if family exists
            if family_name not in families:
                print(f'❌ Missing family: {family_name}')
                missing_family_count += 1
                continue

            # Create the variant
            variant = ProductVariant(
                product_family_id=families[family_name],
                model_number=model_number,
                description=description,
                base_price=base_price,
                base_length=base_length,
                voltage=voltage,
                material=material,
            )

            db.add(variant)
            added_count += 1
            print(f'✅ Added: {model_number} - ${base_price}')

        # Commit all changes
        db.commit()

        # Print summary
        print('\n' + '=' * 60)
        print('SUMMARY')
        print('=' * 60)
        print(f'Variants added: {added_count}')
        print(f'Variants skipped (already exist): {skipped_count}')
        print(f'Missing families: {missing_family_count}')

        # Verify final count
        final_count = db.query(ProductVariant).count()
        print(f'Total variants in database: {final_count}')

        if added_count > 0:
            print('\n✅ Successfully added missing key variants from price list!')
        else:
            print('\nℹ️  No new variants were added (all already exist)')

    except Exception as e:
        print(f'❌ Error: {e}')
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    add_missing_variants()
