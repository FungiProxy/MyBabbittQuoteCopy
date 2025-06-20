"""
Database initialization orchestrator.
This script coordinates the initialization of both business configuration and sample data.
"""

from init_sample_data import init_sample_data

from scripts.data.init.init_business_config import init_business_config


def init_database():
    """Initialize the database with both business configuration and sample data."""
    print('Initializing database...')

    # First initialize business configuration
    print('\nInitializing business configuration...')
    init_business_config()

    # Then initialize sample data
    print('\nInitializing sample data...')
    init_sample_data()

    print('\nDatabase initialization complete!')


if __name__ == '__main__':
    init_database()
