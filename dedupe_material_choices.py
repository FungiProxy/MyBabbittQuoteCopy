#!/usr/bin/env python3

from src.core.database import SessionLocal
from src.core.models.option import Option


def dedupe_material_choices():
    db = SessionLocal()
    try:
        material_options = db.query(Option).filter(Option.category == 'Material').all()
        for opt in material_options:
            if not opt.choices or not isinstance(opt.choices, list):
                continue
            seen = set()
            deduped = []
            for choice in opt.choices:
                if isinstance(choice, dict):
                    code = choice.get('code')
                else:
                    code = choice
                if code and code not in seen:
                    seen.add(code)
                    deduped.append(choice)
            if len(deduped) != len(opt.choices):
                print(
                    f'Deduping Option ID {opt.id} ({opt.name}): {len(opt.choices)} -> {len(deduped)} choices'
                )
                opt.choices = deduped
        db.commit()
        print('Deduplication complete!')
    finally:
        db.close()


if __name__ == '__main__':
    dedupe_material_choices()
