#!/usr/bin/env python3
"""
Test script to examine the actual current quote data structure.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_current_quote_data():
    """Test the actual current quote data structure."""
    
    # This is what your current quote data probably looks like (based on the export results)
    current_quote_data = {
        'quote_number': 'Q-2025-0701-001',
        'quote_date': '2025-07-01',
        'customer': {
            'name': 'ABC',
            'company': '',  # This is probably empty
            'contact_name': 'ABC',
            'email': 'abc@example.com',
            'phone': '(555) 123-4567',
        },
        'customer_name': 'ABC',
        'customer_company': '',  # This is probably empty
        'items': [
            {
                'product': 'LS2000',
                'product_family': 'LS2000',
                'model_number': 'LS2000',  # This is probably just the family name, not the full model number
                'description': 'LS2000 Level Sensor',
                'material': 'None',  # This is probably None or empty
                'voltage': 'None',   # This is probably None or empty
                'length': None,      # This is probably None or empty
                'quantity': 1,
                'unit_price': 785.0,
                'total_price': 785.0,
                'config_data': {},   # This is probably empty
                'configuration': {}, # This is probably empty
                'connection_type': '',
                'connection_material': '',
            }
        ],
        'total_price': 785.0
    }
    
    print("🔍 Testing Current Quote Data Structure")
    print(f"📋 Current quote data: {current_quote_data}")
    
    # Test the export service with this data
    from src.core.services.export_service import QuoteExportService
    
    export_service = QuoteExportService()
    template_data = export_service._prepare_template_data(current_quote_data)
    
    print(f"\n🎯 Template Data Results with Current Data:")
    print(f"  cust_name: '{template_data.get('cust_name', 'NOT FOUND')}'")
    print(f"  cust_company: '{template_data.get('cust_company', 'NOT FOUND')}'")
    print(f"  p1_name: '{template_data.get('p1_name', 'NOT FOUND')}'")
    print(f"  p1_conn: '{template_data.get('p1_conn', 'NOT FOUND')}'")
    print(f"  p1_connmat: '{template_data.get('p1_connmat', 'NOT FOUND')}'")
    print(f"  p1_volt: '{template_data.get('p1_volt', 'NOT FOUND')}'")
    print(f"  p1_mat: '{template_data.get('p1_mat', 'NOT FOUND')}'")
    print(f"  p1_len: '{template_data.get('p1_len', 'NOT FOUND')}'")
    
    print(f"\n❌ Issues identified:")
    print(f"  1. cust_company is empty because customer.company is empty")
    print(f"  2. p1_connmat is empty because config_data is empty")
    print(f"  3. p1_name shows 'LS2000' instead of full model number because model_number is not set")
    print(f"  4. p1_volt, p1_mat, p1_len are empty because config_data is empty")
    
    print(f"\n✅ Solutions:")
    print(f"  1. Fill in the company name in the UI")
    print(f"  2. Ensure products are configured with all options selected")
    print(f"  3. The configuration data should be saved in config_data when products are added")

if __name__ == "__main__":
    test_current_quote_data() 