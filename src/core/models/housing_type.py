"""
HousingType model for storing available housing types.
"""

from sqlalchemy import Column, Integer, String
from ..database import Base


class HousingType(Base):
    """
    SQLAlchemy model representing a type of housing.

    Attributes:
        id (int): Primary key
        name (str): The name of the housing type (e.g., "Standard", "Explosion-Proof")
        description (str): A description of the housing type.
    """

    __tablename__ = "housing_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<HousingType(name='{self.name}')>"
