#!/usr/bin/env python3
"""
Technical Data Gap Analysis
Comprehensive analysis of all technical specifications data to identify gaps and inconsistencies.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel
from src.core.models.product_variant import ProductFamily
from src.core.models.option import Option

def analyze_technical_data_gaps():
    """Analyze all technical specifications data for gaps and inconsistencies."""
    
    db = SessionLocal()
    try:
        print("=== TECHNICAL DATA GAP ANALYSIS ===\n")
        
        # Get all base models
        base_models = db.query(BaseModel).all()
        product_families = db.query(ProductFamily).all()
        
        print(f"Total Base Models: {len(base_models)}")
        print(f"Total Product Families: {len(product_families)}")
        print()
        
        # 1. Analyze missing technical specifications
        print("=== MISSING TECHNICAL SPECIFICATIONS ===")
        missing_data = {
            'insulator_material': [],
            'insulator_length': [],
            'insulator_temp_rating': [],
            'process_connection_type': [],
            'process_connection_size': [],
            'max_pressure': [],
            'housing_type': [],
            'housing_ratings': [],
            'application_notes': [],
            'special_notes': []
        }
        
        for model in base_models:
            for field in missing_data.keys():
                if not getattr(model, field, None):
                    missing_data[field].append(model.model_number)
        
        for field, models in missing_data.items():
            if models:
                print(f"Missing {field}: {len(models)} models")
                for model_num in models:
                    print(f"  • {model_num}")
                print()
        
        # 2. Analyze data inconsistencies
        print("=== DATA INCONSISTENCIES ===")
        
        # Check for inconsistent insulator materials within families
        print("Insulator Material Inconsistencies:")
        family_insulators = {}
        for model in base_models:
            family = model.product_family.name if model.product_family else 'Unknown'
            insulator = getattr(model, 'insulator_material', None)
            if insulator:
                if family not in family_insulators:
                    family_insulators[family] = set()
                family_insulators[family].add(insulator)
        
        for family, insulators in family_insulators.items():
            if len(insulators) > 1:
                print(f"  • {family}: {', '.join(insulators)}")
        print()
        
        # Check for inconsistent pressure ratings
        print("Pressure Rating Inconsistencies:")
        family_pressures = {}
        for model in base_models:
            family = model.product_family.name if model.product_family else 'Unknown'
            pressure = getattr(model, 'max_pressure', None)
            if pressure:
                if family not in family_pressures:
                    family_pressures[family] = set()
                family_pressures[family].add(str(pressure))
        
        for family, pressures in family_pressures.items():
            if len(pressures) > 1:
                print(f"  • {family}: {', '.join(pressures)}")
        print()
        
        # 3. Analyze data quality issues
        print("=== DATA QUALITY ISSUES ===")
        
        # Check for malformed special notes
        malformed_notes = []
        for model in base_models:
            special_notes = getattr(model, 'special_notes', None)
            if special_notes and ('};' in special_notes or '\\' in special_notes):
                malformed_notes.append(model.model_number)
        
        if malformed_notes:
            print("Models with malformed special notes:")
            for model_num in malformed_notes:
                print(f"  • {model_num}")
            print()
        
        # Check for incomplete application notes
        incomplete_app_notes = []
        for model in base_models:
            app_notes = getattr(model, 'application_notes', None)
            if app_notes and len(app_notes.strip()) < 50:  # Very short notes might be incomplete
                incomplete_app_notes.append(model.model_number)
        
        if incomplete_app_notes:
            print("Models with potentially incomplete application notes:")
            for model_num in incomplete_app_notes:
                print(f"  • {model_num}")
            print()
        
        # 4. Cross-reference with RTF data
        print("=== RTF DATA CROSS-REFERENCE ===")
        
        # Check if we have RTF data for all families
        rtf_families = set()
        try:
            import json
            with open('extracted_rtf_data.json', 'r') as f:
                rtf_data = json.load(f)
                for item in rtf_data:
                    rtf_families.add(item.get('product_family', ''))
        except FileNotFoundError:
            print("RTF data file not found")
        except Exception as e:
            print(f"Error reading RTF data: {e}")
        
        db_families = {pf.name for pf in product_families}
        
        missing_rtf = db_families - rtf_families
        extra_rtf = rtf_families - db_families
        
        if missing_rtf:
            print("Product families missing RTF data:")
            for family in missing_rtf:
                print(f"  • {family}")
            print()
        
        if extra_rtf:
            print("RTF data for non-existent product families:")
            for family in extra_rtf:
                print(f"  • {family}")
            print()
        
        # 5. Summary and recommendations
        print("=== SUMMARY AND RECOMMENDATIONS ===")
        
        total_fields = len(base_models) * 10  # 10 technical spec fields per model
        filled_fields = sum(
            sum(1 for field in missing_data.keys() if getattr(model, field, None))
            for model in base_models
        )
        
        completion_rate = (filled_fields / total_fields) * 100
        print(f"Overall data completion rate: {completion_rate:.1f}%")
        print()
        
        print("Priority Actions:")
        print("1. Fill missing pressure ratings (most critical for safety)")
        print("2. Standardize insulator materials within product families")
        print("3. Clean up malformed special notes")
        print("4. Add missing application notes for key products")
        print("5. Verify housing type consistency")
        print("6. Cross-reference with RTF templates for accuracy")
        
        # 6. Detailed model-by-model analysis
        print("\n=== DETAILED MODEL ANALYSIS ===")
        for model in base_models:
            print(f"\n{model.model_number}:")
            missing = []
            for field in missing_data.keys():
                if not getattr(model, field, None):
                    missing.append(field)
            
            if missing:
                print(f"  Missing: {', '.join(missing)}")
            else:
                print("  Complete ✓")
            
            # Show key specifications
            insulator = getattr(model, 'insulator_material', None)
            pressure = getattr(model, 'max_pressure', None)
            housing = getattr(model, 'housing_type', None)
            
            if insulator:
                print(f"  Insulator: {insulator}")
            if pressure:
                print(f"  Max Pressure: {pressure}")
            if housing:
                print(f"  Housing: {housing}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    analyze_technical_data_gaps() 