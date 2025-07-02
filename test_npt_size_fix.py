#!/usr/bin/env python3
"""
Test script to verify that NPT Size options are correctly filtered by product family.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.services.product_service import ProductService

def test_npt_size_filtering():
    """Test that NPT Size options are correctly filtered by product family."""
    print("=== Testing NPT Size Filtering ===")
    
    db = SessionLocal()
    product_service = ProductService(db)
    
    # Test LS2000 - should only have 3/4" NPT
    print("\n--- Testing LS2000 ---")
    ls2000_options = product_service.get_additional_options(db, "LS2000")
    
    npt_size_options = [opt for opt in ls2000_options if opt['name'] == 'NPT Size']
    print(f"Found {len(npt_size_options)} NPT Size options for LS2000")
    
    for opt in npt_size_options:
        print(f"  Option ID: {opt['id']}")
        print(f"  Choices: {opt['choices']}")
        print(f"  Product Families: {opt.get('product_families', 'N/A')}")
    
    # Verify LS2000 only has 3/4" option
    if npt_size_options:
        choices = npt_size_options[0]['choices']
        if choices == ['3/4"']:
            print("✓ LS2000 correctly shows only 3/4\" NPT option")
        else:
            print(f"✗ LS2000 shows incorrect choices: {choices}")
    else:
        print("✗ No NPT Size options found for LS2000")
    
    # Test LS6000 - should have both 1" and 3/4" NPT
    print("\n--- Testing LS6000 ---")
    ls6000_options = product_service.get_additional_options(db, "LS6000")
    
    npt_size_options = [opt for opt in ls6000_options if opt['name'] == 'NPT Size']
    print(f"Found {len(npt_size_options)} NPT Size options for LS6000")
    
    for opt in npt_size_options:
        print(f"  Option ID: {opt['id']}")
        print(f"  Choices: {opt['choices']}")
        print(f"  Product Families: {opt.get('product_families', 'N/A')}")
    
    # Verify LS6000 has both 1" and 3/4" options
    if npt_size_options:
        choices = npt_size_options[0]['choices']
        if '1"' in choices and '3/4"' in choices:
            print("✓ LS6000 correctly shows both 1\" and 3/4\" NPT options")
        else:
            print(f"✗ LS6000 shows incorrect choices: {choices}")
    else:
        print("✗ No NPT Size options found for LS6000")
    
    # Test LS8000 - should have both 3/4" and 1" NPT (in that order)
    print("\n--- Testing LS8000 ---")
    ls8000_options = product_service.get_additional_options(db, "LS8000")
    
    npt_size_options = [opt for opt in ls8000_options if opt['name'] == 'NPT Size']
    print(f"Found {len(npt_size_options)} NPT Size options for LS8000")
    
    for opt in npt_size_options:
        print(f"  Option ID: {opt['id']}")
        print(f"  Choices: {opt['choices']}")
        print(f"  Product Families: {opt.get('product_families', 'N/A')}")
    
    # Verify LS8000 has both 3/4" and 1" options (in that order)
    if npt_size_options:
        choices = npt_size_options[0]['choices']
        if choices == ['3/4"', '1"']:
            print("✓ LS8000 correctly shows 3/4\" and 1\" NPT options in correct order")
        else:
            print(f"✗ LS8000 shows incorrect choices: {choices}")
    else:
        print("✗ No NPT Size options found for LS8000")
    
    db.close()

def test_material_filtering():
    """Test that Material options are correctly filtered by product family."""
    print("\n=== Testing Material Filtering ===")
    
    db = SessionLocal()
    product_service = ProductService(db)
    
    # Test LS2000 materials
    print("\n--- Testing LS2000 Materials ---")
    ls2000_materials = ProductService.get_available_materials(db, "LS2000")
    
    print(f"Found {len(ls2000_materials)} material options for LS2000")
    for material in ls2000_materials:
        print(f"  Material: {material['name']}")
        print(f"  Choices: {material['choices']}")
    
    # Test LS6000 materials
    print("\n--- Testing LS6000 Materials ---")
    ls6000_materials = ProductService.get_available_materials(db, "LS6000")
    
    print(f"Found {len(ls6000_materials)} material options for LS6000")
    for material in ls6000_materials:
        print(f"  Material: {material['name']}")
        print(f"  Choices: {material['choices']}")
    
    db.close()

if __name__ == "__main__":
    test_npt_size_filtering()
    test_material_filtering()
    print("\n=== Test Complete ===") 