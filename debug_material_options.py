#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService


def debug_material_options():
    db = SessionLocal()
    try:
        print("=== DEBUGGING MATERIAL OPTIONS ===\n")

        test_family = "LS2000"

        # Get the product family
        from src.core.models.product_variant import ProductFamily

        family = (
            db.query(ProductFamily).filter(ProductFamily.name == test_family).first()
        )

        # Get a base variant
        from src.core.models.product_variant import ProductVariant

        base_variant = (
            db.query(ProductVariant)
            .filter(
                ProductVariant.product_family_id == family.id,
                ProductVariant.material == "S",
            )
            .first()
        )

        # Initialize services
        product_service = ProductService()
        config_service = ConfigurationService(db, product_service)

        # Start configuration
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

        print(f"Configuration started for {test_family}")
        print(f"Base price: ${base_variant.base_price:.2f}")

        # Get all options
        all_options = product_service.get_additional_options(db, test_family)
        print(f"\nTotal options returned: {len(all_options)}")

        # Filter material options
        material_options = [
            opt for opt in all_options if opt.get("category") == "Material"
        ]
        print(f"Material options: {len(material_options)}")

        # Test each material option
        for i, opt in enumerate(material_options):
            print(f"\n--- Material Option {i+1} ---")
            print(f"Name: {opt.get('name')}")
            print(f"Category: {opt.get('category')}")
            print(f"Choices: {opt.get('choices')}")
            print(f"Adders: {opt.get('adders')}")

            # Get the material code from choices
            material_code = None
            if opt.get("choices") and isinstance(opt.get("choices"), list):
                for choice in opt.get("choices"):
                    if isinstance(choice, dict):
                        material_code = choice.get("code")
                        break

            if material_code:
                print(f"Material code: {material_code}")

                # Test selecting this material
                print(f"Testing selection of {material_code}...")
                config_service.select_option("Material", material_code)

                # Check what's in selected_options
                selected_material = config_service.current_config.selected_options.get(
                    "Material"
                )
                print(f"Selected material in config: {selected_material}")

                # Check final price
                final_price = config_service.current_config.final_price
                base_price = base_variant.base_price
                applied_adder = final_price - base_price

                print(f"Final price: ${final_price:.2f}")
                print(f"Applied adder: ${applied_adder:.2f}")

                # Check expected adder
                expected_adder = 0.0
                adders = opt.get("adders", {})
                if isinstance(adders, dict):
                    expected_adder = adders.get(material_code, 0.0)

                print(f"Expected adder: ${expected_adder:.2f}")

                if abs(applied_adder - expected_adder) < 0.01:
                    print(f"✅ CORRECT")
                else:
                    print(f"❌ INCORRECT")

        # Debug the _update_price method
        print(f"\n=== DEBUGGING _update_price METHOD ===")

        # Select H material
        config_service.select_option("Material", "H")

        print(f"Selected options: {config_service.current_config.selected_options}")

        # Manually call _update_price and see what happens
        config_service._update_price()

        print(
            f"Final price after _update_price: ${config_service.current_config.final_price:.2f}"
        )

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    debug_material_options()
