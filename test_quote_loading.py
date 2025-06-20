"""
Test script to verify quote loading functionality.
"""

import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.core.database import SessionLocal
from src.core.services.quote_service import QuoteService
from src.core.services.customer_service import CustomerService
from src.core.services.product_service import ProductService

def test_quote_loading():
    """Test the quote loading functionality."""
    print("Testing quote loading functionality...")
    
    db = SessionLocal()
    
    try:
        # First, check if we have any quotes in the database
        quotes_summary = QuoteService.get_all_quotes_summary(db)
        print(f"Found {len(quotes_summary)} quotes in database")
        
        if not quotes_summary:
            print("No quotes found. Creating a test quote...")
            
            # Create a test customer
            customer = CustomerService.create_customer(
                db=db,
                name="Test Customer",
                company="Test Company",
                email="test@example.com",
                phone="555-123-4567"
            )
            
            # Get a product to add to the quote
            products = ProductService.get_product_variants(db)
            if not products:
                print("No products found in database. Cannot create test quote.")
                return
            
            product = products[0]
            print(f"Using product: {product.model_number}")
            
            # Create a test quote
            customer_data = {
                "name": customer.name,
                "company": customer.company,
                "email": customer.email,
                "phone": customer.phone
            }
            
            products_data = [{
                "product_id": product.id,
                "part_number": product.model_number,
                "quantity": 2,
                "base_price": product.base_price or 100.0,
                "options": []
            }]
            
            quote_details = {"notes": "Test quote for loading verification"}
            
            quote = QuoteService.create_quote_with_items(
                db=db,
                customer_data=customer_data,
                products_data=products_data,
                quote_details=quote_details
            )
            
            print(f"Created test quote: {quote.quote_number}")
        
        # Now test loading the first quote
        quotes_summary = QuoteService.get_all_quotes_summary(db)
        if quotes_summary:
            first_quote = quotes_summary[0]
            quote_id = first_quote["id"]
            
            print(f"\nTesting loading quote {first_quote['quote_number']} (ID: {quote_id})...")
            
            # Load the full quote details
            quote_details = QuoteService.get_full_quote_details(db, quote_id)
            
            if quote_details:
                print("✓ Quote details loaded successfully")
                print(f"  Quote Number: {quote_details.get('quote_number')}")
                print(f"  Customer: {quote_details.get('customer', {}).get('name')}")
                print(f"  Products: {len(quote_details.get('products', []))}")
                
                for i, product in enumerate(quote_details.get('products', [])):
                    print(f"    Product {i+1}: {product.get('part_number')} - {product.get('product_family')}")
                    print(f"      Quantity: {product.get('quantity')}")
                    print(f"      Base Price: ${product.get('base_price', 0):.2f}")
                    print(f"      Options: {len(product.get('options', []))}")
                    
                    for option in product.get('options', []):
                        print(f"        - {option.get('name')}: {option.get('selected')} (${option.get('price', 0):.2f})")
                
                # Test the transformation logic
                print("\nTesting data transformation...")
                from src.ui.views.quote_creation_redesign import QuoteCreationPageRedesign
                
                # Create a temporary instance to test the transformation
                quote_page = QuoteCreationPageRedesign()
                
                # Test the transformation methods
                products = quote_details.get('products', [])
                if products:
                    product = products[0]
                    options = product.get('options', [])
                    
                    # Test configuration formatting
                    config = quote_page._format_loaded_configuration(options)
                    print(f"  Configuration string: {config}")
                    
                    # Test options transformation
                    ui_options = quote_page._transform_options_to_ui_format(options)
                    print(f"  UI options format: {ui_options}")
                    
                    # Test full item transformation
                    item = {
                        "product_family": product.get("product_family", product.get("name", "Unknown")),
                        "model_number": product.get("part_number", "Unknown"),
                        "quantity": product.get("quantity", 1),
                        "unit_price": product.get("base_price", 0.0),
                        "total_price": product.get("base_price", 0.0) * product.get("quantity", 1),
                        "configuration": quote_page._format_loaded_configuration(product.get("options", [])),
                        "config_data": {
                            "product_data": {
                                "id": product.get("product_id"),
                                "family_name": product.get("product_family", product.get("name", "Unknown")),
                                "description": product.get("description", "")
                            },
                            "selected_options": quote_page._transform_options_to_ui_format(product.get("options", []))
                        }
                    }
                    
                    print(f"  Transformed item structure:")
                    print(f"    product_family: {item['product_family']}")
                    print(f"    model_number: {item['model_number']}")
                    print(f"    quantity: {item['quantity']}")
                    print(f"    unit_price: {item['unit_price']}")
                    print(f"    total_price: {item['total_price']}")
                    print(f"    configuration: {item['configuration']}")
                    print(f"    config_data keys: {list(item['config_data'].keys())}")
                
                print("\n✓ Quote loading test completed successfully!")
                
            else:
                print("✗ Failed to load quote details")
        
        else:
            print("No quotes found in database")
    
    except Exception as e:
        print(f"✗ Error during quote loading test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    test_quote_loading() 