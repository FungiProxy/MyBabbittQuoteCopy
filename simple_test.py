#!/usr/bin/env python3

import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

def test_quote_service():
    """Test the quote service directly."""
    try:
        from src.core.database import SessionLocal
        from src.core.services.quote_service import QuoteService
        
        print("Testing quote service...")
        
        db = SessionLocal()
        
        # Get all quotes
        quotes = QuoteService.get_all_quotes_summary(db)
        print(f"Found {len(quotes)} quotes in database")
        
        if quotes:
            # Test loading the first quote
            first_quote = quotes[0]
            quote_id = first_quote["id"]
            
            print(f"Loading quote {first_quote['quote_number']} (ID: {quote_id})...")
            
            quote_details = QuoteService.get_full_quote_details(db, quote_id)
            
            if quote_details:
                print("✓ Quote loaded successfully!")
                print(f"  Quote Number: {quote_details.get('quote_number')}")
                print(f"  Customer: {quote_details.get('customer', {}).get('name')}")
                print(f"  Products: {len(quote_details.get('products', []))}")
                
                for i, product in enumerate(quote_details.get('products', [])):
                    print(f"    Product {i+1}: {product.get('part_number')} - {product.get('product_family')}")
                    print(f"      Quantity: {product.get('quantity')}")
                    print(f"      Base Price: ${product.get('base_price', 0):.2f}")
                    print(f"      Options: {len(product.get('options', []))}")
            else:
                print("✗ Failed to load quote details")
        else:
            print("No quotes found in database")
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_quote_service() 