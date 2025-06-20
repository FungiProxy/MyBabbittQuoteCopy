#!/usr/bin/env python3
"""
Test script for the new length adder rules system.
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

from src.core.database import SessionLocal, init_db
from src.core.services.product_service import ProductService
from sqlalchemy import text

def test_length_adder_rules():
    """Test the length adder rules with various scenarios."""
    
    # Initialize database
    init_db()
    
    # Create service
    service = ProductService()
    
    print("Testing Length Adder Rules")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        # (product_family, material, length, expected_adder, description)
        ('LS2000', 'S', 10, 0, 'LS2000 S material at base length (no adder)'),
        ('LS2000', 'S', 24, 0, 'LS2000 S material at threshold (no adder yet)'),
        ('LS2000', 'S', 36, 45, 'LS2000 S material at 36" (1 foot beyond 24")'),
        ('LS2000', 'S', 48, 90, 'LS2000 S material at 48" (2 feet beyond 24")'),
        ('LS2000', 'H', 24, 0, 'LS2000 H material at threshold (no adder yet)'),
        ('LS2000', 'H', 36, 110, 'LS2000 H material at 36" (1 foot beyond 24")'),
        ('LS2000', 'U', 4, 0, 'LS2000 U material at base length (no adder)'),
        ('LS2000', 'U', 8, 160, 'LS2000 U material at 8" (4 inches beyond 4")'),
        ('FS10000', 'S', 18, 0, 'FS10000 S material at threshold (no adder yet)'),
        ('FS10000', 'S', 30, 45, 'FS10000 S material at 30" (1 foot beyond 18")'),
        ('LS6000', 'CPVC', 4, 0, 'LS6000 CPVC material at base length (no adder)'),
        ('LS6000', 'CPVC', 8, 200, 'LS6000 CPVC material at 8" (4 inches beyond 4")'),
    ]
    
    for product_family, material, length, expected, description in test_cases:
        result = service.calculate_length_price(product_family, material, length)
        status = "✓" if result == expected else "✗"
        print(f"{status} {description}")
        print(f"   Expected: ${expected}, Got: ${result}")
        print()
    
    # Test getting rules
    print("Testing Rule Retrieval")
    print("=" * 30)
    
    rules = service.get_length_adder_rules(product_family='LS2000')
    print(f"Found {len(rules)} rules for LS2000:")
    for rule in rules:
        print(f"  {rule['material_code']}: {rule['adder_type']} starting at {rule['first_threshold']}\" = ${rule['adder_amount']}")
    
    print()
    
    # Test database query directly
    print("Testing Direct Database Query")
    print("=" * 35)
    
    with SessionLocal() as session:
        query = text("""
            SELECT product_family, material_code, adder_type, first_threshold, adder_amount
            FROM length_adder_rules 
            WHERE product_family = 'FS10000'
        """)
        
        result = session.execute(query).fetchall()
        print(f"FS10000 rules:")
        for row in result:
            print(f"  {row.material_code}: {row.adder_type} starting at {row.first_threshold}\" = ${row.adder_amount}")

if __name__ == "__main__":
    test_length_adder_rules() 