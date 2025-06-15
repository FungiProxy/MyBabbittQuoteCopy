"""
Product variant seed data.
This package contains seed data for all product variants.
"""

from .ls2000_variants import seed_ls2000_variants
from .ls6000_variants import seed_ls6000_variants
from .ls7000_variants import seed_ls7000_variants
from .ls7000_2_variants import seed_ls7000_2_variants
from .ls8000_2_variants import seed_ls8000_2_variants


def seed_all_product_variants(db):
    """Seed all product variants in the database."""
    seed_ls2000_variants(db)
    seed_ls6000_variants(db)
    seed_ls7000_variants(db)
    seed_ls7000_2_variants(db)
    seed_ls8000_2_variants(db) 