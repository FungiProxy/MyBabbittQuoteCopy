import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.core.models.option import Option


def cleanup_and_verify_ls6000_options():
    """Remove all LS6000 options, reseed, and print for verification."""
    db = SessionLocal()
    try:
        # Remove all options where product_families includes LS6000
        deleted = db.query(Option).filter(Option.product_families.like('%LS6000%'))
        count = deleted.count()
        deleted.delete(synchronize_session=False)
        db.commit()
        print(f'Deleted {count} LS6000 options.')

        # Reseed using the main seed_options.py
        from scripts.seed_options import seed_options

        seed_options(db)
        print('Reseeded LS6000 options using seed_options.py.')

        # Print all LS6000 options for verification
        options = db.query(Option).filter(Option.product_families.like('%LS6000%'))
        print(f'\nCurrent LS6000 options ({options.count()}):')
        for opt in options:
            print(
                f'- {opt.name} (Category: {opt.category}) Choices: {opt.choices} Adders: {opt.adders}'
            )
    finally:
        db.close()


if __name__ == '__main__':
    cleanup_and_verify_ls6000_options()
