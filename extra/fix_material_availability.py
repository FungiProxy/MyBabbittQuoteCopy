import json
import logging
import sys
from pathlib import Path

# Add project root to the Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified
from src.core.database import engine
from src.core.models import Option

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)

# Define the product families and the materials that should be available for them.
# This is based on the errors found in the traceback.
PRODUCT_MATERIAL_MAP = {
    "LS8500": ["TS"],
    "FS10000": ["CPVC", "U", "H"],
    "LS7000/2": ["S"],
    "LS7500": ["U"],
}

def add_missing_materials():
    """
    Adds missing material choices to product families in the options table.
    """
    session = Session()
    try:
        for product_family, materials_to_add in PRODUCT_MATERIAL_MAP.items():
            # Find the material option for the product family
            material_option = session.query(Option).filter(
                Option.name == "Material",
                Option.category == "Material",
                Option.product_families.like(f"%{product_family}%")
            ).first()

            if not material_option:
                logger.warning(f"No material option found for product family: {product_family}. Skipping.")
                continue

            # Get the current list of choices
            choices = material_option.choices
            if choices is None:
                choices = []
            
            existing_material_codes = {
                choice['code'] if isinstance(choice, dict) else str(choice)
                for choice in choices
            }

            # Add new materials if they aren't already in the list
            for material_code in materials_to_add:
                if material_code not in existing_material_codes:
                    # We need to find the display name for the material code to add the full dict
                    # This is a simplification; in a real scenario, you might query a materials table.
                    # For now, we'll create a simplified display name.
                    display_name = f"{material_code} - (Added by script)"
                    if material_code == 'S':
                        display_name = "S - 316 Stainless Steel"
                    elif material_code == 'TS':
                        display_name = "TS - Teflon Sleeve"
                    elif material_code == 'CPVC':
                        display_name = "CPVC - CPVC"
                    elif material_code == 'U':
                        display_name = "U - Uranus B6"
                    elif material_code == 'H':
                        display_name = "H - Halar"

                    new_choice = {"code": material_code, "display_name": display_name}
                    choices.append(new_choice)
                    logger.info(f"Adding material '{material_code}' to '{product_family}'.")
            
            flag_modified(material_option, "choices")

        session.commit()
        logger.info("Successfully added missing materials to the database.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    add_missing_materials() 