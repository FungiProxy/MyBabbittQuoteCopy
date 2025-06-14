"""
Database initialization script to populate the database with sample data.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


from src.core.database import SessionLocal, init_db
from src.core.models.customer import Customer
from src.core.models.material import Material
from src.core.models.option import Option
from src.core.models.product_family import ProductFamily


def init_sample_data():
    """Initialize the database with sample data."""
    # Initialize database
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Add sample customers
        customers = [
            Customer(
                name="John Smith",
                company="ABC Manufacturing",
                email="john.smith@abcmfg.com",
                phone="555-0123",
                address="123 Industrial Way",
                city="Springfield",
                state="IL",
                zip_code="62701",
            ),
            Customer(
                name="Jane Doe",
                company="XYZ Industries",
                email="jane.doe@xyzind.com",
                phone="555-0124",
                address="456 Factory Lane",
                city="Riverside",
                state="CA",
                zip_code="92501",
            ),
        ]
        db.add_all(customers)

        # Add sample materials
        materials = [
            Material(
                code="BAB-001",
                name="Standard Babbitt",
                description="Standard grade Babbitt material",
                base_length=12.0,
                length_adder_per_inch=0.5,
                base_price_adder=100.0,
            ),
            Material(
                code="BAB-002",
                name="High-Performance Babbitt",
                description="High-performance grade Babbitt material",
                base_length=12.0,
                length_adder_per_inch=0.75,
                base_price_adder=150.0,
            ),
        ]
        db.add_all(materials)

        # Add sample product families
        product_families = [
            ProductFamily(
                name="Standard Bearings",
                description="Standard bearing product line",
                category="Bearings",
            ),
            ProductFamily(
                name="High-Performance Bearings",
                description="High-performance bearing product line",
                category="Bearings",
            ),
        ]
        db.add_all(product_families)

        # Add sample options
        options = [
            Option(
                name="Extended Warranty",
                description="5-year extended warranty",
                price=500.0,
                price_type="fixed",
                category="Warranty",
            ),
            Option(
                name="Express Shipping",
                description="Next-day shipping",
                price=100.0,
                price_type="fixed",
                category="Shipping",
            ),
        ]
        db.add_all(options)

        # Commit all changes
        db.commit()
        print("Sample data initialized successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error initializing sample data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_sample_data()
