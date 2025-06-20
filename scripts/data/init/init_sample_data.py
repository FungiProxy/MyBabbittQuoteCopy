"""
Database initialization script for sample/test data.
This includes development and testing data such as sample customers, product variants, and options.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scripts.data.seeds.customers import seed_customers
from scripts.data.seeds.options import seed_options
from scripts.data.seeds.product_variants import seed_all_product_variants
from src.core.database import SessionLocal, init_db


def init_sample_data():
    """Initialize the database with sample data for development and testing."""
    # Initialize database
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Seed product variants
        print("\nSeeding product variants...")
        seed_all_product_variants(db)

        # Seed options
        print("\nSeeding options...")
        seed_options(db)

        # Seed customers
        print("\nSeeding customers...")
        seed_customers(db)

        print("\nSample data initialized successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error initializing sample data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_sample_data()
