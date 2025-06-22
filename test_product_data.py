#!/usr/bin/env python3
"""
Test script to check product data and options.
"""

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.models import ProductFamily, BaseModel, Option

def test_product_data():
    """Test the product data and options."""
    db = SessionLocal()
    
    try:
        # Check product families
        families = db.query(ProductFamily).all()
        print(f"Product Families ({len(families)}):")
        for family in families:
            print(f"  - {family.name} (ID: {family.id})")
        
        print("\n" + "="*50)
        
        # Check base models
        base_models = db.query(BaseModel).all()
        print(f"Base Models ({len(base_models)}):")
        for model in base_models:
            print(f"  - {model.model_number} (Family: {model.product_family.name}, Price: ${model.base_price})")
        
        print("\n" + "="*50)
        
        # Check options
        options = db.query(Option).all()
        print(f"Options ({len(options)}):")
        for option in options:
            print(f"  - {option.name} (Category: {option.category}, Choices: {option.choices}, Adders: {option.adders})")
        
        print("\n" + "="*50)
        
        # Test product service
        ps = ProductService()
        
        # Test LS2000 options
        print("LS2000 Options:")
        ls2000_options = ps.get_additional_options(db, 'LS2000')
        for opt in ls2000_options:
            print(f"  - {opt['name']}: {opt['choices']} (adders: {opt['adders']})")
        
        print("\n" + "="*50)
        
        # Test materials for LS2000
        print("LS2000 Materials:")
        materials = ps.get_available_materials_for_product(db, 'LS2000')
        for mat in materials:
            print(f"  - {mat['name']}: {mat['choices']} (adders: {mat['adders']})")
        
        print("\n" + "="*50)
        
        # Test voltages for LS2000
        print("LS2000 Voltages:")
        voltages = ps.get_available_voltages(db, 'LS2000')
        for voltage in voltages:
            print(f"  - {voltage}")
            
    finally:
        db.close()

if __name__ == "__main__":
    test_product_data() 