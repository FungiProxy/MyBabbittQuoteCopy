#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService


def verify_cpvc_fix():
    db = SessionLocal()
    try:
        print("=== VERIFYING CPVC FIX ===\n")

        # Test families that should have CPVC
        families_with_cpvc = ["LS6000", "LS7000"]

        # Test families that should NOT have CPVC
        families_without_cpvc = ["LS2000", "LS2100", "LS8000"]

        product_service = ProductService()

        print("=== FAMILIES THAT SHOULD HAVE CPVC ===")
        for family_name in families_with_cpvc:
            print(f"\n--- {family_name} ---")

            # Check ProductService output
            additional_options = product_service.get_additional_options(db, family_name)
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
                            print(f"  ✅ CPVC available (adder: ${cpvc_adder:.2f})")
                            break
                    if cpvc_found:
                        break

            if not cpvc_found:
                print("  ❌ CPVC not found!")

            # Test pricing if CPVC is available
            if cpvc_found:
                # Get base variant
                from src.core.models.product_variant import (
                    ProductFamily,
                    ProductVariant,
                )

                family = (
                    db.query(ProductFamily)
                    .filter(ProductFamily.name == family_name)
                    .first()
                )
                base_variant = (
                    db.query(ProductVariant)
                    .filter(
                        ProductVariant.product_family_id == family.id,
                        ProductVariant.material == "S",
                    )
                    .first()
                )

                if base_variant:
                    # Test CPVC pricing
                    config_service = ConfigurationService(db, product_service)
                    config_service.start_configuration(
                        family.id,
                        family_name,
                        {
                            "id": base_variant.id,
                            "model_number": base_variant.model_number,
                            "base_price": base_variant.base_price,
                            "base_length": base_variant.base_length,
                            "voltage": base_variant.voltage,
                            "material": base_variant.material,
                        },
                    )

                    config_service.select_option("Material", "CPVC")
                    final_price = config_service.current_config.final_price
                    base_price = base_variant.base_price
                    applied_adder = final_price - base_price

                    print(f"  Base price: ${base_price:.2f}")
                    print(f"  Final price: ${final_price:.2f}")
                    print(f"  Applied adder: ${applied_adder:.2f}")

                    if abs(applied_adder - 400.0) < 0.01:
                        print("  ✅ CPVC pricing correct")
                    else:
                        print("  ❌ CPVC pricing incorrect (expected $400.00)")

        print("\n=== FAMILIES THAT SHOULD NOT HAVE CPVC ===")
        for family_name in families_without_cpvc:
            print(f"\n--- {family_name} ---")

            # Check ProductService output
            additional_options = product_service.get_additional_options(db, family_name)
            material_options = [
                opt for opt in additional_options if opt.get("category") == "Material"
            ]

            cpvc_found = False
            for opt in material_options:
                if opt.get("choices") and isinstance(opt.get("choices"), list):
                    for choice in opt.get("choices"):
                        if isinstance(choice, dict) and choice.get("code") == "CPVC":
                            cpvc_found = True
                            break
                    if cpvc_found:
                        break

            if cpvc_found:
                print("  ❌ CPVC incorrectly available!")
            else:
                print("  ✅ CPVC correctly not available")

        print("\n=== SUMMARY ===")
        print("CPVC should only be available for LS6000 and LS7000 with $400 adder")
        print("All other families should not have CPVC available")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    verify_cpvc_fix()
