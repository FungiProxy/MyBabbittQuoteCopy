"""
Database initialization script.
"""

from src.core.services.database import DatabaseService
from scripts.data.config.product_families import initialize_product_families
from scripts.data.config.materials import initialize_materials
from scripts.data.config.connections import initialize_connections
from scripts.data.config.voltages import initialize_voltages
from scripts.data.config.standard_lengths import initialize_standard_lengths
from scripts.data.config.misc_options import initialize_misc_options


def initialize_database():
    """Initialize the database with all required data."""

    # Create database service
    db = DatabaseService()

    # Initialize product families
    print("Initializing product families...")
    initialize_product_families(db)

    # Initialize materials
    print("Initializing materials...")
    initialize_materials(db)

    # Initialize connections
    print("Initializing connections...")
    initialize_connections(db)

    # Initialize voltages
    print("Initializing voltages...")
    initialize_voltages(db)

    # Initialize standard lengths
    print("Initializing standard lengths...")
    initialize_standard_lengths(db)

    # Initialize miscellaneous options
    print("Initializing miscellaneous options...")
    initialize_misc_options(db)

    print("Database initialization complete!")


if __name__ == "__main__":
    initialize_database()
