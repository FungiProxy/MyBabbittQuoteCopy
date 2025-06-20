import re
import sys
from pathlib import Path

# Add project root to path to allow importing project modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text

from src.core.database import engine


def parse_price_list(filepath='data/price_list.txt'):
    """
    Parses the price list to extract a canonical list of product families and variants.

    Returns:
        A dictionary containing 'families' (a set of names) and 'variants'
        (a dict mapping family names to a set of model numbers).
    """
    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Price list not found at '{filepath}'")
        return None

    lines = content.split('\n')

    expected_data = {'families': set(), 'variants': {}}

    # Regex to find a product family header, e.g., "LS2000 LEVEL SWITCH"
    # It captures the core identifier like "LS2000" or "LS7000/2"
    family_pattern = re.compile(
        r'^(LS\w+(?:/\d)?|FS\w+|LT\w+)\s+.*?(?:LEVEL|SWITCH|SYSTEM|PROBE|TRANSMITTER)'
    )

    # Regex to find a product variant line, e.g., "LS2000-115VAC-S-10" $425.00"
    # It captures the full model number.
    variant_pattern = re.compile(r'^\s*((?:LS|FS|LT)[\w./-]+?)\s+.*?\s+\$[\d,.]+')

    current_family = None
    for line in lines:
        family_match = family_pattern.match(line)
        if family_match:
            current_family = family_match.group(1)
            # Handle cases like LS7000/2 where variant names might not repeat the full prefix
            if '/' in current_family:
                current_family = current_family.split('/')[
                    0
                ]  # Normalize to LS7000 for grouping

            expected_data['families'].add(current_family)
            if current_family not in expected_data['variants']:
                expected_data['variants'][current_family] = set()
            continue

        if current_family:
            variant_match = variant_pattern.match(line)
            if variant_match:
                model_number = variant_match.group(1).strip()
                # Ensure the variant belongs to the current family context
                if model_number.startswith(current_family):
                    expected_data['variants'][current_family].add(model_number)

    # Clean up any families that were detected but had no variants found under them
    expected_data['families'] = {f for f, v in expected_data['variants'].items() if v}

    return expected_data


def audit_database():
    """
    Connects to the database, compares its contents against the price list,
    and generates a detailed audit report of discrepancies.
    """
    print('=' * 80)
    print('STARTING DATABASE AUDIT')
    print('=' * 80)

    # Step 1: Parse the price list to get the "source of truth"
    print('\n[1/3] Parsing price_list.txt...')
    expected_data = parse_price_list()
    if not expected_data:
        return  # Stop if parsing fails

    print(f" -> Found {len(expected_data['families'])} expected product families.")
    total_variants = sum(len(v) for v in expected_data['variants'].values())
    print(f' -> Found {total_variants} expected product variants.')

    # Step 2: Connect to the database and query current data
    print('\n[2/3] Querying database...')
    db_data = {
        'families': set(),
        'variants': {},  # Maps family to a set of variant model numbers
    }

    try:
        with engine.connect() as connection:
            # Get product families from the database
            result_families = connection.execute(
                text('SELECT name FROM product_families')
            )
            db_data['families'] = {row[0] for row in result_families}
            print(f" -> Found {len(db_data['families'])} families in the database.")

            # Get product variants from the database by joining with product_families
            query = """
            SELECT pv.model_number, pf.name
            FROM product_variants pv
            JOIN product_families pf ON pv.product_family_id = pf.id
            """
            result_variants = connection.execute(text(query))
            for model, family in result_variants:
                if family not in db_data['variants']:
                    db_data['variants'][family] = set()
                db_data['variants'][family].add(model)
            total_db_variants = sum(len(v) for v in db_data['variants'].values())
            print(f' -> Found {total_db_variants} variants in the database.')

    except Exception as e:
        print(
            ' -> DATABASE ERROR: Could not query database. Please ensure it exists and is accessible.'
        )
        print(f'    Details: {e}')
        return

    # Step 3: Compare data and generate the report
    print('\n[3/3] Generating audit report...')
    print('-' * 80)
    print('AUDIT REPORT')
    print('-' * 80)

    # --- Product Families ---
    print('\n--- Product Families ---')
    expected_families = expected_data['families']
    db_families = db_data['families']
    missing_families = expected_families - db_families
    extra_families = db_families - expected_families

    if not missing_families and not extra_families:
        print(' -> STATUS: OK. Product families in the database match the price list.')
    else:
        if missing_families:
            print(
                f" -> MISSING FROM DB ({len(missing_families)}): {', '.join(sorted(missing_families))}"
            )
        if extra_families:
            print(
                f" -> EXTRA IN DB ({len(extra_families)}): {', '.join(sorted(extra_families))}"
            )

    # --- Product Variants (grouped by family) ---
    print('\n--- Product Variants ---')
    all_families = sorted(expected_families.union(db_families))
    for family in all_families:
        print(f'\n[{family}]')
        expected_variants = expected_data['variants'].get(family, set())
        db_variants = db_data['variants'].get(family, set())

        missing_variants = expected_variants - db_variants
        extra_variants = db_variants - expected_variants

        if not missing_variants and not extra_variants:
            print(
                ' -> STATUS: OK. All variants from price list are present in the database.'
            )
        else:
            if missing_variants:
                print(f'    -> MISSING FROM DB ({len(missing_variants)}):')
                for variant in sorted(missing_variants)[:5]:  # Show first 5
                    print(f'        - {variant}')
                if len(missing_variants) > 5:
                    print(f'        - ... and {len(missing_variants) - 5} more.')
            if extra_variants:
                print(f'    -> EXTRA IN DB ({len(extra_variants)}):')
                for variant in sorted(extra_variants)[:5]:  # Show first 5
                    print(f'        - {variant}')
                if len(extra_variants) > 5:
                    print(f'        - ... and {len(extra_variants) - 5} more.')

    print('\n' + '=' * 80)
    print('AUDIT COMPLETE')
    print('=' * 80)


if __name__ == '__main__':
    audit_database()
