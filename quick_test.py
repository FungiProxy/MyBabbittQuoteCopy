#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

def quick_test():
    db = SessionLocal()
    try:
        product_service = ProductService(db=db)
        config_service = ConfigurationService(db, product_service)
        
        print("=== QUICK TEST ===")
        
        # Start configuration
        config_service.start_configuration(
            product_family_id=1,
            product_family_name="LS2000",
            base_product_info={
                "name": "LS2000",
                "id": 1,
                "base_price": 425.0,
                "model_number": "LS2000-115VAC-S-10",
                "base_length": 10,
                "voltage": "115VAC",
                "material": "S"
            }
        )
        
        print(f"Base: {config_service.generate_model_number()}")
        
        # Test each code
        config_service.set_option("Extra Static Protection", "Yes")
        print(f"With xsp: {config_service.generate_model_number()}")
        
        config_service.set_option("Bent Probe", "Yes")
        config_service.set_option("Bent Probe Degree", 45)
        print(f"With 45DEG: {config_service.generate_model_number()}")
        
        config_service.set_option('3/4" Diameter Probe', "Yes")
        print(f"With 3/4OD: {config_service.generate_model_number()}")
        
        config_service.set_option("Insulator Material", "Teflon Upgrade")
        print(f"With TEFINS: {config_service.generate_model_number()}")
        
        config_service.set_option("Connection Type", "Tri-clamp")
        config_service.set_option("Tri-clamp", "1-1/2\" Spud")
        print(f"With TC1-1/2\"SPD: {config_service.generate_model_number()}")
        
        print("=== TEST COMPLETE ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    quick_test() 