#!/usr/bin/env python3
"""
Technical Specifications Compilation
Shows all available technical data for each product family for review.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel

def compile_technical_specs():
    """Compile all technical specifications for review."""
    
    db = SessionLocal()
    try:
        print("=== TECHNICAL SPECIFICATIONS COMPILATION ===\n")
        print("This shows ALL technical data available in the database for each product family.\n")
        print("Please review and verify the accuracy of this data before updating the export system.\n")
        
        # Get all base models with their technical specs
        base_models = db.query(BaseModel).all()
        
        for model in base_models:
            print(f"=== {model.model_number} ===")
            print(f"Product Family: {model.product_family.name if model.product_family else 'Unknown'}")
            print(f"Description: {model.description}")
            print(f"Base Price: ${model.base_price}")
            print(f"Base Length: {model.base_length}\"")
            print(f"Default Voltage: {model.voltage}")
            print(f"Default Material: {model.material}")
            print()
            
            print("TECHNICAL SPECIFICATIONS:")
            print(f"  • Output Type: {getattr(model, 'output_type', None) or 'NOT SET'}")
            print(f"  • Insulator Material: {getattr(model, 'insulator_material', None) or 'NOT SET'}")
            print(f"  • Insulator Length: {getattr(model, 'insulator_length', None) or 'NOT SET'}")
            print(f"  • Insulator Temp Rating: {getattr(model, 'insulator_temp_rating', None) or 'NOT SET'}")
            print(f"  • Process Connection Type: {getattr(model, 'process_connection_type', None) or 'NOT SET'}")
            print(f"  • Process Connection Size: {getattr(model, 'process_connection_size', None) or 'NOT SET'}")
            print(f"  • Max Pressure: {getattr(model, 'max_pressure', None) or 'NOT SET'}")
            print(f"  • Housing Type: {getattr(model, 'housing_type', None) or 'NOT SET'}")
            print(f"  • Housing Ratings: {getattr(model, 'housing_ratings', None) or 'NOT SET'}")
            print(f"  • Application Notes: {getattr(model, 'application_notes', None) or 'NOT SET'}")
            print(f"  • Special Notes: {getattr(model, 'special_notes', None) or 'NOT SET'}")
            print()
            print("-" * 80)
            print()
        
        # Summary
        print("=== SUMMARY ===")
        print(f"Total Base Models: {len(base_models)}")
        
        # Count models with technical specs
        with_insulator = sum(1 for m in base_models if getattr(m, 'insulator_material', None))
        with_connection = sum(1 for m in base_models if getattr(m, 'process_connection_type', None))
        with_housing = sum(1 for m in base_models if getattr(m, 'housing_type', None))
        with_pressure = sum(1 for m in base_models if getattr(m, 'max_pressure', None))
        
        print(f"Models with Insulator Data: {with_insulator}/{len(base_models)}")
        print(f"Models with Connection Data: {with_connection}/{len(base_models)}")
        print(f"Models with Housing Data: {with_housing}/{len(base_models)}")
        print(f"Models with Pressure Data: {with_pressure}/{len(base_models)}")
        
        print("\n=== NEXT STEPS ===")
        print("1. Review all technical specifications above")
        print("2. Verify accuracy of insulator materials, temperatures, pressure ratings")
        print("3. Confirm housing types and ratings are correct")
        print("4. Check that application notes and special notes are accurate")
        print("5. Once verified, we can update the export system to use this data")
        
    except Exception as e:
        print(f"Error during compilation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    compile_technical_specs()
