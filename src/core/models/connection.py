"""
Connection model for storing core connection types and properties.

This module defines the base Connection model for Babbitt International's quoting system.
It stores the core connection types and their fundamental properties, which are then
used by ConnectionOption to create specific product configurations.

Supports:
- Core connection types (Flange, Tri-Clamp)
- Connection properties and specifications
- Connection validation and constraints
"""

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlalchemy import Column, String, Boolean, JSON, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel


class Connection(BaseModel):
    """
    SQLAlchemy model representing a core connection type.

    This is the base model for all connection types in the system. It defines
    the fundamental properties and specifications of a connection type, which
    are then used to create specific connection options for products.

    Attributes:
        id (int): Primary key
        code (str): Unique connection code (e.g., "FL", "TC")
        name (str): Full connection name (e.g., "Flange", "Tri-Clamp")
        description (str): Detailed description
        created_at (datetime): Timestamp of creation
        updated_at (datetime): Timestamp of last update
        is_active (bool): Whether the connection type is currently active
        sort_order (int): Display order in UI
        specifications (Dict): Technical specifications
        options (List[ConnectionOption]): Related connection options
    """

    __tablename__ = "connections"

    # Core fields
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # Properties
    specifications = Column(JSON, nullable=True)

    # Relationships
    options = relationship("ConnectionOption", back_populates="connection")

    @validator("code")
    def validate_code(cls, v):
        """Validate connection code format."""
        if not v or len(v) > 10:
            raise ValueError("Connection code must be between 1 and 10 characters")
        return v.upper()

    @validator("name")
    def validate_name(cls, v):
        """Validate connection name."""
        if not v or len(v) > 50:
            raise ValueError("Connection name must be between 1 and 50 characters")
        return v

    def get_specification(self, key: str, default: any = None) -> any:
        """Get a specific technical specification value."""
        if not self.specifications:
            return default
        return self.specifications.get(key, default)

    def get_display_name(self) -> str:
        """Get a formatted display name for the connection type."""
        return f"{self.name} ({self.code})"

    def __repr__(self):
        """Return a string representation of the Connection."""
        return f"<Connection(code='{self.code}', name='{self.name}')>"
