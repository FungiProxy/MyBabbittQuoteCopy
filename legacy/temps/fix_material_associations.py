#!/usr/bin/env python3
"""
Fix material option associations for all product families.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging

from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fix_material_associations():
    """Ensure all product families have access to the material option."""
    db: Session = next(get_db())

    try:
        # Get the material option
        material_option = db.query(Option).filter(Option.name == "Material").first()
        if not material_option:
            logger.error("Material option not found")
            return

        logger.info(f"Found material option: {material_option.name}")

        # Get all product families
        families = db.query(ProductFamily).all()
        logger.info(f"Found {len(families)} product families")

        # Check which families already have the material option
        existing_associations = (
            db.query(ProductFamilyOption)
            .filter(ProductFamilyOption.option_id == material_option.id)
            .all()
        )

        existing_family_ids = {
            assoc.product_family_id for assoc in existing_associations
        }
        logger.info(f"Families with material option: {existing_family_ids}")

        # Add missing associations
        added_count = 0
        for family in families:
            if family.id not in existing_family_ids:
                # Create new association
                association = ProductFamilyOption(
                    product_family_id=family.id,
                    option_id=material_option.id,
                    is_available=1,
                )
                db.add(association)
                added_count += 1
                logger.info(f"Added material option to family: {family.name}")

        # Commit changes
        db.commit()
        logger.info(f"Added material option to {added_count} families")

        # Verify the fix
        logger.info("Verifying fix...")
        for family in families:
            materials = (
                db.query(Option)
                .join(Option.family_associations)
                .filter(
                    Option.family_associations.any(
                        product_family_id=family.id,
                        option_id=material_option.id,
                        is_available=1,
                    )
                )
                .all()
            )
            logger.info(f"Family {family.name}: {len(materials)} material options")

    except Exception as e:
        logger.error(f"Error fixing material associations: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    fix_material_associations()
