#!/usr/bin/env python3
"""
Clear all special notes for all base models.
"""
from src.core.database import SessionLocal
from src.core.models.base_model import BaseModel

def clear_special_notes():
    db = SessionLocal()
    try:
        models = db.query(BaseModel).all()
        cleared = 0
        for m in models:
            if getattr(m, 'special_notes', None):
                m.special_notes = None
                cleared += 1
        if cleared:
            db.commit()
        print(f"Cleared special notes for {cleared} models.")
    finally:
        db.close()

if __name__ == "__main__":
    clear_special_notes() 