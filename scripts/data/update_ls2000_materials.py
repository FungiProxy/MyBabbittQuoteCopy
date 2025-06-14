"""
Script to update LS2000 material options in the database to use single-letter codes.
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.core.database import SessionLocal
from src.core.models.option import Option


def update_ls2000_materials():
    """Update LS2000 material options to use single-letter codes."""
    db = SessionLocal()
    try:
        # Get the existing material option
        material_option = (
            db.query(Option)
            .filter(Option.name == "Material", Option.product_families == "LS2000")
            .first()
        )

        if material_option:
            # Update the choices and adders
            material_option.choices = ["S", "H", "U", "T"]
            material_option.adders = {"S": 0, "H": 50, "U": 30, "T": 40}
            material_option.rules = "S=316SS, H=Halar, U=UHMWPE, T=Teflon"

            db.commit()
            print("Successfully updated LS2000 material options")
        else:
            print("LS2000 material option not found in database")

    except Exception as e:
        print(f"Error updating LS2000 material options: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    update_ls2000_materials()
