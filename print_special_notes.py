#!/usr/bin/env python3
"""
Print all special notes for base models.
"""
from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel

def print_special_notes():
    db = SessionLocal()
    try:
        print("=== SPECIAL NOTES PRESENT IN DATABASE ===\n")
        for m in db.query(BaseModel).all():
            notes = getattr(m, 'special_notes', None)
            if notes:
                print(f"{m.model_number}: {notes}\n")
    finally:
        db.close()

if __name__ == "__main__":
    print_special_notes() 