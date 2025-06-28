#!/usr/bin/env python3
"""
Debug voltage options for LS7000/2 and LS8000/2
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.models.product_variant import ProductFamily
from src.core.models.option import Option, ProductFamilyOption

def debug_voltage_issue():
    """Debug voltage options for LS7000/2 and LS8000/2"""
    print("=== DEBUGGING VOLTAGE ISSUE FOR LS7000/2 AND LS8000/2 ===\n")
    
    db = SessionLocal()
    
    try:
        # Get the family IDs
        ls7000_2 = db.query(ProductFamily).filter_by(name="LS7000/2").first()
        ls8000_2 = db.query(ProductFamily).filter_by(name="LS8000/2").first()
        
        print(f"LS7000/2 family ID: {ls7000_2.id if ls7000_2 else 'NOT FOUND'}")
        print(f"LS8000/2 family ID: {ls8000_2.id if ls8000_2 else 'NOT FOUND'}")
        
        # Check the specific voltage options that are associated
        print("\n1. Checking specific voltage options (17 and 19):")
        option_17 = db.query(Option).filter_by(id=17).first()
        option_19 = db.query(Option).filter_by(id=19).first()
        
        if option_17:
            print(f"  Option 17: {option_17.name}")
            print(f"    category: '{option_17.category}'")
            print(f"    product_families: '{option_17.product_families}'")
            print(f"    choices: {option_17.choices}")
        else:
            print("  Option 17: NOT FOUND")
            
        if option_19:
            print(f"  Option 19: {option_19.name}")
            print(f"    category: '{option_19.category}'")
            print(f"    product_families: '{option_19.product_families}'")
            print(f"    choices: {option_19.choices}")
        else:
            print("  Option 19: NOT FOUND")
        
        # Check all voltage options
        print("\n2. All voltage options in database:")
        voltage_options = db.query(Option).filter(Option.category == "Voltage").all()
        print(f"Found {len(voltage_options)} voltage options")
        for opt in voltage_options:
            print(f"  - ID {opt.id}: {opt.name}")
            print(f"    product_families: '{opt.product_families}' (type: {type(opt.product_families)})")
            print(f"    choices: {opt.choices}")
        
        # Check all options to see what categories exist
        print("\n3. All option categories in database:")
        all_options = db.query(Option).all()
        categories = set()
        for opt in all_options:
            if opt.category:
                categories.add(opt.category)
        print(f"Categories found: {sorted(categories)}")
        
        # Check family associations for voltage options
        print("\n4. Family associations for voltage options:")
        for opt in voltage_options:
            associations = db.query(ProductFamilyOption).filter_by(option_id=opt.id).all()
            print(f"  - Option {opt.id} ({opt.name}):")
            for assoc in associations:
                family = db.query(ProductFamily).filter_by(id=assoc.product_family_id).first()
                print(f"    * Family {assoc.product_family_id} ({family.name if family else 'UNKNOWN'}): is_available={assoc.is_available}")
        
        # Check specific associations for LS7000/2 and LS8000/2
        print("\n5. Specific associations for LS7000/2 and LS8000/2:")
        if ls7000_2:
            ls7000_2_assocs = db.query(ProductFamilyOption).filter_by(product_family_id=ls7000_2.id).all()
            print(f"  LS7000/2 associations:")
            for assoc in ls7000_2_assocs:
                option = db.query(Option).filter_by(id=assoc.option_id).first()
                print(f"    * Option {assoc.option_id} ({option.name if option else 'UNKNOWN'}): is_available={assoc.is_available}")
        
        if ls8000_2:
            ls8000_2_assocs = db.query(ProductFamilyOption).filter_by(product_family_id=ls8000_2.id).all()
            print(f"  LS8000/2 associations:")
            for assoc in ls8000_2_assocs:
                option = db.query(Option).filter_by(id=assoc.option_id).first()
                print(f"    * Option {assoc.option_id} ({option.name if option else 'UNKNOWN'}): is_available={assoc.is_available}")
        
        # Test the current get_available_voltages method
        print("\n6. Testing get_available_voltages method:")
        product_service = ProductService(db)
        
        for model_name in ["LS7000/2", "LS8000/2"]:
            print(f"\n  Testing {model_name}:")
            try:
                voltages = product_service.get_available_voltages(db, model_name)
                print(f"    Result: {voltages}")
            except Exception as e:
                print(f"    Error: {e}")
                import traceback
                traceback.print_exc()
        
        # Test manual query to see what's happening
        print("\n7. Manual query test:")
        for model_name in ["LS7000/2", "LS8000/2"]:
            print(f"\n  Manual query for {model_name}:")
            # Try different approaches
            options1 = db.query(Option).filter(Option.category == "Voltage").filter(Option.product_families.contains(model_name)).all()
            print(f"    Using contains('{model_name}'): {len(options1)} options found")
            for opt in options1:
                print(f"      - {opt.name}: product_families='{opt.product_families}'")
            
            # Try with family ID
            if model_name == "LS7000/2" and ls7000_2:
                options2 = db.query(Option).join(ProductFamilyOption).filter(ProductFamilyOption.product_family_id == ls7000_2.id).filter(Option.category == "Voltage").all()
                print(f"    Using family ID {ls7000_2.id}: {len(options2)} options found")
                for opt in options2:
                    print(f"      - {opt.name}")
        
    except Exception as e:
        print(f"Error in debug: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
    
    print("\n=== VOLTAGE DEBUG COMPLETE ===")

if __name__ == "__main__":
    debug_voltage_issue() 