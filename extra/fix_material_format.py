#!/usr/bin/env python3
"""
Fix the mixed material format in the database.
Convert exotic metal strings to proper dictionary format to match standard materials.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging

from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.models.option import Option

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fix_material_format():
    """Fix the mixed material format in the database."""
    db: Session = next(get_db())

    try:
        # Get all material options
        material_options = db.query(Option).filter(Option.name == "Material").all()

        logger.info(f"Found {len(material_options)} material options to fix")

        for option in material_options:
            choices = option.choices

            logger.info(f"Processing material option for family: {option.category}")
            logger.info(f"Original choices: {choices}")

            # Convert exotic metal strings to dictionary format
            updated_choices = []
            exotic_metal_descriptions = {
                "A": "A - Alloy 20",
                "HC": "HC - Hastelloy-C-276",
                "HB": "HB - Hastelloy-B",
                "TT": "TT - Titanium",
            }

            for choice in choices:
                if isinstance(choice, str) and choice in exotic_metal_descriptions:
                    # Convert exotic metal string to dictionary
                    updated_choice = {
                        "code": choice,
                        "display_name": exotic_metal_descriptions[choice],
                    }
                    updated_choices.append(updated_choice)
                    logger.info(f"Converted {choice} to {updated_choice}")
                else:
                    # Keep existing format (already dictionary or other string)
                    updated_choices.append(choice)

            # Update the option
            option.choices = updated_choices
            logger.info(f"Updated choices: {updated_choices}")

        # Commit changes
        db.commit()
        logger.info("Successfully updated material format in database")

        # Verify the fix
        logger.info("Verifying the fix...")
        material_options = db.query(Option).filter(Option.name == "Material").all()
        for option in material_options:
            choices = option.choices
            logger.info(
                f"Family {option.category} - All choices are now dictionaries: {all(isinstance(c, dict) for c in choices)}"
            )
            for choice in choices:
                logger.info(f"  {type(choice)}: {choice}")

    except Exception as e:
        logger.error(f"Error fixing material format: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    fix_material_format()
