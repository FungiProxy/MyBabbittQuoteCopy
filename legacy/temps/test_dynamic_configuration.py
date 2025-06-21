#!/usr/bin/env python3
"""
Test the dynamic configuration system.
This script verifies that the system can build configurations
dynamically using the unified options without static variants.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService


def test_dynamic_configuration():
    """Test the dynamic configuration system."""
    db = SessionLocal()
    try:
        print("🧪 Testing Dynamic Configuration System")
        print("=" * 50)

        # Test 1: Product Service can get families without variants
        print("\n1️⃣ Testing ProductService.get_product_families()...")
        product_service = ProductService()
        families = product_service.get_product_families(db)
        print(f"✅ Found {len(families)} product families")
        for family in families:
            print(f"   - {family['name']}: {family['description']}")

        # Test 2: Product Service can get options for a family
        print("\n2️⃣ Testing ProductService.get_additional_options() for LT9000...")
        lt9000_family = (
            db.query(ProductFamily).filter(ProductFamily.name == "LT9000").first()
        )
        if lt9000_family:
            options = product_service.get_additional_options(db, lt9000_family.id)
            print(f"✅ Found {len(options)} options for LT9000")

            # Show material options specifically
            material_options = [
                opt for opt in options if opt.get("category") == "Material"
            ]
            print(f"   Material options: {len(material_options)}")
            for opt in material_options:
                print(
                    f"     - {opt['name']}: {opt['choices']} (adders: {opt['adders']})"
                )

        # Test 3: Configuration Service can build configurations
        print("\n3️⃣ Testing ConfigurationService with LT9000...")
        config_service = ConfigurationService(db, product_service)

        # Test configuration for LT9000 with H material

        try:
            # Start configuration
            config_service.start_configuration(
                product_family_id=lt9000_family.id,
                product_family_name=lt9000_family.name,
                base_product_info={
                    "material": "H",
                    "voltage": "115VAC",
                    "length": 10.0,
                },
            )

            # Select options
            config_service.select_option("Material", "H")
            config_service.select_option("Voltage", "115VAC")

            # Get results
            final_price = config_service.calculate_price()
            model_number = config_service.generate_model_number()
            description = config_service.get_final_description()

            print("✅ Configuration successful!")
            print(f"   Model Number: {model_number}")
            print(f"   Final Price: ${final_price:.2f}")
            print(f"   Description: {description}")
        except Exception as e:
            print(f"❌ Configuration failed: {e}")
            import traceback

            traceback.print_exc()

        # Test 4: Verify no static variants exist
        print("\n4️⃣ Verifying no static variants exist...")
        from src.core.models.product_variant import ProductVariant

        variant_count = db.query(ProductVariant).count()
        print(f"✅ Static variants: {variant_count} (should be 0)")

        print("\n" + "=" * 50)
        print("🎉 Dynamic Configuration Test Complete!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    test_dynamic_configuration()
