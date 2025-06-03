"""
Test script for business logic services.
"""
import sys
from datetime import datetime

from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.core.models import Option
from src.core.services import QuoteService, CustomerService, ProductService
from src.utils.db_utils import get_by_id


def test_customer_service():
    """Test CustomerService functionality."""
    print("\n===== Testing CustomerService =====")
    db = SessionLocal()
    
    try:
        # Create a new customer
        print("Creating a new customer...")
        customer = CustomerService.create_customer(
            db=db,
            name="John Doe",
            company="Test Company",
            email="john@example.com",
            phone="555-123-4567",
            address="123 Main St",
            city="Anytown",
            state="CA",
            zip_code="12345",
            notes="Test customer"
        )
        print(f"Created customer: {customer.name} at {customer.company} (ID: {customer.id})")
        
        # Get all customers
        all_customers = CustomerService.get_all_customers(db)
        print(f"Total customers: {len(all_customers)}")
        
        # Search for customers
        search_results = CustomerService.search_customers(db, "Test")
        print(f"Search results for 'Test': {len(search_results)} customers found")
        for cust in search_results:
            print(f"  - {cust.name} at {cust.company} (ID: {cust.id})")
            
        # Update customer
        print(f"Updating customer {customer.id}...")
        updated_customer = CustomerService.update_customer(
            db=db,
            customer_id=customer.id,
            values={"name": "Jane Smith", "email": "jane@example.com"}
        )
        print(f"Updated customer: {updated_customer.name} at {updated_customer.company}")
        
        # Clean up (delete the test customer)
        print(f"Deleting test customer {customer.id}...")
        success = CustomerService.delete_customer(db, customer.id)
        print(f"Deletion {'successful' if success else 'failed'}")
        
    finally:
        db.close()


def test_product_service():
    """Test ProductService functionality."""
    print("\n===== Testing ProductService =====")
    db = SessionLocal()
    
    try:
        # Get product families
        families = ProductService.get_product_families(db)
        if not families:
            print("No product families found in database.")
            return
            
        print(f"Found {len(families)} product families:")
        for family in families[:3]:  # Show only first 3 families
            print(f"  - {family.name} (ID: {family.id})")
            if len(families) > 3 and family == families[2]:
                print(f"  ... and {len(families) - 3} more")
                
        # Get variants for the first family
        family_id = families[0].id
        variants = ProductService.get_product_variants(db, family_id=family_id)
        print(f"\nFound {len(variants)} variants for family ID {family_id}:")
        for variant in variants[:3]:  # Show only first 3 variants
            print(f"  - {variant.model_number}: {variant.description} (ID: {variant.id})")
            if len(variants) > 3 and variant == variants[2]:
                print(f"  ... and {len(variants) - 3} more")
        
        if variants:
            # Test product configuration and pricing
            print("\nTesting product configuration and pricing:")
            product_id = variants[0].id
            product, price = ProductService.configure_product(db, product_id)
            print(f"Product: {product.model_number}, Base Price: ${price:.2f}")
            
            # Try with custom length if applicable
            if hasattr(product, 'base_length'):
                custom_length = product.base_length + 12  # Add 12 inches
                product, price = ProductService.configure_product(
                    db, product_id, length=custom_length
                )
                print(f"Same product with length {custom_length}\" - Price: ${price:.2f}")
        
        # Test material retrieval
        materials = ProductService.get_available_materials(db)
        print(f"\nFound {len(materials)} materials:")
        for material in materials[:5]:  # Show only first 5 materials
            print(f"  - {material.code}: {material.description}")
            if len(materials) > 5 and material == materials[4]:
                print(f"  ... and {len(materials) - 5} more")
                
        # Test options retrieval
        options = ProductService.get_product_options(db)
        print(f"\nFound {len(options)} options:")
        for option in options[:5]:  # Show only first 5 options
            print(f"  - {option.name}: ${option.price} ({option.price_type})")
            if len(options) > 5 and option == options[4]:
                print(f"  ... and {len(options) - 5} more")
                
    finally:
        db.close()


def test_quote_service():
    """Test QuoteService functionality."""
    print("\n===== Testing QuoteService =====")
    db = SessionLocal()
    
    try:
        # First, get a customer (create one if needed)
        customers = CustomerService.get_all_customers(db)
        if not customers:
            print("Creating a test customer first...")
            customer = CustomerService.create_customer(
                db=db,
                name="Quote Tester",
                company="Quote Test Company",
                email="quote@example.com"
            )
        else:
            customer = customers[0]
            
        print(f"Using customer: {customer.name} at {customer.company} (ID: {customer.id})")
        
        # Create a new quote
        print("\nCreating a new quote...")
        quote = QuoteService.create_quote(
            db=db,
            customer_id=customer.id,
            expiration_days=30,
            notes="Test quote created by test script"
        )
        print(f"Created quote: {quote.quote_number} (ID: {quote.id})")
        
        # Get product variants to add to the quote
        variants = ProductService.get_product_variants(db)
        if not variants:
            print("No product variants found in database.")
            return
            
        # Add a product to the quote
        product = variants[0]
        print(f"\nAdding product {product.model_number} to quote...")
        quote_item = QuoteService.add_product_to_quote(
            db=db,
            quote_id=quote.id,
            product_id=product.id,
            quantity=2
        )
        print(f"Added line item: {quote_item.description} - ${quote_item.unit_price:.2f} each")
        
        # Get options
        options = ProductService.get_product_options(db)
        if options:
            # Add an option to the quote item
            option = options[0]
            print(f"\nAdding option '{option.name}' to quote item...")
            quote_item_option = QuoteService.add_option_to_quote_item(
                db=db,
                quote_item_id=quote_item.id,
                option_id=option.id,
                quantity=1
            )
            print(f"Added option: {option.name} - ${quote_item_option.price:.2f}")
        
        # Update quote status
        print("\nUpdating quote status to 'sent'...")
        updated_quote = QuoteService.update_quote_status(db, quote.id, "sent")
        print(f"Updated quote status: {updated_quote.status}")
        
        # Get fresh quote data to see totals
        db.refresh(quote)
        print(f"\nQuote total: ${quote.total:.2f}")
        print(f"Quote items: {len(quote.items)}")
        for item in quote.items:
            print(f"  - {item.description}: {item.quantity} x ${item.unit_price:.2f} = ${item.total:.2f}")
            if item.options:
                for option_item in item.options:
                    option = get_by_id(db, Option, option_item.option_id)
                    print(f"    + {option.name}: {option_item.quantity} x ${option_item.price:.2f}")
                    
    finally:
        db.close()


if __name__ == "__main__":
    """Run the test functions based on command line arguments."""
    if len(sys.argv) > 1:
        test_function = sys.argv[1].lower()
        if test_function == "customer":
            test_customer_service()
        elif test_function == "product":
            test_product_service()
        elif test_function == "quote":
            test_quote_service()
        else:
            print(f"Unknown test function: {test_function}")
            print("Available options: customer, product, quote")
    else:
        print("Testing all services...")
        test_customer_service()
        test_product_service()
        test_quote_service() 