"""
Update database with new tables.

This script updates the existing database to add any missing tables.
It's specifically designed to add the spare_parts table.
"""
import os
import sys
import traceback
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.database import engine, Base, SessionLocal
from src.core.models import SparePart, ProductFamily  # Make sure SparePart is imported
from src.core.services.database_populate import populate_spare_parts, populate_from_price_list

def update_database():
    """Update database with new tables."""
    print("Updating database with new tables...")
    
    try:
        # Create all tables before populating
        Base.metadata.create_all(bind=engine)
        print("All tables created.")
        
        # Populate the product families and spare parts data
        db = SessionLocal()
        try:
            print("Populating product families...")
            populate_from_price_list(db)  # Ensure product families are present
            print("Populating spare parts...")
            populate_spare_parts(db)
            
            # Verify data was inserted
            parts_count = db.query(SparePart).count()
            print(f"Spare parts count after population: {parts_count}")
            
            if parts_count > 0:
                # Get LS2000 and LS2100 product family IDs
                ls2000 = db.query(ProductFamily).filter(ProductFamily.name == "LS2000").first()
                ls2100 = db.query(ProductFamily).filter(ProductFamily.name == "LS2100").first()
                
                if ls2000:
                    ls2000_parts = db.query(SparePart).filter(SparePart.product_family_id == ls2000.id).all()
                    print(f"\nLS2000 parts count: {len(ls2000_parts)}")
                    for part in ls2000_parts:
                        print(f"  - {part.part_number} ({part.name})")
                
                if ls2100:
                    ls2100_parts = db.query(SparePart).filter(SparePart.product_family_id == ls2100.id).all()
                    print(f"\nLS2100 parts count: {len(ls2100_parts)}")
                    for part in ls2100_parts:
                        print(f"  - {part.part_number} ({part.name})")
                
                print("\nSample of all spare parts:")
                parts = db.query(SparePart).limit(5).all()
                for part in parts:
                    print(f"  - {part.part_number} (Family ID: {part.product_family_id})")
            else:
                print("WARNING: No spare parts were added!")
                
            print("Spare parts data populated.")
        except Exception as e:
            print(f"Error populating spare parts: {e}")
            print(traceback.format_exc())
        finally:
            db.close()
        
        print("Database update completed.")
    except Exception as e:
        print(f"Error updating database: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    update_database()
