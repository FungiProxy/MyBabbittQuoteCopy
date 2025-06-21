#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option, ProductFamilyOption
from src.core.models.product_variant import ProductFamily


def print_voltage_assignments(db, family, label):
    assignments = (
        db.query(ProductFamilyOption)
        .filter(ProductFamilyOption.product_family_id == family.id)
        .join(Option)
        .filter(Option.category == "Voltage")
        .all()
    )
    print(
        f"{label} voltages:",
        [
            a.option.choices[0] if a.option.choices else a.option.name
            for a in assignments
        ],
    )


def check_and_fix_voltage_assignments():
    """Check and fix voltage assignments for FS10000 and LS8500"""
    db = SessionLocal()
    try:
        # Get the product families
        fs10000 = (
            db.query(ProductFamily).filter(ProductFamily.name == "FS10000").first()
        )
        ls8500 = db.query(ProductFamily).filter(ProductFamily.name == "LS8500").first()
        if not fs10000 or not ls8500:
            print("Error: Could not find FS10000 or LS8500 product families")
            return
        print(f"FS10000 ID: {fs10000.id}")
        print(f"LS8500 ID: {ls8500.id}")

        # Print current assignments
        print("\nCurrent voltage assignments BEFORE:")
        print_voltage_assignments(db, fs10000, "FS10000")
        print_voltage_assignments(db, ls8500, "LS8500")

        # Explicitly delete all voltage assignments for both families
        for family in [fs10000, ls8500]:
            assignments = (
                db.query(ProductFamilyOption)
                .filter(ProductFamilyOption.product_family_id == family.id)
                .join(Option)
                .filter(Option.category == "Voltage")
                .all()
            )
            for a in assignments:
                db.delete(a)
        db.commit()
        print("\nRemoved all voltage assignments for both families.")

        # Add correct assignments
        fs10000_voltage_codes = ["115VAC", "230VAC"]
        ls8500_voltage_codes = ["115VAC", "24VDC", "12VDC", "220VAC"]
        for voltage_code in fs10000_voltage_codes:
            voltage_option = (
                db.query(Option)
                .filter(
                    Option.category == "Voltage",
                    Option.choices.contains([voltage_code]),
                )
                .first()
            )
            if voltage_option:
                db.add(
                    ProductFamilyOption(
                        product_family_id=fs10000.id,
                        option_id=voltage_option.id,
                        is_available=1,
                    )
                )
                print(f"  Added {voltage_code} to FS10000")
            else:
                print(f"  Warning: Could not find voltage option for {voltage_code}")
        for voltage_code in ls8500_voltage_codes:
            voltage_option = (
                db.query(Option)
                .filter(
                    Option.category == "Voltage",
                    Option.choices.contains([voltage_code]),
                )
                .first()
            )
            if voltage_option:
                db.add(
                    ProductFamilyOption(
                        product_family_id=ls8500.id,
                        option_id=voltage_option.id,
                        is_available=1,
                    )
                )
                print(f"  Added {voltage_code} to LS8500")
            else:
                print(f"  Warning: Could not find voltage option for {voltage_code}")
        db.commit()
        print("\nVoltage assignments updated successfully!")

        # Print new assignments
        print("\nCurrent voltage assignments AFTER:")
        print_voltage_assignments(db, fs10000, "FS10000")
        print_voltage_assignments(db, ls8500, "LS8500")

        # Verify via ProductService
        from src.core.services.product_service import ProductService

        ps = ProductService()
        fs10000_options = ps.get_additional_options(db, "FS10000")
        fs10000_voltages = [
            opt for opt in fs10000_options if opt.get("category") == "Voltage"
        ]
        print(
            f"FS10000 voltages via ProductService: {[opt.get('choices', []) for opt in fs10000_voltages]}"
        )
        ls8500_options = ps.get_additional_options(db, "LS8500")
        ls8500_voltages = [
            opt for opt in ls8500_options if opt.get("category") == "Voltage"
        ]
        print(
            f"LS8500 voltages via ProductService: {[opt.get('choices', []) for opt in ls8500_voltages]}"
        )
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    check_and_fix_voltage_assignments()
