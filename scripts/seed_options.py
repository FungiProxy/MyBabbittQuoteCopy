import os
import sys

from sqlalchemy import text
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.core.models.option import Option


def seed_options(db: Session):
    """Seeds the database with product options."""

    options_data = [
        # O-Ring Materials
        {
            'name': 'Viton',
            'description': 'Viton O-ring',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'O-ring Material',
            'choices': ['Viton'],
            'adders': {},
        },
        {
            'name': 'Silicon',
            'description': 'Silicon O-ring',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'O-ring Material',
            'choices': ['Silicon'],
            'adders': {},
        },
        {
            'name': 'Buna-N',
            'description': 'Buna-N O-ring',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'O-ring Material',
            'choices': ['Buna-N'],
            'adders': {},
        },
        {
            'name': 'EPDM',
            'description': 'EPDM O-ring',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'O-ring Material',
            'choices': ['EPDM'],
            'adders': {},
        },
        {
            'name': 'PTFE',
            'description': 'PTFE O-ring',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'O-ring Material',
            'choices': ['PTFE'],
            'adders': {},
        },
        {
            'name': 'Kalrez',
            'description': 'Kalrez O-ring',
            'price': 295.0,
            'price_type': 'fixed',
            'category': 'O-ring Material',
            'choices': ['Kalrez'],
            'adders': {'Kalrez': 295.0},
        },
        # Exotic Metals
        {
            'name': 'None',
            'description': 'No exotic metal',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'Exotic Metal',
            'choices': ['None'],
            'adders': {},
        },
        {
            'name': 'Alloy 20',
            'description': 'Alloy 20 (Consult Factory)',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'Exotic Metal',
            'choices': ['Alloy 20'],
            'adders': {},
        },
        {
            'name': 'Hastelloy-C-276',
            'description': 'Hastelloy-C-276 (Consult Factory)',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'Exotic Metal',
            'choices': ['Hastelloy-C-276'],
            'adders': {},
        },
        {
            'name': 'Hastelloy-B',
            'description': 'Hastelloy-B (Consult Factory)',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'Exotic Metal',
            'choices': ['Hastelloy-B'],
            'adders': {},
        },
        {
            'name': 'Titanium',
            'description': 'Titanium (Consult Factory)',
            'price': 0.0,
            'price_type': 'fixed',
            'category': 'Exotic Metal',
            'choices': ['Titanium'],
            'adders': {},
        },
    ]

    for data in options_data:
        # Check if an option with the same name and category already exists
        exists = (
            db.query(Option)
            .filter_by(name=data['name'], category=data['category'])
            .first()
        )
        if not exists:
            option = Option(**data)
            db.add(option)

    db.commit()
    print('Successfully seeded product options.')


if __name__ == '__main__':
    db = SessionLocal()
    try:
        # For SQLite, it's helpful to enable foreign key constraints
        if db.bind.dialect.name == 'sqlite':
            db.execute(text('PRAGMA foreign_keys = ON;'))
        seed_options(db)
    finally:
        db.close()
