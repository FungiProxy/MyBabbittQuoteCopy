"""
Create database if needed.

This script checks if the database exists and has the necessary tables.
If not, it creates the database and populates it with initial data.

It can be run directly to create or update the database:
    python scripts/create_db_if_needed.py

It's also imported and used by the main application to ensure
the database exists when the application starts.
"""
import os
import sys
import logging
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from src.core.services.database_init import initialize_database_if_needed
from src.core.services.database_populate import populate_database


def create_database_if_needed():
    """Check if database exists and create it if needed."""
    try:
        # Initialize database if it doesn't exist or is missing tables
        created = initialize_database_if_needed()
        
        # If we created a new database, populate it with initial data
        if created:
            populate_database()
            logger.info("Database created and populated successfully.")
        else:
            logger.info("Database already exists with all required tables.")
            
        return True
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        return False


if __name__ == "__main__":
    # Run the create database function
    success = create_database_if_needed()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1) 