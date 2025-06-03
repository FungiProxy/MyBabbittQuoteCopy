"""
Script to run the business logic tests with proper path handling.
"""
import os
import sys
import importlib.util

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the test module
from scripts.test_business_logic import (
    test_customer_service,
    test_product_service,
    test_quote_service
)

if __name__ == "__main__":
    """Run tests based on command-line arguments."""
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        if test_name == "customer":
            test_customer_service()
        elif test_name == "product":
            test_product_service()
        elif test_name == "quote":
            test_quote_service()
        else:
            print(f"Unknown test: {test_name}")
            print("Available tests: customer, product, quote")
    else:
        print("Running all tests...\n")
        test_customer_service()
        test_product_service()
        test_quote_service() 