#!/usr/bin/env python3
"""
Test script to check the current state of configuration logic and pricing.
"""

import sys
import logging
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.services.configuration_service import ConfigurationService

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_product_service():
    """Test the product service functionality."""
    print("=== Testing Product Service ===")
    
    db = SessionLocal()
    product_service = ProductService()
    
    try:
        # Test 1: Get product families
        print("\n1. Testing get_product_families_by_category...")
        families = product_service.get_product_families_by_category(db)
        print(f"Found {len(families)} categories")
        for category in families[:3]:  # Show first 3 categories
            print(f"  Category: {category['name']}")
            print(f"    Families: {len(category['families'])}")
            for family in category['families'][:2]:  # Show first 2 families per category
                print(f"      - {family['name']}: {family['description'][:50]}...")
        
        # Test 2: Get products for a specific family
        print("\n2. Testing get_products_by_family...")
        if families and families[0]['families']:
            test_family = families[0]['families'][0]['name']
            print(f"Testing with family: {test_family}")
            products = product_service.get_products_by_family(db, test_family)
            print(f"Found {len(products)} products")
            for product in products[:3]:  # Show first 3 products
                print(f"  - {product['name']}: ${product['base_price']:,.2f}")
        
        # Test 3: Get additional options
        print("\n3. Testing get_additional_options...")
        if families and families[0]['families']:
            test_family = families[0]['families'][0]['name']
            print(f"Testing with family: {test_family}")
            options = product_service.get_additional_options(db, test_family)
            print(f"Found {len(options)} options")
            for option in options[:5]:  # Show first 5 options
                print(f"  - {option.get('name')}: {option.get('category')}")
                print(f"    Choices: {option.get('choices', [])[:3]}...")  # Show first 3 choices
                print(f"    Adders: {list(option.get('adders', {}).keys())[:3]}...")  # Show first 3 adders
        
    except Exception as e:
        print(f"Error in product service test: {e}")
        logger.exception("Product service test failed")
    finally:
        db.close()

def test_configuration_service():
    """Test the configuration service functionality."""
    print("\n=== Testing Configuration Service ===")
    
    db = SessionLocal()
    product_service = ProductService()
    config_service = ConfigurationService(db, product_service)
    
    try:
        # Test 1: Start configuration
        print("\n1. Testing start_configuration...")
        families = product_service.get_product_families_by_category(db)
        if families and families[0]['families']:
            test_family = families[0]['families'][0]
            test_product = product_service.get_products_by_family(db, test_family['name'])[0]
            
            print(f"Testing with product: {test_product['name']}")
            config_service.start_configuration(
                product_family_id=test_family['id'],
                product_family_name=test_family['name'],
                base_product_info=test_product
            )
            print("Configuration started successfully")
            
            # Test 2: Set options
            print("\n2. Testing set_option...")
            config_service.set_option("Material", "S")
            config_service.set_option("Voltage", "24V")
            print("Options set successfully")
            
            # Test 3: Get current configuration
            print("\n3. Testing current_config...")
            current_config = config_service.current_config
            if current_config:
                print(f"Current configuration: {current_config.selected_options}")
                print(f"Calculated price: ${current_config.final_price:,.2f}")
            else:
                print("No current configuration found")
        
    except Exception as e:
        print(f"Error in configuration service test: {e}")
        logger.exception("Configuration service test failed")
    finally:
        db.close()

def main():
    """Run all tests."""
    print("Configuration Logic and Pricing Test")
    print("=" * 50)
    
    test_product_service()
    test_configuration_service()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main() 