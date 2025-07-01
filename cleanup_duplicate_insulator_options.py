#!/usr/bin/env python3
"""
Script to remove duplicate/legacy 'Insulator Material' options.
Keeps only the correct one with choices as dicts (with 'code' and 'display_name').
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.core.models.option import Option

def main():
    db = SessionLocal()
    try:
        print("=== BEFORE CLEANUP ===")
        options = db.query(Option).filter(Option.name == 'Insulator Material').all()
        for opt in options:
            print(f"ID: {opt.id}, Choices: {opt.choices}")
        
        # Identify the correct option (choices as list of dicts with 'code' and 'display_name')
        correct_option = None
        for opt in options:
            if (
                isinstance(opt.choices, list)
                and len(opt.choices) > 0
                and isinstance(opt.choices[0], dict)
                and 'code' in opt.choices[0]
                and 'display_name' in opt.choices[0]
            ):
                correct_option = opt
                break
        
        # Delete all other Insulator Material options
        deleted_count = 0
        for opt in options:
            if correct_option and opt.id == correct_option.id:
                continue
            print(f"Deleting legacy/duplicate Insulator Material option ID: {opt.id}")
            db.delete(opt)
            deleted_count += 1
        
        db.commit()
        print(f"Deleted {deleted_count} duplicate/legacy options.")
        
        print("\n=== AFTER CLEANUP ===")
        options = db.query(Option).filter(Option.name == 'Insulator Material').all()
        for opt in options:
            print(f"ID: {opt.id}, Choices: {opt.choices}")
        if len(options) == 1:
            print("SUCCESS: Only the correct Insulator Material option remains.")
        else:
            print("WARNING: More than one Insulator Material option remains!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 