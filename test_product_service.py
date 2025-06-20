#!/usr/bin/env python3
"""
Test script to verify ProductService functionality after database refactoring.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models import Option
from src.core.models.product_variant import ProductFamily as ProductFamilyModel


def test_database_models():
    """Test if the new unified options structure is working."""
    db = SessionLocal()
    try:
        # Test if we can query the new unified options
        options = db.query(Option).all()
        print(f"Found {len(options)} options in unified options table")

        # Test if we can query product families
        families = db.query(ProductFamilyModel).all()
        print(f"Found {len(families)} product families")

        # Test the association
        for family in families[:3]:  # Test first 3 families
            family_options = family.options
            print(f"Family {family.name} has {len(family_options)} options")

    except Exception as e:
        print(f"Error testing database models: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    test_database_models()
