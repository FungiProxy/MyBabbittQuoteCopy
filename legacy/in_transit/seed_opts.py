import os
import sys

from sqlalchemy import text
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.core.models.option import Option


def seed_options(db: Session):
    """Seeds the database with product options."""
    options_data = [
        # O-Rings
        {
            "name": "O-Ring Material",
            "description": "O-Ring material selection",
            "price": 0.0,
            "price_type": "fixed",
            "category": "O-ring Material",
            "choices": ["Viton", "Silicon", "Buna-N", "EPDM", "PTFE", "Kalrez"],
            "adders": {
                "Viton": 0,
                "Silicon": 0,
                "Buna-N": 0,
                "EPDM": 0,
                "PTFE": 0,
                "Kalrez": 295,
            },
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
        },
        # Exotic Metals
        {
            "name": "Exotic Metal Material",
            "description": "Exotic Metal material selection",
            "price": 0.0,
            "price_type": "fixed",
            "category": "Exotic Metal Material",
            "choices": ["Alloy 20", "Hastelloy-C-276", "Hastelloy-B", "Titanium"],
            "adders": {
                "Alloy 20": 0,
                "Hastelloy-C-276": 0,
                "Hastelloy-B": 0,
                "Titanium": 0,
            },
            "product_families": "LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500",
        }
    ]