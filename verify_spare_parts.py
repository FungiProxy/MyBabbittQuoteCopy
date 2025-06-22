#!/usr/bin/env python3
"""
Verify and display the spare parts in the database.
"""

from src.core.database import SessionLocal
from src.core.models.spare_part import SparePart
from src.core.models.product_variant import ProductFamily

def verify_spare_parts():
    """Display all spare parts in the database with their details."""
    
    db = SessionLocal()
    
    try:
        # Get all spare parts with product family information
        spare_parts = db.query(SparePart).join(ProductFamily).all()
        
        print("SPARE PARTS IN DATABASE")
        print("=" * 80)
        print(f"Total spare parts: {len(spare_parts)}")
        print()
        
        # Group by product family
        families = {}
        for part in spare_parts:
            family_name = part.product_family.name
            if family_name not in families:
                families[family_name] = []
            families[family_name].append(part)
        
        # Display by family
        for family_name in sorted(families.keys()):
            print(f"\n{family_name} ({len(families[family_name])} parts):")
            print("-" * 50)
            
            for part in sorted(families[family_name], key=lambda x: x.part_number):
                category = part.category if part.category else "Uncategorized"
                print(f"  {part.part_number:<40} ${part.price:>8.2f}  [{category}]")
                print(f"    {part.name}")
                if part.description:
                    print(f"    Description: {part.description}")
                print()
        
        # Summary statistics
        print("SUMMARY STATISTICS")
        print("=" * 50)
        print(f"Total spare parts: {len(spare_parts)}")
        print(f"Product families with spare parts: {len(families)}")
        
        # Price statistics
        prices = [part.price for part in spare_parts]
        if prices:
            print(f"Average price: ${sum(prices) / len(prices):.2f}")
            print(f"Lowest price: ${min(prices):.2f}")
            print(f"Highest price: ${max(prices):.2f}")
        
        # Category statistics
        categories = {}
        for part in spare_parts:
            category = part.category if part.category else "Uncategorized"
            categories[category] = categories.get(category, 0) + 1
        
        print(f"\nParts by category:")
        for category, count in sorted(categories.items()):
            print(f"  {category}: {count} parts")
        
    except Exception as e:
        print(f"Error verifying spare parts: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_spare_parts() 