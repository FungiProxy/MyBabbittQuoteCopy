"""
Script to clean up product options in the database for all product families.
This script:
1. Removes duplicate options
2. Removes core options from additional options
3. Logs all changes made
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

from src.core.database import SessionLocal
from src.core.models import Option, ProductFamily

# Set up logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Core options that should not appear in additional options
CORE_OPTIONS = {
    'Voltage',
    'Material',
    'Length',
    'Probe Length',
    'Housing',
    'Connection Type',
    'Process Connection',
    'Receiver Enclosure',
}


def setup_log_file():
    """Create a log file with timestamp."""
    log_dir = Path(__file__).resolve().parent.parent.parent / 'legacy' / 'logs'
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'product_options_cleanup_{timestamp}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(file_handler)
    return log_file


def get_product_families(db) -> List[ProductFamily]:
    """Get all product families."""
    return db.query(ProductFamily).all()


def get_family_options(db, family_name: str) -> List[Option]:
    """Get all options associated with a product family."""
    return (
        db.query(Option).filter(Option.product_families.like(f'%{family_name}%')).all()
    )


def remove_duplicates(db, options: List[Option]) -> Set[str]:
    """Remove duplicate options, keeping the first occurrence."""
    seen_names = set()
    duplicates = set()

    for option in options:
        if option.name in seen_names:
            logger.info(f'Removing duplicate option: {option.name}')
            db.delete(option)
            duplicates.add(option.name)
        else:
            seen_names.add(option.name)

    return duplicates


def remove_core_options(db, options: List[Option]) -> Set[str]:
    """Remove core options from additional options."""
    removed = set()

    for option in options:
        if option.name in CORE_OPTIONS:
            logger.info(f'Removing core option from additional options: {option.name}')
            db.delete(option)
            removed.add(option.name)

    return removed


def cleanup_family(db, family: ProductFamily) -> Dict[str, Set[str]]:
    """Clean up options for a specific product family."""
    logger.info(f'\nProcessing family: {family.name} (ID: {family.id})')

    # Get all options for this family
    options = get_family_options(db, family.name)
    logger.info(f'Found {len(options)} options for {family.name}')

    # Remove duplicates
    duplicates = remove_duplicates(db, options)
    logger.info(f'Removed {len(duplicates)} duplicate options: {duplicates}')

    # Get remaining options after duplicate removal
    remaining_options = get_family_options(db, family.name)

    # Remove core options
    removed_core = remove_core_options(db, remaining_options)
    logger.info(f'Removed {len(removed_core)} core options: {removed_core}')

    # Log final state
    final_options = get_family_options(db, family.name)
    logger.info(f'Final state: {len(final_options)} options remaining')
    for option in final_options:
        logger.info(f'Remaining option: {option.name}')

    return {
        'duplicates': duplicates,
        'removed_core': removed_core,
        'remaining': {opt.name for opt in final_options},
    }


def main():
    # Set up logging
    log_file = setup_log_file()
    logger.info('Starting product options cleanup')

    # Create database session
    db = SessionLocal()

    try:
        # Get all product families
        families = get_product_families(db)
        logger.info(f'Found {len(families)} product families')

        # Process each family
        results = {}
        for family in families:
            results[family.name] = cleanup_family(db, family)

        # Commit changes
        db.commit()

        # Print summary
        logger.info('\nCleanup Summary:')
        for family_name, result in results.items():
            logger.info(f'\n{family_name}:')
            logger.info(f"  Duplicates removed: {len(result['duplicates'])}")
            logger.info(f"  Core options removed: {len(result['removed_core'])}")
            logger.info(f"  Remaining options: {len(result['remaining'])}")

        logger.info(f'\nCleanup complete. Log file: {log_file}')

    except Exception as e:
        logger.error(f'Error during cleanup: {e!s}', exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    main()
