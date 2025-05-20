"""
Service for managing quotes and quote items.

This module provides a service layer for managing quotes and quote-related operations
in Babbitt International's quoting system. It supports:
- Creating and updating quotes
- Adding products and options to quotes
- Managing quote statuses and line items
- Calculating prices for quote items and options

Follows domain-driven design and separates business logic from data access.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from src.core.models import Quote, QuoteItem, QuoteItemOption, ProductVariant, Option
from src.core.pricing import calculate_product_price, calculate_option_price
from src.utils.db_utils import add_and_commit, get_by_id, generate_quote_number


class QuoteService:
    """
    Service class for managing quotes and quote-related operations.
    
    Provides methods for creating quotes, adding products and options, updating
    quote statuses, and handling all quote-related business logic.
    
    Example:
        >>> db = SessionLocal()
        >>> quote = QuoteService.create_quote(db, customer_id=1)
        >>> item = QuoteService.add_product_to_quote(db, quote_id=quote.id, product_id=2)
        >>> option = QuoteService.add_option_to_quote_item(db, quote_item_id=item.id, option_id=3)
        >>> updated = QuoteService.update_quote_status(db, quote_id=quote.id, status="sent")
    """

    @staticmethod
    def create_quote(
        db: Session,
        customer_id: int,
        expiration_days: int = 30,
        notes: Optional[str] = None
    ) -> Quote:
        """
        Create a new quote for a customer.
        
        Args:
            db: Database session
            customer_id: ID of the customer for the quote
            expiration_days: Number of days until quote expires
            notes: Optional notes for the quote
            
        Returns:
            Newly created Quote object
        """
        # Generate quote number
        quote_number = generate_quote_number(db)
        
        # Calculate expiration date
        expiration_date = datetime.now() + timedelta(days=expiration_days)
        
        # Create quote
        quote = Quote(
            quote_number=quote_number,
            customer_id=customer_id,
            status="draft",
            expiration_date=expiration_date,
            notes=notes
        )
        
        return add_and_commit(db, quote)
    
    @staticmethod
    def add_product_to_quote(
        db: Session,
        quote_id: int,
        product_id: int,
        quantity: int = 1,
        length: Optional[float] = None,
        material_override: Optional[str] = None,
        description: Optional[str] = None,
        discount_percent: float = 0.0
    ) -> QuoteItem:
        """
        Add a product to an existing quote.
        
        Args:
            db: Database session
            quote_id: ID of the quote
            product_id: ID of the product variant
            quantity: Quantity of the product
            length: Length in inches (if applicable)
            material_override: Material code to override product's default
            description: Custom description for the quote item
            discount_percent: Discount percentage for this line item
            
        Returns:
            Newly created QuoteItem object
            
        Raises:
            ValueError: If quote or product not found
        """
        # Get quote
        quote = get_by_id(db, Quote, quote_id)
        if not quote:
            raise ValueError(f"Quote with ID {quote_id} not found")
        
        # Get product
        product = get_by_id(db, ProductVariant, product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        # If length is not specified, use product's base length
        if length is None and hasattr(product, 'base_length'):
            length = product.base_length
            
        # If material is not specified, use product's default material
        if material_override is None and hasattr(product, 'material'):
            material_override = product.material
            
        # Calculate unit price
        unit_price = calculate_product_price(
            db=db, 
            product_id=product_id, 
            length=length, 
            material_override=material_override
        )
        
        # Create quote item
        quote_item = QuoteItem(
            quote_id=quote_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            length=length,
            material=material_override,
            voltage=product.voltage if hasattr(product, 'voltage') else None,
            description=description or product.description,
            discount_percent=discount_percent
        )
        
        return add_and_commit(db, quote_item)
    
    @staticmethod
    def add_option_to_quote_item(
        db: Session,
        quote_item_id: int,
        option_id: int,
        quantity: int = 1
    ) -> QuoteItemOption:
        """
        Add an option to a quote line item.
        
        Args:
            db: Database session
            quote_item_id: ID of the quote item
            option_id: ID of the option to add
            quantity: Quantity of the option
            
        Returns:
            Newly created QuoteItemOption
            
        Raises:
            ValueError: If quote item or option not found
        """
        # Get quote item
        quote_item = get_by_id(db, QuoteItem, quote_item_id)
        if not quote_item:
            raise ValueError(f"Quote item with ID {quote_item_id} not found")
        
        # Get option
        option = get_by_id(db, Option, option_id)
        if not option:
            raise ValueError(f"Option with ID {option_id} not found")
        
        # Calculate option price based on the quote item's length if needed
        price = calculate_option_price(
            option_price=option.price,
            option_price_type=option.price_type,
            length=quote_item.length
        )
        
        # Create quote item option
        quote_item_option = QuoteItemOption(
            quote_item_id=quote_item_id,
            option_id=option_id,
            quantity=quantity,
            price=price
        )
        
        return add_and_commit(db, quote_item_option)
    
    @staticmethod
    def update_quote_status(
        db: Session,
        quote_id: int,
        status: str
    ) -> Quote:
        """
        Update the status of a quote.
        
        Args:
            db: Database session
            quote_id: ID of the quote
            status: New status ("draft", "sent", "accepted", "rejected")
            
        Returns:
            Updated Quote
            
        Raises:
            ValueError: If quote not found or status invalid
        """
        # Validate status
        valid_statuses = ["draft", "sent", "accepted", "rejected"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")
        
        # Get quote
        quote = get_by_id(db, Quote, quote_id)
        if not quote:
            raise ValueError(f"Quote with ID {quote_id} not found")
        
        # Update status
        quote.status = status
        db.commit()
        db.refresh(quote)
        
        return quote 