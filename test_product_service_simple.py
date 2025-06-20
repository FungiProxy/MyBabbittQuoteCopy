#!/usr/bin/env python3
"""
Simple test for the updated ProductService.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily
from src.core.services.product_service import ProductService


def test_get_additional_options():
    """Test the get_additional_options method with a known product family."""
    db = SessionLocal()
    try:
        # Get a known product family
        family = db.query(ProductFamily).first()
        if not family:
            print("No product families found in database")
            return False

        print(f"Testing with product family: {family.name}")

        # Test the method
        service = ProductService()
        options = service.get_additional_options(db, family.name)

        print(f"Found {len(options)} options")

        # Basic assertions
        assert isinstance(options, list), "Should return a list"

        if options:
            # Check structure of first option
            first_option = options[0]
            assert "name" in first_option, "Option should have 'name' field"
            assert "category" in first_option, "Option should have 'category' field"
            assert "choices" in first_option, "Option should have 'choices' field"
            assert "adders" in first_option, "Option should have 'adders' field"

            print(f"First option: {first_option['name']} ({first_option['category']})")
            print(f"  Choices: {first_option['choices']}")
            print(f"  Adders: {first_option['adders']}")

        print("✅ Test passed!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = test_get_additional_options()
    sys.exit(0 if success else 1)
