#!/usr/bin/env python3
"""
Debug script to examine quote data structure for export issues.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.services.export_service import QuoteExportService
from src.core.database import SessionLocal
from src.core.models.quote import Quote
from src.core.models.customer import Customer

def debug_quote_data():
    """Debug the quote data structure to identify export issues."""
    
    # Get a recent quote from the database
    db = SessionLocal()
    try:
        # Get the most recent quote
        quote = db.query(Quote).order_by(Quote.date_created.desc()).first()
        
        if not quote:
            print("❌ No quotes found in database")
            return
        
        print(f"🔍 Debugging Quote: {quote.quote_number}")
        print(f"📅 Created: {quote.date_created}")
        print(f"👤 Customer ID: {quote.customer_id}")
        
        # Get customer details
        customer = db.query(Customer).filter(Customer.id == quote.customer_id).first()
        if customer:
            print(f"👤 Customer Name: '{customer.name}'")
            print(f"🏢 Customer Company: '{customer.company}'")
            print(f"📧 Customer Email: '{customer.email}'")
            print(f"📞 Customer Phone: '{customer.phone}'")
        else:
            print("❌ Customer not found")
        
        # Get quote items
        print(f"\n📦 Quote Items ({len(quote.items)}):")
        for i, item in enumerate(quote.items, 1):
            print(f"\n  Item {i}:")
            print(f"    Product ID: {item.product_id}")
            print(f"    Description: '{item.description}'")
            print(f"    Quantity: {item.quantity}")
            print(f"    Unit Price: ${item.unit_price}")
            print(f"    Material: '{item.material}'")
            print(f"    Voltage: '{item.voltage}'")
            print(f"    Length: {item.length}")
            
            # Check for configuration data
            if hasattr(item, 'config_data'):
                print(f"    Config Data: {item.config_data}")
            if hasattr(item, 'configuration'):
                print(f"    Configuration: {item.configuration}")
        
        # Now test the export service data preparation
        print(f"\n🚀 Testing Export Service Data Preparation")
        
        # Prepare quote data as it would be passed to export service
        quote_data = {
            'quote_number': quote.quote_number,
            'quote_date': quote.date_created.strftime('%Y-%m-%d'),
            'customer': {
                'name': customer.name if customer else '',
                'company': customer.company if customer else '',
                'email': customer.email if customer else '',
                'phone': customer.phone if customer else '',
            },
            'items': []
        }
        
        for item in quote.items:
            item_data = {
                'product': item.description,
                'model_number': item.description,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'total_price': item.quantity * item.unit_price,
                'material': item.material,
                'voltage': item.voltage,
                'length': item.length,
                'config_data': {},  # This would normally contain the configuration
                'configuration': {}  # Legacy format
            }
            quote_data['items'].append(item_data)
        
        print(f"\n📋 Quote Data Structure:")
        print(f"  Quote Number: '{quote_data['quote_number']}'")
        print(f"  Quote Date: '{quote_data['quote_date']}'")
        print(f"  Customer Name: '{quote_data['customer']['name']}'")
        print(f"  Customer Company: '{quote_data['customer']['company']}'")
        print(f"  Items Count: {len(quote_data['items'])}")
        
        # Test the export service
        export_service = QuoteExportService()
        template_data = export_service._prepare_template_data(quote_data)
        
        print(f"\n🎯 Template Data Results:")
        print(f"  cust_name: '{template_data.get('cust_name', 'NOT FOUND')}'")
        print(f"  cust_company: '{template_data.get('cust_company', 'NOT FOUND')}'")
        print(f"  p1_conn: '{template_data.get('p1_conn', 'NOT FOUND')}'")
        print(f"  p1_connmat: '{template_data.get('p1_connmat', 'NOT FOUND')}'")
        print(f"  p1_volt: '{template_data.get('p1_volt', 'NOT FOUND')}'")
        print(f"  p1_mat: '{template_data.get('p1_mat', 'NOT FOUND')}'")
        
        # Check if there are any items
        if quote_data['items']:
            first_item = quote_data['items'][0]
            print(f"\n🔍 First Item Analysis:")
            print(f"  Product: '{first_item.get('product', 'N/A')}'")
            print(f"  Material: '{first_item.get('material', 'N/A')}'")
            print(f"  Voltage: '{first_item.get('voltage', 'N/A')}'")
            print(f"  Config Data: {first_item.get('config_data', {})}")
            print(f"  Configuration: {first_item.get('configuration', {})}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_quote_data() 