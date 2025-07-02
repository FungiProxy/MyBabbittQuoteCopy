#!/usr/bin/env python3
"""
Debug script to examine configuration data structure for export issues.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.services.export_service import QuoteExportService

def debug_config_data():
    """Debug the configuration data structure to identify export issues."""
    
    # Create sample configuration data that should be present
    sample_config = {
        "Voltage": "24VDC",
        "Material": "H",
        "Probe Length": "24",
        "Connection Type": "NPT",
        "Connection Material": "S",  # This should be present
        "NPT Size": "1\"",
        "Insulator Material": "TEF",
        "Insulator Length": "4"
    }
    
    # Create sample item data
    sample_item = {
        'product': 'LS2000',
        'product_family': 'LS2000',
        'model_number': 'LS2000-24VDC-H-24"-TEFINS',
        'description': 'LS2000 Level Sensor',
        'material': 'H',
        'voltage': '24VDC',
        'length': '24',
        'quantity': 1,
        'unit_price': 785.0,
        'total_price': 785.0,
        'config_data': sample_config,
        'configuration': sample_config,  # for legacy support
        'connection_type': 'NPT',
        'connection_material': 'S',
    }
    
    # Create sample quote data
    quote_data = {
        'quote_number': 'Q-2025-0701-001',
        'quote_date': '2025-07-01',
        'customer': {
            'name': 'ABC',
            'company': 'ABC Company',  # This should populate cust_company
            'contact_name': 'ABC',
            'email': 'abc@example.com',
            'phone': '(555) 123-4567',
        },
        'customer_name': 'ABC',
        'customer_company': 'ABC Company',
        'items': [sample_item],
        'total_price': 785.0
    }
    
    print("🔍 Debugging Configuration Data Structure")
    print(f"📋 Sample Config Data: {sample_config}")
    print(f"📦 Sample Item Data: {sample_item}")
    print(f"📄 Sample Quote Data: {quote_data}")
    
    # Test the export service
    export_service = QuoteExportService()
    template_data = export_service._prepare_template_data(quote_data)
    
    print(f"\n🎯 Template Data Results:")
    print(f"  cust_name: '{template_data.get('cust_name', 'NOT FOUND')}'")
    print(f"  cust_company: '{template_data.get('cust_company', 'NOT FOUND')}'")
    print(f"  p1_name: '{template_data.get('p1_name', 'NOT FOUND')}'")
    print(f"  p1_conn: '{template_data.get('p1_conn', 'NOT FOUND')}'")
    print(f"  p1_connmat: '{template_data.get('p1_connmat', 'NOT FOUND')}'")
    print(f"  p1_volt: '{template_data.get('p1_volt', 'NOT FOUND')}'")
    print(f"  p1_mat: '{template_data.get('p1_mat', 'NOT FOUND')}'")
    print(f"  p1_len: '{template_data.get('p1_len', 'NOT FOUND')}'")
    
    # Test the connection material formatting specifically
    print(f"\n🔧 Connection Material Formatting Test:")
    conn_mat = export_service._format_connection_material(sample_item)
    print(f"  _format_connection_material result: '{conn_mat}'")
    
    # Test insulator material formatting
    print(f"\n🔧 Insulator Material Formatting Test:")
    ins_mat = export_service._format_insulator_material(sample_item)
    print(f"  _format_insulator_material result: '{ins_mat}'")

if __name__ == "__main__":
    debug_config_data() 