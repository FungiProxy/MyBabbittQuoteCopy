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

import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload

from src.core.models import (
    BaseModel,
    Customer,
    ProductFamily,
    Quote,
    QuoteItem,
    QuoteItemOption,
)
from src.core.services.customer_service import CustomerService
from src.utils.db_utils import add_and_commit, generate_quote_number, get_by_id


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
        notes: Optional[str] = None,
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
            status='draft',
            expiration_date=expiration_date,
            notes=notes,
        )

        return add_and_commit(db, quote)

    @staticmethod
    def create_quote_with_items(
        db: Session,
        customer_data: Dict[str, Any],
        products_data: List[Dict[str, Any]],
        quote_details: Dict[str, Any],
    ) -> Quote:
        """
        Create a full quote including customer, quote items, and options.
        """
        customer = (
            db.query(Customer)
            .filter(Customer.email == customer_data.get('email'))
            .first()
        )
        if not customer:
            customer = CustomerService.create_customer(db, **customer_data)

        quote = QuoteService.create_quote(
            db,
            customer_id=customer.id,
            expiration_days=30,
            notes=quote_details.get('notes'),
        )

        for product_data in products_data:
            quote_item = QuoteItem(
                quote_id=quote.id,
                product_id=product_data.get('product_id'),
                quantity=product_data.get('quantity', 1),
                unit_price=product_data.get('base_price', 0),
                description=product_data.get('part_number'),
            )
            db.add(quote_item)
            db.flush()

            for option_data in product_data.get('options', []):
                if option_data.get('id'):
                    db.add(
                        QuoteItemOption(
                            quote_item_id=quote_item.id,
                            option_id=option_data['id'],
                            quantity=1,
                            price=option_data.get('price', 0),
                        )
                    )

        db.commit()
        db.refresh(quote)
        return quote

    @staticmethod
    def get_all_quotes_summary(db: Session) -> List[Dict[str, Any]]:
        """
        Retrieves a summary of all quotes.
        """
        quotes = (
            db.query(Quote)
            .options(
                joinedload(Quote.customer),
                selectinload(Quote.items),  # Eager load items to calculate total
            )
            .order_by(Quote.date_created.desc())
            .all()
        )

        return [
            {
                'id': quote.id,
                'quote_number': quote.quote_number,
                'customer_name': quote.customer.name,
                'date_created': quote.date_created.strftime('%Y-%m-%d'),
                'total': quote.total,
            }
            for quote in quotes
        ]

    @staticmethod
    def get_full_quote_details(db: Session, quote_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves full details for a single quote, formatted for the UI.
        """
        quote = (
            db.query(Quote)
            .options(
                joinedload(Quote.customer),
                joinedload(Quote.items)
                .joinedload(QuoteItem.product)
                .joinedload(BaseModel.product_family),
                joinedload(Quote.items)
                .joinedload(QuoteItem.options)
                .joinedload(QuoteItemOption.option),
            )
            .filter(Quote.id == quote_id)
            .first()
        )

        if not quote:
            return None

        products_data = [
            {
                'id': str(uuid.uuid4()),
                'part_number': item.description,
                'product_id': item.product.id,
                'name': item.product.product_family.name,
                'quantity': item.quantity,
                'base_price': item.unit_price,
                'options': [
                    {
                        'id': item_opt.option.id,
                        'name': item_opt.option.category,
                        'selected': item_opt.option.name,
                        'price': item_opt.price,
                        'code': item_opt.option.code,
                    }
                    for item_opt in item.options
                ],
                'description': item.product.product_family.description,
            }
            for item in quote.items
        ]

        return {
            'quote_number': quote.quote_number,
            'customer': {
                'name': quote.customer.name,
                'company': quote.customer.company,
                'email': quote.customer.email,
                'phone': quote.customer.phone,
            },
            'products': products_data,
            'expiration_date': quote.expiration_date,
            'date_created': quote.date_created,
            'notes': quote.notes,
        }

    @staticmethod
    def update_quote_status(db: Session, quote_id: int, status: str) -> Quote:
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
        valid_statuses = ['draft', 'sent', 'accepted', 'rejected']
        if status not in valid_statuses:
            raise ValueError(
                f'Invalid status: {status}. Must be one of {valid_statuses}'
            )

        # Get quote
        quote = get_by_id(db, Quote, quote_id)
        if not quote:
            raise ValueError(f'Quote with ID {quote_id} not found')

        # Update status
        quote.status = status
        db.commit()
        db.refresh(quote)

        return quote

    @staticmethod
    def delete_quote(db: Session, quote_id: int) -> bool:
        """
        Deletes a quote from the database.

        Args:
            db: The database session.
            quote_id: The ID of the quote to delete.

        Returns:
            True if the quote was deleted, False otherwise.
        """
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if quote:
            db.delete(quote)
            db.commit()
            return True
        return False

    @staticmethod
    def get_dashboard_statistics(db: Session) -> Dict[str, Any]:
        """
        Get statistics for the dashboard overview.

        Returns:
            Dict containing:
            - total_quotes: Total number of quotes
            - total_quote_value: Total value of all quotes
            - total_customers: Total number of unique customers
            - total_products: Total number of unique products quoted
            - recent_quotes: List of recent quotes with basic info
            - sales_by_category: Sales breakdown by product category
        """
        # Get total quotes
        total_quotes = db.query(func.count(Quote.id)).scalar()

        # Get total quote value
        total_quote_value = (
            db.query(func.sum(QuoteItem.unit_price * QuoteItem.quantity)).scalar() or 0
        )

        # Get total unique customers
        total_customers = db.query(
            func.count(func.distinct(Quote.customer_id))
        ).scalar()

        # Get total unique products quoted
        total_products = db.query(
            func.count(func.distinct(QuoteItem.product_id))
        ).scalar()

        # Get recent quotes (last 5)
        recent_quotes = (
            db.query(Quote)
            .options(joinedload(Quote.customer))
            .order_by(Quote.date_created.desc())
            .limit(5)
            .all()
        )

        recent_quotes_data = [
            {
                'quote_number': quote.quote_number,
                'customer': quote.customer.name,
                'total': quote.total,
                'date': quote.date_created.strftime('%Y-%m-%d'),
            }
            for quote in recent_quotes
        ]

        # Get sales by product category
        sales_by_category = (
            db.query(
                ProductFamily.category,
                func.sum(QuoteItem.unit_price * QuoteItem.quantity).label('total'),
            )
            .join(BaseModel, BaseModel.id == QuoteItem.product_id)
            .join(ProductFamily, ProductFamily.id == BaseModel.product_family_id)
            .group_by(ProductFamily.category)
            .all()
        )

        # Calculate percentages for each category
        total_sales = (
            sum(cat.total for cat in sales_by_category) or 1
        )  # Avoid division by zero
        sales_by_category_data = [
            {
                'category': cat.category,
                'percentage': round((cat.total / total_sales) * 100),
            }
            for cat in sales_by_category
        ]

        # Get month-over-month changes
        last_month = datetime.now() - timedelta(days=30)
        current_month_quotes = (
            db.query(func.count(Quote.id))
            .filter(Quote.date_created >= last_month)
            .scalar()
        )

        previous_month_quotes = (
            db.query(func.count(Quote.id))
            .filter(
                Quote.date_created >= last_month - timedelta(days=30),
                Quote.date_created < last_month,
            )
            .scalar()
        )

        quote_change = (
            (
                (current_month_quotes - previous_month_quotes)
                / previous_month_quotes
                * 100
            )
            if previous_month_quotes
            else 0
        )

        current_month_value = (
            db.query(func.sum(QuoteItem.unit_price * QuoteItem.quantity))
            .join(Quote, Quote.id == QuoteItem.quote_id)
            .filter(Quote.date_created >= last_month)
            .scalar()
            or 0
        )

        previous_month_value = (
            db.query(func.sum(QuoteItem.unit_price * QuoteItem.quantity))
            .join(Quote, Quote.id == QuoteItem.quote_id)
            .filter(
                Quote.date_created >= last_month - timedelta(days=30),
                Quote.date_created < last_month,
            )
            .scalar()
            or 0
        )

        value_change = (
            ((current_month_value - previous_month_value) / previous_month_value * 100)
            if previous_month_value
            else 0
        )

        return {
            'total_quotes': total_quotes,
            'total_quote_value': total_quote_value,
            'total_customers': total_customers,
            'total_products': total_products,
            'recent_quotes': recent_quotes_data,
            'sales_by_category': sales_by_category_data,
            'quote_change': round(quote_change, 1),
            'value_change': round(value_change, 1),
        }
