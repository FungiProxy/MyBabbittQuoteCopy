#!/usr/bin/env python3
"""
Check all options and their associated product families, focusing on LT9000.
"""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.option import Option


def print_options_by_family(family_name):
    db = SessionLocal()
    try:
        print(f'\n🔍 Options for product family: {family_name}')
        options = (
            db.query(Option)
            .filter(Option.product_families.like(f'%{family_name}%'))
            .all()
        )
        if not options:
            print('❌ No options found for this family.')
        for opt in options:
            print(
                f'- {opt.name} (category: {opt.category}) choices: {opt.choices} adders: {opt.adders}'
            )
    finally:
        db.close()


if __name__ == '__main__':
    print_options_by_family('LT9000')
