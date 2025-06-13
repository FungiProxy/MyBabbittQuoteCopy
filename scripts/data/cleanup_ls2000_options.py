"""
Script to clean up the LS2000 options in the database.
This script:
1. Removes duplicate options
2. Removes core options from additional options
3. Logs all changes made
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Set

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import SessionLocal
from src.core.models import Option, ProductFamily

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Core options that should not appear in additional options
CORE_OPTIONS = {
    'Voltage',
    'Material',
    'Length',
    'Probe Length',
    'Housing',
    'Connection Type'
}

def setup_log_file():
    """Create a log file with timestamp."""
    log_dir = Path(__file__).resolve().parent.parent.parent / "legacy" / "logs"
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"ls2000_cleanup_{timestamp}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    return log_file

def get_ls2000_options(db) -> List[Option]:
    """Get all options associated with LS2000."""
    return (
        db.query(Option)
        .filter(Option.product_families.like('%LS2000%'))
        .all()
    )

def remove_duplicates(db, options: List[Option]) -> Set[str]:
    """Remove duplicate options, keeping the first occurrence."""
    seen_names = set()
    duplicates = set()
    
    for option in options:
        if option.name in seen_names:
            logger.info(f"Removing duplicate option: {option.name}")
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
            logger.info(f"Removing core option from additional options: {option.name}")
            db.delete(option)
            removed.add(option.name)
    
    return removed

def main():
    # Set up logging
    log_file = setup_log_file()
    logger.info("Starting LS2000 options cleanup")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Get all LS2000 options
        options = get_ls2000_options(db)
        logger.info(f"Found {len(options)} options for LS2000")
        
        # Remove duplicates
        duplicates = remove_duplicates(db, options)
        logger.info(f"Removed {len(duplicates)} duplicate options: {duplicates}")
        
        # Get remaining options after duplicate removal
        remaining_options = get_ls2000_options(db)
        
        # Remove core options
        removed_core = remove_core_options(db, remaining_options)
        logger.info(f"Removed {len(removed_core)} core options: {removed_core}")
        
        # Commit changes
        db.commit()
        
        # Log final state
        final_options = get_ls2000_options(db)
        logger.info(f"Final state: {len(final_options)} options remaining")
        for option in final_options:
            logger.info(f"Remaining option: {option.name}")
        
        logger.info(f"Cleanup complete. Log file: {log_file}")
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 