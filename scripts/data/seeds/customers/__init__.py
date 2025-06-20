"""
Customer seed data.
This package contains seed data for development and testing customers.
"""

from src.core.models.customer import Customer


def seed_customers(db):
    """Seed development and testing customers in the database."""
    customers = [
        Customer(
            name='John Smith',
            company='ABC Manufacturing',
            email='john.smith@abcmfg.com',
            phone='555-0123',
            address='123 Industrial Way',
            city='Springfield',
            state='IL',
            zip_code='62701',
        ),
        Customer(
            name='Jane Doe',
            company='XYZ Industries',
            email='jane.doe@xyzind.com',
            phone='555-0124',
            address='456 Factory Lane',
            city='Riverside',
            state='CA',
            zip_code='92501',
        ),
    ]
    db.add_all(customers)
    db.commit()
    print(f'Added {len(customers)} customers')
