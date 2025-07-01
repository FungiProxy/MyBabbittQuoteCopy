#!/usr/bin/env python3
"""
Script to fix Insulator Material option:
- Remove 'Standard' from choices
- Change 'Teflon Upgrade' to 'Teflon'
"""
from src.core.database import SessionLocal
from src.core.models.option import Option

def main():
    db = SessionLocal()
    option = db.query(Option).filter_by(name='Insulator Material').first()
    if not option:
        print('Insulator Material option not found!')
        return
    print('Before:', option.choices)
    # Fix choices
    new_choices = []
    for c in option.choices:
        if isinstance(c, dict):
            name = c.get('display_name', c.get('code', str(c)))
            if name == 'Standard':
                continue
            if name == 'Teflon Upgrade':
                c['display_name'] = 'Teflon'
                c['code'] = 'Teflon'
            new_choices.append(c)
        else:
            if c == 'Standard':
                continue
            if c == 'Teflon Upgrade':
                new_choices.append('Teflon')
            else:
                new_choices.append(c)
    option.choices = new_choices
    db.add(option)
    db.commit()
    db.refresh(option)
    print('After:', option.choices)
    db.close()

if __name__ == '__main__':
    main() 