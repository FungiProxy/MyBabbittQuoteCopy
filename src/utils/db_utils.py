"""
Database utility functions for common operations.
"""
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session

from src.core.database import Base

# Generic type for SQLAlchemy models
T = TypeVar("T", bound=Base)


def add_and_commit(db: Session, obj: T) -> T:
    """Add object to database and commit."""
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def add_all_and_commit(db: Session, objects: List[T]) -> List[T]:
    """Add multiple objects to database and commit."""
    db.add_all(objects)
    db.commit()
    for obj in objects:
        db.refresh(obj)
    return objects


def get_by_id(db: Session, model: Type[T], id: int) -> Optional[T]:
    """Get object by ID."""
    return db.query(model).filter(model.id == id).first()


def get_all(db: Session, model: Type[T], **kwargs) -> List[T]:
    """Get all objects, optionally filtered by keyword arguments."""
    query = db.query(model)
    for key, value in kwargs.items():
        if hasattr(model, key):
            query = query.filter(getattr(model, key) == value)
    return query.all()


def update_and_commit(db: Session, obj: T, values: Dict[str, Any]) -> T:
    """Update object with values and commit."""
    for key, value in values.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_and_commit(db: Session, obj: T) -> bool:
    """Delete object and commit."""
    db.delete(obj)
    db.commit()
    return True


def generate_quote_number(db: Session) -> str:
    """Generate a unique quote number."""
    from src.core.models import Quote
    
    # Get the latest quote number
    latest_quote = db.query(Quote).order_by(Quote.id.desc()).first()
    
    if not latest_quote:
        # Start with 1001 if no quotes exist
        return "Q-1001"
    
    # Extract the numeric part and increment
    try:
        num_part = int(latest_quote.quote_number.split("-")[1])
        return f"Q-{num_part + 1}"
    except (ValueError, IndexError):
        # Fallback if quote number format is unexpected
        return f"Q-{latest_quote.id + 1001}" 