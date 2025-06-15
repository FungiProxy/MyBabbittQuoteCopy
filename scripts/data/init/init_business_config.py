"""
Database initialization script for business configuration data.
This includes essential business rules, materials, standard lengths, and pricing configurations.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.database import SessionLocal, init_db
from scripts.data.config.connections import init_connection_options
from scripts.data.config.insulation import init_insulation_options
from scripts.data.config.insulation_application_notes import init_insulation_application_notes
from scripts.data.config.insulation_temperature_limits import init_insulation_temperature_limits
from scripts.data.config.materials import init_material_options
from scripts.data.config.misc_options import init_misc_options
from scripts.data.config.product_families import init_product_families
from scripts.data.config.standard_lengths import init_standard_lengths
from scripts.data.config.voltages import init_voltage_options


def init_business_config():
    """Initialize the database with essential business configuration data."""
    # Initialize database
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Initialize product families
        print("\nInitializing product families...")
        init_product_families(db)

        # Initialize material options
        print("\nInitializing material options...")
        init_material_options(db)

        # Initialize connection options
        print("\nInitializing connection options...")
        init_connection_options(db)

        # Initialize insulation options
        print("\nInitializing insulation options...")
        init_insulation_options(db)

        # Initialize insulation application notes
        print("\nInitializing insulation application notes...")
        init_insulation_application_notes(db)

        # Initialize insulation temperature limits
        print("\nInitializing insulation temperature limits...")
        init_insulation_temperature_limits(db)

        # Initialize voltage options
        print("\nInitializing voltage options...")
        init_voltage_options(db)

        # Initialize standard lengths
        print("\nInitializing standard lengths...")
        init_standard_lengths(db)

        # Initialize miscellaneous options
        print("\nInitializing miscellaneous options...")
        init_misc_options(db)

        # Commit all changes
        db.commit()
        print("\nBusiness configuration data initialized successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error initializing business configuration data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_business_config() 