#!/usr/bin/env python3
"""
Test script to examine the actual configuration data structure from the UI.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_config_data_structure():
    """Test what the configuration data structure looks like from the UI."""
    
    # This is what the ModernProductSelectionDialog should return
    # based on the code I found
    sample_config_from_dialog = {
        'product': 'LS2000',
        'product_id': 1,
        'description': 'LS2000 Level Sensor',
        'unit_price': 785.0,
        'quantity': 1,
        'total_price': 785.0,
        'configuration': {
            'Voltage': '24VDC',
            'Material': 'H',
            'Probe Length': '24',
            'Connection Type': 'NPT',
            'Connection Material': 'S',
            'NPT Size': '1"',
            'Insulator Material': 'TEF',
            'Insulator Length': '4'
        },
        'model_number': 'LS2000-24VDC-H-24"-TEFINS',
        'config_data': {
            'Voltage': '24VDC',
            'Material': 'H',
            'Probe Length': '24',
            'Connection Type': 'NPT',
            'Connection Material': 'S',
            'NPT Size': '1"',
            'Insulator Material': 'TEF',
            'Insulator Length': '4'
        },
        'options': []
    }
    
    print("🔍 Testing Configuration Data Structure from UI")
    print(f"📋 Sample config from dialog: {sample_config_from_dialog}")
    
    # Test how this would be processed in _on_product_configured
    config_data = sample_config_from_dialog
    
    # Simulate the processing in _on_product_configured
    quote_item = {
        "product_id": config_data.get("product_id"),
        "product_family": config_data.get("product", "N/A"),
        "model_number": config_data.get("model_number", config_data.get("product", "N/A")),
        "configuration": config_data.get("description", "Standard Configuration"),
        "quantity": config_data.get("quantity", 1),
        "unit_price": config_data.get("unit_price", 0),
        "total_price": config_data.get("total_price", 0),
        "config_data": config_data.get("configuration", {}),
        "options": config_data.get("options", []),
        "is_spare_part": config_data.get("is_spare_part", False),
        "spare_part_data": config_data.get("spare_part_data", {}),
        "base_product_info": config_data.get("base_product_info", {})
    }
    
    print(f"\n📦 Quote item after processing: {quote_item}")
    
    # Test how this would be processed in _prepare_quote_data_for_export
    config = quote_item.get("config_data", {})
    if not config:
        config = quote_item.get("configuration", {})
    
    connection_type = config.get("Connection Type", "")
    connection_material = config.get("Connection Material", "")
    voltage = config.get("Voltage", quote_item.get("voltage", ""))
    material = config.get("Material", quote_item.get("material", ""))
    length = config.get("Probe Length", quote_item.get("length", ""))
    model_number = quote_item.get("model_number", "")
    description = quote_item.get("description", "")
    
    export_item = {
        'product': quote_item.get("product_family", "N/A"),
        'product_family': quote_item.get("product_family", "N/A"),
        'model_number': model_number,
        'description': description,
        'material': material,
        'voltage': voltage,
        'length': length,
        'quantity': quote_item.get("quantity", 1),
        'unit_price': quote_item.get("unit_price", 0.0),
        'total_price': quote_item.get("total_price", 0.0),
        'config_data': config,
        'configuration': config,
        'connection_type': connection_type,
        'connection_material': connection_material,
    }
    
    print(f"\n📤 Export item after processing: {export_item}")
    
    # Test the export service
    from src.core.services.export_service import QuoteExportService
    
    quote_data = {
        'quote_number': 'Q-2025-0701-001',
        'quote_date': '2025-07-01',
        'customer': {
            'name': 'ABC',
            'company': 'ABC Company',
            'contact_name': 'ABC',
            'email': 'abc@example.com',
            'phone': '(555) 123-4567',
        },
        'customer_name': 'ABC',
        'customer_company': 'ABC Company',
        'items': [export_item],
        'total_price': 785.0
    }
    
    export_service = QuoteExportService()
    template_data = export_service._prepare_template_data(quote_data)
    
    print(f"\n🎯 Final Template Data Results:")
    print(f"  cust_name: '{template_data.get('cust_name', 'NOT FOUND')}'")
    print(f"  cust_company: '{template_data.get('cust_company', 'NOT FOUND')}'")
    print(f"  p1_name: '{template_data.get('p1_name', 'NOT FOUND')}'")
    print(f"  p1_conn: '{template_data.get('p1_conn', 'NOT FOUND')}'")
    print(f"  p1_connmat: '{template_data.get('p1_connmat', 'NOT FOUND')}'")
    print(f"  p1_volt: '{template_data.get('p1_volt', 'NOT FOUND')}'")
    print(f"  p1_mat: '{template_data.get('p1_mat', 'NOT FOUND')}'")
    print(f"  p1_len: '{template_data.get('p1_len', 'NOT FOUND')}'")

if __name__ == "__main__":
    test_config_data_structure() 