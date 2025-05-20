"""
Database initialization service.
Handles checking if database exists and creating it if needed.
"""
import os
from pathlib import Path
import sqlite3
import logging

from src.core.database import SessionLocal, init_db, Base, engine
from sqlalchemy import inspect
from src.core.services.database_populate import remove_obsolete_products

# Set up logging
logger = logging.getLogger(__name__)

def check_database_exists():
    """Check if the database file exists."""
    data_dir = Path("data")
    db_path = data_dir / "quotes.db"
    return db_path.exists()

def check_tables_exist():
    """Check if the required database tables exist."""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Define the tables we expect to find
        expected_tables = [
            "materials",
            "standard_lengths",
            "product_families",
            "product_variants",
            "options",
            "customers",
            "quotes",
            "quote_items",
            "quote_item_options",
            "spare_parts"
        ]
        
        # Check if all expected tables exist
        for table in expected_tables:
            if table not in tables:
                logger.info(f"Missing table: {table}")
                return False
        
        return True
    except Exception as e:
        logger.error(f"Error checking tables: {str(e)}")
        return False

def create_database():
    """Create the database schema."""
    logger.info("Creating database schema...")
    init_db()
    logger.info("Database schema created.")

def ensure_obsolete_products_removed():
    """Ensure that ultrasonic and radar products are removed from the database."""
    db = SessionLocal()
    try:
        logger.info("Ensuring ultrasonic and radar products are removed...")
        remove_obsolete_products(db)
    except Exception as e:
        logger.error(f"Error removing obsolete products: {str(e)}")
    finally:
        db.close()

def initialize_database_if_needed():
    """Initialize the database if it doesn't exist."""
    try:
        # Check if database file exists
        if not check_database_exists():
            logger.info("Database file does not exist. Creating database...")
            create_database()
            return True
        
        # Check if tables exist
        if not check_tables_exist():
            logger.info("Database tables are missing. Initializing database...")
            create_database()
            return True
            
        # Database already exists and has tables
        logger.info("Database already exists with required tables.")
        
        # Even if database exists, ensure obsolete products are removed
        ensure_obsolete_products_removed()
            
        return False
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False 