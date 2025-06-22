#!/usr/bin/env python3
"""
Populate the database with all spare parts from the JSON file.
This script only adds spare parts without modifying any other tables.
"""

import json
import os
from pathlib import Path

from src.core.database import SessionLocal
from src.core.models.spare_part import SparePart

def populate_spare_parts():
    """Populate the database with all spare parts from the JSON file."""
    
    # Load spare parts data from JSON file
    json_file_path = Path("data/spare_parts_db.json")
    
    if not json_file_path.exists():
        print(f"Error: Spare parts JSON file not found at {json_file_path}")
        return
    
    try:
        with open(json_file_path, 'r') as f:
            spare_parts_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return
    
    print(f"Loaded {len(spare_parts_data)} spare parts from JSON file")
    
    # Connect to database
    db = SessionLocal()
    
    try:
        # Check if spare parts already exist
        existing_count = db.query(SparePart).count()
        if existing_count > 0:
            print(f"Warning: Database already contains {existing_count} spare parts")
            response = input("Do you want to continue and add more? (y/N): ")
            if response.lower() != 'y':
                print("Operation cancelled.")
                return
        
        # Process each spare part
        added_count = 0
        skipped_count = 0
        
        for part_data in spare_parts_data:
            # Check if this part number already exists
            existing_part = db.query(SparePart).filter(
                SparePart.part_number == part_data["part_number"]
            ).first()
            
            if existing_part:
                print(f"Skipping existing part: {part_data['part_number']}")
                skipped_count += 1
                continue
            
            # Create new spare part
            spare_part = SparePart(
                part_number=part_data["part_number"],
                name=part_data["name"],
                description=part_data.get("description"),
                price=part_data["price"],
                product_family_id=part_data["product_family_id"],
                category=part_data.get("category")
            )
            
            db.add(spare_part)
            added_count += 1
            print(f"Added: {part_data['part_number']} - {part_data['name']}")
        
        # Commit all changes
        db.commit()
        
        print(f"\nSpare parts population completed!")
        print(f"Added: {added_count} new spare parts")
        print(f"Skipped: {skipped_count} existing spare parts")
        print(f"Total spare parts in database: {db.query(SparePart).count()}")
        
        # Show summary by product family
        print("\nSummary by product family:")
        families = db.query(SparePart.product_family_id).distinct().all()
        for family_id in families:
            count = db.query(SparePart).filter(
                SparePart.product_family_id == family_id[0]
            ).count()
            print(f"  Family ID {family_id[0]}: {count} parts")
        
    except Exception as e:
        print(f"Error populating spare parts: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_spare_parts() 