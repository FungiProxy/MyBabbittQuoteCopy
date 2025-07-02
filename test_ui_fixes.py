#!/usr/bin/env python3
"""
Test script to verify UI fixes for:
1. Model number display formatting
2. Spare parts functionality
3. TRAN-EX configuration
"""

import sys
import os
sys.path.append('.')

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService
from src.core.services.spare_part_service import SparePartService
from src.core.config.base_models import get_base_model

def test_model_number_generation():
    """Test model number generation for different products."""
    print("=== Testing Model Number Generation ===")
    
    db = SessionLocal()
    product_service = ProductService(db)
    config_service = ConfigurationService(db, product_service)
    
    test_products = ["LS2000", "FS10000", "TRAN-EX"]
    
    for product_name in test_products:
        try:
            # Get base product info
            base_product = product_service.get_base_product_for_family(db, product_name)
            if not base_product:
                print(f"❌ No base product found for {product_name}")
                continue
                
            # Start configuration
            config_service.start_configuration(
                product_family_id=base_product.get('id', 1),
                product_family_name=product_name,
                base_product_info=base_product
            )
            
            # Generate model number
            model_number = config_service.generate_model_number()
            print(f"✅ {product_name}: {model_number}")
            
        except Exception as e:
            print(f"❌ Error with {product_name}: {e}")
    
    db.close()

def test_spare_parts():
    """Test spare parts functionality."""
    print("\n=== Testing Spare Parts ===")
    
    db = SessionLocal()
    
    try:
        # Get all spare parts
        all_parts = SparePartService.get_all_spare_parts(db)
        print(f"✅ Found {len(all_parts)} spare parts")
        
        # Test getting parts by family
        ls2000_parts = SparePartService.get_spare_parts_by_family(db, "LS2000")
        print(f"✅ Found {len(ls2000_parts)} LS2000 spare parts")
        
        # Test getting parts by category
        categories = SparePartService.get_spare_part_categories(db)
        print(f"✅ Found categories: {categories}")
        
        # Show first few parts
        print("First 3 spare parts:")
        for i, part in enumerate(all_parts[:3]):
            print(f"  {i+1}. {part.part_number} - {part.name} (${part.price:.2f})")
            
    except Exception as e:
        print(f"❌ Error testing spare parts: {e}")
    
    db.close()

def test_tran_ex_config():
    """Test TRAN-EX configuration."""
    print("\n=== Testing TRAN-EX Configuration ===")
    
    try:
        # Check base model
        base_model = get_base_model("TRAN-EX")
        if base_model:
            print(f"✅ TRAN-EX base model found: {base_model['model_number']}")
            print(f"   Base price: ${base_model['base_price']}")
            print(f"   Material: {base_model['material']}")
            print(f"   Voltage: {base_model['voltage']}")
        else:
            print("❌ TRAN-EX base model not found")
            
    except Exception as e:
        print(f"❌ Error testing TRAN-EX: {e}")

def test_product_options():
    """Test product options loading."""
    print("\n=== Testing Product Options ===")
    
    db = SessionLocal()
    product_service = ProductService(db)
    
    test_products = ["LS2000", "FS10000", "TRAN-EX"]
    
    for product_name in test_products:
        try:
            options = product_service.get_additional_options(db, product_name)
            print(f"✅ {product_name}: {len(options)} options")
            
            # Show option categories
            categories = set(opt.get('category', 'Unknown') for opt in options)
            print(f"   Categories: {list(categories)}")
            
        except Exception as e:
            print(f"❌ Error with {product_name} options: {e}")
    
    db.close()

if __name__ == "__main__":
    print("Testing UI Fixes...\n")
    
    test_model_number_generation()
    test_spare_parts()
    test_tran_ex_config()
    test_product_options()
    
    print("\n✅ All tests completed!") 