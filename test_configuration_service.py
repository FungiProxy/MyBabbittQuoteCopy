#!/usr/bin/env python3
"""
Simple test for the updated ConfigurationService.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService


def test_configuration_service():
    """Test the ConfigurationService with the new unified options structure."""
    print("Testing ConfigurationService with unified options structure...")

    db = SessionLocal()
    try:
        # Create services
        product_service = ProductService()
        config_service = ConfigurationService(db, product_service)

        # Get a known product family
        family_objs = product_service.get_product_families(db)
        if not family_objs:
            print("❌ No product families found in database")
            return False

        first_family = family_objs[0]
        print(f"✅ Testing with product family: {first_family['name']}")

        # Get variants for this family
        variants = product_service.get_variants_for_family(db, first_family["id"])
        if not variants:
            print("❌ No variants found for product family")
            return False

        first_variant = variants[0]
        base_product_info = {
            "id": first_family["id"],
            "name": first_family["name"],
            "base_price": first_variant["base_price"],
            "base_length": first_variant["base_length"],
            "voltage": first_variant["voltage"],
            "material": first_variant["material"],
        }

        # Start configuration
        config_service.start_configuration(
            product_family_id=first_family["id"],
            product_family_name=first_family["name"],
            base_product_info=base_product_info,
        )

        print("✅ Configuration started successfully")

        # Test option selection
        config_service.select_option("Material", "S")
        print("✅ Material option selected")

        # Test getting option price
        material_price = config_service._get_option_price("Material", "S")
        print(f"✅ Material price: ${material_price:.2f}")

        # Test price calculation
        final_price = config_service.current_config.final_price
        print(f"✅ Final price calculated: ${final_price:.2f}")

        # Test model number generation
        model_number = config_service.generate_model_number()
        print(f"✅ Model number generated: {model_number}")

        print("✅ ConfigurationService test passed!")
        return True

    except Exception as e:
        print(f"❌ ConfigurationService test failed: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = test_configuration_service()
    sys.exit(0 if success else 1)
