#!/usr/bin/env python3
"""
Update option category names to be more descriptive and specific.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.option import Option


def update_category_names():
    """Update option category names to be more descriptive."""
    print("=== UPDATING OPTION CATEGORY NAMES ===")
    
    # Define the category name mappings
    category_mappings = {
        'Electrical': 'Voltages',
        'Mechanical': 'Connections', 
        'Material': 'Materials',
        'Exotic Metal': 'Exotic Metals',
        'O-ring Material': 'O-Ring Materials'
    }
    
    # Additional category for accessories
    accessories_options = [
        'Bent Probe',
        'Stainless Steel Tag', 
        '3/4" Diameter Probe',
        'NEMA 4 Enclosure',
        'GRK Exp Proof Enclosure',
        'Extra Static Protection',
        'Twisted Shielded Pair',
        'Additional Coaxial Cable'
    ]
    
    db = SessionLocal()
    try:
        # Show what will be changed
        print("Category name mappings:")
        for old_name, new_name in category_mappings.items():
            count = db.query(Option).filter_by(category=old_name).count()
            print(f"  '{old_name}' → '{new_name}' ({count} options)")
        
        # Show accessories that will be moved
        accessories_count = db.query(Option).filter(Option.name.in_(accessories_options)).count()
        print(f"  Moving {accessories_count} options to new 'Accessories' category")
        
        # Confirm before proceeding
        print(f"\nAbout to update {len(category_mappings)} categories and create 1 new category.")
        response = input("Proceed with updates? (y/N): ").strip().lower()
        if response != 'y':
            print("Update cancelled.")
            return
        
        # Update existing categories
        print("\nUpdating category names...")
        for old_name, new_name in category_mappings.items():
            options = db.query(Option).filter_by(category=old_name).all()
            for option in options:
                option.category = new_name
            print(f"  ✅ Updated {len(options)} options: '{old_name}' → '{new_name}'")
        
        # Move accessories to new category
        print("\nMoving accessories to new category...")
        accessories = db.query(Option).filter(Option.name.in_(accessories_options)).all()
        for option in accessories:
            option.category = 'Accessories'
        print(f"  ✅ Moved {len(accessories)} options to 'Accessories' category")
        
        # Commit changes
        db.commit()
        print("\n✅ All category updates completed successfully!")
        
        # Show final category structure
        print("\n=== FINAL CATEGORY STRUCTURE ===")
        categories = db.query(Option.category).distinct().all()
        for cat in sorted(categories):
            count = db.query(Option).filter_by(category=cat[0]).count()
            print(f"  {cat[0]}: {count} options")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating categories: {e}")
        raise
    finally:
        db.close()


def verify_category_updates():
    """Verify that the category updates were successful."""
    print("\n=== VERIFICATION ===")
    
    db = SessionLocal()
    try:
        # Check final categories
        categories = db.query(Option.category).distinct().all()
        print(f"Total categories: {len(categories)}")
        
        expected_categories = ['Materials', 'Voltages', 'Connections', 'O-Ring Materials', 'Exotic Metals', 'Accessories']
        
        print("\nCategory verification:")
        for cat in sorted(categories):
            count = db.query(Option).filter_by(category=cat[0]).count()
            status = "✅" if cat[0] in expected_categories else "⚠️"
            print(f"  {status} {cat[0]}: {count} options")
        
        # Check for any remaining old category names
        old_categories = ['Electrical', 'Mechanical', 'Material', 'Exotic Metal', 'O-ring Material']
        print("\nChecking for old category names:")
        for old_cat in old_categories:
            count = db.query(Option).filter_by(category=old_cat).count()
            if count > 0:
                print(f"  ❌ Found {count} options still using old category '{old_cat}'")
            else:
                print(f"  ✅ No options using old category '{old_cat}'")
                
    finally:
        db.close()


def main():
    """Run the category name updates."""
    print("OPTION CATEGORY NAME UPDATES")
    print("=" * 50)
    
    update_category_names()
    verify_category_updates()
    
    print("\n" + "=" * 50)
    print("CATEGORY UPDATES COMPLETE")
    print("=" * 50)


if __name__ == '__main__':
    main() 