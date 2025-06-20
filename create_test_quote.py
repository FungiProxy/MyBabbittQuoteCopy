#!/usr/bin/env python3

import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

def create_test_quote():
    """Create a test quote with products and options."""
    try:
        from src.core.database import SessionLocal
        from src.core.services.quote_service import QuoteService
        from src.core.services.customer_service import CustomerService
        from src.core.services.product_service import ProductService
        
        print("Creating test quote...")
        
        db = SessionLocal()
        
        # Create a test customer
        customer = CustomerService.create_customer(
            db=db,
            name="Test Customer",
            company="Test Company",
            email="test@example.com",
            phone="555-123-4567"
        )
        print(f"Created customer: {customer.name}")
        
        # Get products
        products = ProductService.get_product_variants(db)
        if not products:
            print("No products found. Creating a basic product...")
            # We need to create a product first
            from src.core.models import ProductFamily, BaseModel
            from src.core.services.product_service import ProductService
            
            # Create a product family
            family = ProductFamily(
                name="Test Family",
                description="Test product family",
                category="Test",
                base_price=100.0
            )
            db.add(family)
            db.flush()
            
            # Create a base model
            base_model = BaseModel(
                model_number="TEST-001",
                product_family_id=family.id,
                base_price=100.0
            )
            db.add(base_model)
            db.flush()
            
            products = [base_model]
        
        product = products[0]
        print(f"Using product: {product.model_number}")
        
        # Create quote data
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
        
        # Create the quote
        quote = QuoteService.create_quote_with_items(
            db=db,
            customer_data=customer_data,
            products_data=products_data,
            quote_details=quote_details
        )
        
        print(f"✓ Created test quote: {quote.quote_number}")
        print(f"  Quote ID: {quote.id}")
        print(f"  Customer: {quote.customer.name}")
        print(f"  Items: {len(quote.items)}")
        
        for item in quote.items:
            print(f"    - {item.description}: {item.quantity} x ${item.unit_price:.2f}")
        
        db.close()
        
        return quote.id
        
    except Exception as e:
        print(f"Error creating test quote: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    quote_id = create_test_quote()
    if quote_id:
        print(f"\nTest quote created with ID: {quote_id}")
        print("You can now test loading this quote in the application.") 