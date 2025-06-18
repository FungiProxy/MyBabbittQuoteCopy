"""
ConnectionOption model for managing specific connection configurations.

This module defines the ConnectionOption model which represents specific configurations
of connection types for products. It extends the base Connection model with additional
properties and specifications needed for product-specific configurations.

Supports:
- Product-specific connection configurations
- Connection specifications and dimensions
- Connection validation and constraints
"""

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlalchemy import Column, String, Boolean, JSON, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel as PydanticBaseModel, Field, validator

from src.core.models.base_model import BaseModel
from src.core.database import Base


class ConnectionOption(Base):
    """Model for connection options."""

    __tablename__ = "connection_options"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    connection_type = Column(String(50), nullable=False)
    rating = Column(String(20))
    size = Column(String(20))
    price = Column(Float, default=0.0)
    is_available = Column(Boolean, default=True)
    product_family_id = Column(Integer, ForeignKey("product_families.id"))
    connection_id = Column(Integer, ForeignKey("connections.id"))

    # Relationships
    product_family = relationship("ProductFamily", back_populates="connection_options")
    connection = relationship("Connection", back_populates="options")

    def __repr__(self):
        return f"<ConnectionOption(code='{self.code}', name='{self.name}', connection_type='{self.connection_type}', price={self.price})>"
