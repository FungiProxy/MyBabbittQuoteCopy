"""
Service for managing customers - COMPLETE IMPLEMENTATION.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from src.core.models import Customer
from src.utils.db_utils import (
    add_and_commit,
    delete_and_commit,
    get_all,
    get_by_id,
    update_and_commit,
)

logger = logging.getLogger(__name__)


class CustomerService:
    """Service class for managing customers in the quoting system."""

    @staticmethod
    def create_customer(
        db: Session,
        name: str,
        company: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Customer:
        """Create a new customer."""
        customer = Customer(
            name=name,
            company=company,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            notes=notes,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        return add_and_commit(db, customer)

    @staticmethod
    def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
        """Get a customer by ID."""
        return get_by_id(db, Customer, customer_id)

    @staticmethod
    def get_all_customers(db: Session) -> List[Customer]:
        """Get all customers."""
        return get_all(db, Customer)

    @staticmethod
    def search_customers(
        db: Session, 
        search_term: str
    ) -> List[Customer]:
        """Search customers by name, company, email, or phone."""
        query = db.query(Customer)
        
        # Apply search filter
        if search_term:
            search_filter = or_(
                Customer.name.ilike(f"%{search_term}%"),
                Customer.company.ilike(f"%{search_term}%"),
                Customer.email.ilike(f"%{search_term}%"),
                Customer.phone.ilike(f"%{search_term}%"),
            )
            query = query.filter(search_filter)
        
        # Apply status filter (for future use with active/inactive status)
        # For now, just return all matching customers
        
        return query.order_by(Customer.name).all()

    @staticmethod
    def update_customer(
        db: Session, customer_id: int, updates: Dict[str, Any]
    ) -> Optional[Customer]:
        """Update a customer's information.
        
        Args:
            db: Database session
            customer_id: ID of customer to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated customer or None if not found
        """
        customer = get_by_id(db, Customer, customer_id)
        if not customer:
            return None
        
        # Update timestamp
        updates["updated_at"] = datetime.utcnow()
        
        return update_and_commit(db, customer, updates)

    @staticmethod
    def delete_customer(db: Session, customer_id: int) -> bool:
        """Delete a customer.
        
        Args:
            db: Database session
            customer_id: ID of customer to delete
            
        Returns:
            True if deleted, False if not found
        """
        customer = get_by_id(db, Customer, customer_id)
        if not customer:
            return False
        
        return delete_and_commit(db, customer)

    @staticmethod
    def get_customer_quotes(db: Session, customer_id: int) -> List[Dict]:
        """Get all quotes for a specific customer.
        
        Args:
            db: Database session
            customer_id: ID of the customer
            
        Returns:
            List of quote dictionaries
        """
        from src.core.models import Quote
        
        quotes = db.query(Quote).filter(Quote.customer_id == customer_id).all()
        
        return [
            {
                "id": quote.id,
                "quote_number": quote.quote_number,
                "date": quote.created_at.strftime("%Y-%m-%d"),
                "total": quote.total_price,
                "status": quote.status,
                "items_count": len(quote.items) if quote.items else 0,
            }
            for quote in quotes
        ]

    @staticmethod
    def get_customer_statistics(db: Session, customer_id: int) -> Dict:
        """Get statistics for a specific customer.
        
        Args:
            db: Database session
            customer_id: ID of the customer
            
        Returns:
            Dictionary with customer statistics
        """
        from src.core.models import Quote
        
        stats = db.query(
            func.count(Quote.id).label("total_quotes"),
            func.sum(Quote.total_price).label("total_value"),
            func.max(Quote.created_at).label("last_quote_date"),
        ).filter(Quote.customer_id == customer_id).first()
        
        return {
            "total_quotes": stats.total_quotes or 0,
            "total_value": float(stats.total_value or 0),
            "last_quote_date": stats.last_quote_date.strftime("%Y-%m-%d") 
                              if stats.last_quote_date else None,
        }

    @staticmethod
    def merge_duplicate_customers(
        db: Session, 
        primary_id: int, 
        duplicate_id: int
    ) -> Optional[Customer]:
        """Merge two duplicate customer records.
        
        Args:
            db: Database session
            primary_id: ID of the primary customer to keep
            duplicate_id: ID of the duplicate customer to merge
            
        Returns:
            The merged customer or None if not found
        """
        primary = get_by_id(db, Customer, primary_id)
        duplicate = get_by_id(db, Customer, duplicate_id)
        
        if not primary or not duplicate:
            return None
        
        # Update all quotes from duplicate to primary
        from src.core.models import Quote
        db.query(Quote).filter(Quote.customer_id == duplicate_id).update(
            {"customer_id": primary_id}
        )
        
        # Merge data (keep primary data unless it's empty)
        updates = {}
        for field in ["company", "email", "phone", "address", "city", "state", "zip_code"]:
            primary_value = getattr(primary, field)
            duplicate_value = getattr(duplicate, field)
            if not primary_value and duplicate_value:
                updates[field] = duplicate_value
        
        # Merge notes
        if duplicate.notes:
            if primary.notes:
                updates["notes"] = f"{primary.notes}\n\n--- Merged from duplicate ---\n{duplicate.notes}"
            else:
                updates["notes"] = duplicate.notes
        
        # Update primary customer
        if updates:
            primary = update_and_commit(db, primary, updates)
        
        # Delete duplicate
        delete_and_commit(db, duplicate)
        
        return primary