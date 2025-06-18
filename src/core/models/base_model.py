"""
Base model with common fields for all models.

This module defines the BaseModel class which provides common fields and functionality
for all models in the application. It includes:
- Common fields (id, created_at, updated_at)
- Common methods (__repr__, to_dict)
- Validation and error handling
"""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr

from src.core.database import Base


class BaseModel(Base):
    """
    Base model class with common fields and functionality.

    This class provides common fields and methods that all models should have.
    It includes:
    - Common fields (id, created_at, updated_at)
    - Common methods (__repr__, to_dict)
    - Validation and error handling

    Attributes:
        id (int): Primary key
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp

    Example:
        >>> class MyModel(BaseModel):
        ...     __tablename__ = 'my_table'
        ...     name = Column(String)
        >>> model = MyModel(name='test')
        >>> print(model.to_dict())
    """

    # Make this an abstract base class
    __abstract__ = True

    # Common fields
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically based on class name.

        Returns:
            str: Table name in snake_case
        """
        return cls.__name__.lower()

    def __repr__(self) -> str:
        """
        Return a string representation of the model.

        Returns:
            str: A string showing the model's class name and ID
        """
        return f"<{self.__class__.__name__}(id={self.id})>"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the model
        """
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def update(self, **kwargs: Any) -> None:
        """
        Update model attributes.

        Args:
            **kwargs: Attributes to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
