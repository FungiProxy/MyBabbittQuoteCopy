"""
Service for managing spare parts.

This module provides a service layer for managing spare parts in Babbitt International's
quoting system. It supports:
- Retrieving, searching, and categorizing spare parts
- Filtering by product family or category
- Handling spare part-related business logic

Follows domain-driven design and separates business logic from data access.
"""
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session

from src.core.models import SparePart, ProductFamily
from src.utils.db_utils import get_by_id, get_all


class SparePartService:
    """
    Service class for managing spare parts.
    
    Provides methods for retrieving, searching, and categorizing spare parts,
    including filtering by product family or category. Encapsulates all spare
    part-related business logic.
    
    Example:
        >>> db = SessionLocal()
        >>> all_parts = SparePartService.get_all_spare_parts(db)
        >>> electronics = SparePartService.get_spare_parts_by_category(db, category="electronics")
        >>> by_family = SparePartService.get_spare_parts_by_family(db, product_family_name="LS2000")
        >>> part = SparePartService.get_spare_part_by_part_number(db, part_number="SP-1001")
        >>> categories = SparePartService.get_spare_part_categories(db)
    """
    
    @staticmethod
    def get_all_spare_parts(db: Session) -> List[SparePart]:
        """
        Get all spare parts.
        
        Args:
            db: Database session
            
        Returns:
            List of all spare parts
        """
        return get_all(db, SparePart)
    
    @staticmethod
    def get_spare_parts_by_family(db: Session, product_family_name: str) -> List[SparePart]:
        """
        Get spare parts for a specific product family.
        
        Args:
            db: Database session
            product_family_name: Name of the product family
            
        Returns:
            List of matching spare parts
        """
        # Find the product family ID
        product_family = db.query(ProductFamily).filter(
            ProductFamily.name == product_family_name
        ).first()
        
        if not product_family:
            return []
            
        # Get spare parts for this family
        return db.query(SparePart).filter(
            SparePart.product_family_id == product_family.id
        ).all()
    
    @staticmethod
    def get_spare_parts_by_category(db: Session, category: str) -> List[SparePart]:
        """
        Get spare parts for a specific category.
        
        Args:
            db: Database session
            category: Category name (e.g., "electronics", "probe_assembly")
            
        Returns:
            List of matching spare parts
        """
        return db.query(SparePart).filter(
            SparePart.category == category
        ).all()
    
    @staticmethod
    def get_spare_part_by_part_number(db: Session, part_number: str) -> Optional[SparePart]:
        """
        Get a spare part by its part number.
        
        Args:
            db: Database session
            part_number: Part number to find
            
        Returns:
            SparePart object if found, None otherwise
        """
        return db.query(SparePart).filter(
            SparePart.part_number == part_number
        ).first()
    
    @staticmethod
    def get_spare_part_categories(db: Session) -> List[str]:
        """
        Get all spare part categories.
        
        Args:
            db: Database session
            
        Returns:
            List of distinct category names
        """
        categories = db.query(SparePart.category).distinct().all()
        return [category[0] for category in categories if category[0]] 