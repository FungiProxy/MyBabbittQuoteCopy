"""
Options seed data.
This package contains seed data for all product options.
"""

from src.core.models.option import Option


def seed_options(db):
    """Seed all options in the database."""
    options = [
        Option(
            name='Extended Warranty',
            description='5-year extended warranty',
            price=500.0,
            price_type='fixed',
            category='Warranty',
        ),
        Option(
            name='Express Shipping',
            description='Next-day shipping',
            price=100.0,
            price_type='fixed',
            category='Shipping',
        ),
    ]
    db.add_all(options)
    db.commit()
    print(f'Added {len(options)} options')
