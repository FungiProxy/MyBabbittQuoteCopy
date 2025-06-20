#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService


def test_ls8000_pricing():
    db = SessionLocal()
    try:
        print("=== TESTING LS8000 PRICING ===\n")

        test_family = "LS8000"

        # Get the product family
        from src.core.models.product_variant import ProductFamily

        family = (
            db.query(ProductFamily).filter(ProductFamily.name == test_family).first()
        )
        if not family:
            print(f"❌ Product family {test_family} not found!")
            return

        print(f"Testing pricing for {test_family}")
        print(f"Family ID: {family.id}")

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

        # Get all material options for this family
        material_options = product_service.get_additional_options(db, test_family)
        material_options = [
            opt for opt in material_options if opt.get("category") == "Material"
        ]

        print(f"\nFound {len(material_options)} material options:")
        for opt in material_options:
            print(
                f"  - {opt.get('name')}: choices={opt.get('choices')}, adders={opt.get('adders')}"
            )

        # Test pricing for each material
        print("\n=== TESTING PRICING FOR EACH MATERIAL ===")

        # Get all material codes
        all_materials = []
        for opt in material_options:
            if opt.get("choices") and isinstance(opt.get("choices"), list):
                for choice in opt.get("choices"):
                    if isinstance(choice, dict):
                        all_materials.append(choice.get("code"))

        all_materials = list(set(all_materials))  # Remove duplicates
        print(f"Testing materials: {sorted(all_materials)}")

        for material_code in sorted(all_materials):
            print(f"\n--- Testing Material: {material_code} ---")

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

            # Select the material
            config_service.select_option("Material", material_code)

            # Get the final price
            final_price = config_service.current_config.final_price
            base_price = base_variant.base_price

            # Calculate the adder that was applied
            applied_adder = final_price - base_price

            print(f"  Base price: ${base_price:.2f}")
            print(f"  Final price: ${final_price:.2f}")
            print(f"  Applied adder: ${applied_adder:.2f}")

            # Check if this matches the expected adder from the options
            expected_adder = 0.0
            for opt in material_options:
                if opt.get("choices") and isinstance(opt.get("choices"), list):
                    for choice in opt.get("choices"):
                        if (
                            isinstance(choice, dict)
                            and choice.get("code") == material_code
                        ):
                            adders = opt.get("adders", {})
                            if isinstance(adders, dict):
                                expected_adder = adders.get(material_code, 0.0)
                                break
                    if expected_adder != 0.0:
                        break

            print(f"  Expected adder: ${expected_adder:.2f}")

            if abs(applied_adder - expected_adder) < 0.01:
                print("  ✅ CORRECT: Adder matches expected value")
            else:
                print("  ❌ INCORRECT: Adder does not match expected value")
                print(f"     Difference: ${applied_adder - expected_adder:.2f}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_ls8000_pricing()
