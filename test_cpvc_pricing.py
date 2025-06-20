#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService


def test_cpvc_pricing():
    db = SessionLocal()
    try:
        print("=== TESTING CPVC PRICING ===\n")

        test_family = "LS2000"  # Test with LS2000 which now has CPVC

        # Get the product family
        from src.core.models.product_variant import ProductFamily

        family = (
            db.query(ProductFamily).filter(ProductFamily.name == test_family).first()
        )
        if not family:
            print(f"❌ Product family {test_family} not found!")
            return

        print(f"Testing CPVC pricing for {test_family}")

        # Get a base variant for this family
        from src.core.models.product_variant import ProductVariant

        base_variant = (
            db.query(ProductVariant)
            .filter(
                ProductVariant.product_family_id == family.id,
                ProductVariant.material == "S",  # Use S as base
            )
            .first()
        )

        if not base_variant:
            print(f"❌ No base variant found for {test_family}")
            return

        print(f"Base variant: {base_variant.model_number}")
        print(f"Base price: ${base_variant.base_price:.2f}")

        # Initialize services
        product_service = ProductService()
        config_service = ConfigurationService(db, product_service)

        # Test CPVC material specifically
        print("\n=== TESTING CPVC MATERIAL ===")

        # Start a new configuration
        config_service.start_configuration(
            family.id,
            test_family,
            {
                "id": base_variant.id,
                "model_number": base_variant.model_number,
                "base_price": base_variant.base_price,
                "base_length": base_variant.base_length,
                "voltage": base_variant.voltage,
                "material": base_variant.material,
            },
        )

        # Select CPVC material
        config_service.select_option("Material", "CPVC")

        # Get the final price
        final_price = config_service.current_config.final_price
        base_price = base_variant.base_price

        # Calculate the adder that was applied
        applied_adder = final_price - base_price

        print(f"Base price: ${base_price:.2f}")
        print(f"Final price: ${final_price:.2f}")
        print(f"Applied adder: ${applied_adder:.2f}")
        print("Expected adder: $400.00")

        if abs(applied_adder - 400.0) < 0.01:
            print("✅ CORRECT: CPVC adder matches expected value")
        else:
            print("❌ INCORRECT: CPVC adder does not match expected value")
            print(f"   Difference: ${applied_adder - 400.0:.2f}")

        # Also test that CPVC is available in the ProductService output
        print("\n=== VERIFYING CPVC IN PRODUCT SERVICE ===")
        additional_options = product_service.get_additional_options(db, test_family)
        material_options = [
            opt for opt in additional_options if opt.get("category") == "Material"
        ]

        cpvc_found = False
        for opt in material_options:
            if opt.get("choices") and isinstance(opt.get("choices"), list):
                for choice in opt.get("choices"):
                    if isinstance(choice, dict) and choice.get("code") == "CPVC":
                        cpvc_found = True
                        adders = opt.get("adders", {})
                        cpvc_adder = adders.get("CPVC", 0)
                        print("✅ CPVC found in ProductService output")
                        print(f"   Choices: {opt.get('choices')}")
                        print(f"   Adders: {adders}")
                        print(f"   CPVC adder: ${cpvc_adder:.2f}")
                        break
                if cpvc_found:
                    break

        if not cpvc_found:
            print("❌ CPVC not found in ProductService output")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_cpvc_pricing()
