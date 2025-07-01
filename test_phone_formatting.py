#!/usr/bin/env python3
"""
Test script for phone number formatting functionality.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from src.utils.phone_formatter import format_phone_number, is_valid_phone_number, clean_phone_number


def test_phone_formatting():
    """Test phone number formatting functions."""
    
    print("Testing Phone Number Formatting")
    print("=" * 40)
    
    # Test cases
    test_cases = [
        ("5551234567", "(555) 123-4567"),
        ("555-123-4567", "(555) 123-4567"),
        ("(555) 123-4567", "(555) 123-4567"),
        ("555.123.4567", "(555) 123-4567"),
        ("555 123 4567", "(555) 123-4567"),
        ("555123456", None),  # Too few digits
        ("55512345678", None),  # Too many digits
        ("", None),  # Empty
        ("abc123def", None),  # Invalid
        ("123", None),  # Too short
    ]
    
    for input_phone, expected in test_cases:
        result = format_phone_number(input_phone)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: '{input_phone}' -> Output: '{result}' (Expected: '{expected}')")
    
    print("\nTesting Phone Number Validation")
    print("=" * 40)
    
    validation_tests = [
        ("5551234567", True),
        ("555-123-4567", True),
        ("(555) 123-4567", True),
        ("555123456", False),
        ("55512345678", False),
        ("", False),
        ("abc123def", False),
    ]
    
    for input_phone, expected in validation_tests:
        result = is_valid_phone_number(input_phone)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: '{input_phone}' -> Valid: {result} (Expected: {expected})")
    
    print("\nTesting Phone Number Cleaning")
    print("=" * 40)
    
    cleaning_tests = [
        ("(555) 123-4567", "5551234567"),
        ("555-123-4567", "5551234567"),
        ("555.123.4567", "5551234567"),
        ("555 123 4567", "5551234567"),
        ("", None),
        ("abc123def", "123"),
    ]
    
    for input_phone, expected in cleaning_tests:
        result = clean_phone_number(input_phone)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: '{input_phone}' -> Cleaned: '{result}' (Expected: '{expected}')")
    
    print("\n" + "=" * 40)
    print("Phone formatting test completed!")


if __name__ == "__main__":
    test_phone_formatting() 