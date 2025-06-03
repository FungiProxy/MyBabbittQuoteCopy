import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.database import SessionLocal
from src.core.services.database_populate import populate_spare_parts
from src.core.models import SparePart

if __name__ == "__main__":
    db = SessionLocal()
    try:
        # Delete all existing spare parts
        deleted = db.query(SparePart).delete()
        db.commit()
        print(f"Deleted {deleted} existing spare parts.")
        # Repopulate with updated data
        populate_spare_parts(db)
        print("Spare parts repopulated successfully.")
    except Exception as e:
        print(f"Error during repopulation: {e}")
        db.rollback()
    finally:
        db.close() 