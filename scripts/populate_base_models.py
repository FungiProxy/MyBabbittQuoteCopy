#!/usr/bin/env python3
"""
Populate the base_models table with the immortalized base model data.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.config.base_models import BASE_MODELS
from src.core.database import SessionLocal
from src.core.models import BaseModel, ProductFamily


def populate_base_models():
    db = SessionLocal()
    try:
        for family_name, config in BASE_MODELS.items():
            family = db.query(ProductFamily).filter_by(name=family_name).first()
            if not family:
                print(f"Product family '{family_name}' not found. Skipping.")
                continue
            # Check if already exists
            existing = (
                db.query(BaseModel).filter_by(product_family_id=family.id).first()
            )
            if existing:
                print(f"Base model for '{family_name}' already exists. Skipping.")
                continue
            base_model = BaseModel(
                product_family_id=family.id,
                model_number=config["model_number"],
                description=config["description"],
                base_price=config["base_price"],
                base_length=config["base_length"],
                voltage=config["voltage"],
                material=config["material"],
                process_connection_type=config.get("process_connection_type"),
                process_connection_size=config.get("process_connection_size"),
            )
            db.add(base_model)
            print(
                f"Added base model for {family_name}: {config['model_number']} (${config['base_price']})"
            )
        db.commit()
        print("\n✅ Base models table populated.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    populate_base_models()
