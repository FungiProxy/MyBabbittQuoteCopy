#!/usr/bin/env python3
"""
Add missing length adder rules for U and T materials
"""

import json
from src.core.database import engine
from sqlalchemy import text

def add_missing_length_adders():
    """Add missing length adder rules for U and T materials"""
    try:
        print("=== ADDING MISSING LENGTH ADDERS ===")
        
        # Define the missing length adder rules
        missing_rules = [
            # LS6000 - U and T materials
            ("LS6000", "U", "per_inch", 4.0, 40.0, "$40 per inch starting at 5\""),
            ("LS6000", "T", "per_inch", 4.0, 50.0, "$50 per inch starting at 5\""),
            
            # LS7000 - U and T materials  
            ("LS7000", "U", "per_inch", 4.0, 40.0, "$40 per inch starting at 5\""),
            ("LS7000", "T", "per_inch", 4.0, 50.0, "$50 per inch starting at 5\""),
            
            # LS8000 - U and T materials
            ("LS8000", "U", "per_inch", 4.0, 40.0, "$40 per inch starting at 5\""),
            ("LS8000", "T", "per_inch", 4.0, 50.0, "$50 per inch starting at 5\"")
        ]
        
        # Connect to database
        with engine.connect() as conn:
            print("\n1. Adding missing length adder rules...")
            
            for rule in missing_rules:
                product_family, material_code, adder_type, first_threshold, adder_amount, description = rule
                
                print(f"   Adding: {product_family} - {material_code} - {adder_type} - ${adder_amount}")
                
                # Check if rule already exists
                result = conn.execute(
                    text("SELECT id FROM length_adder_rules WHERE product_family = :family AND material_code = :material"),
                    {"family": product_family, "material": material_code}
                )
                existing = result.fetchone()
                
                if existing:
                    print(f"     ⚠ Rule already exists (ID: {existing[0]})")
                else:
                    # Insert new rule
                    conn.execute(
                        text("""
                            INSERT INTO length_adder_rules 
                            (product_family, material_code, adder_type, first_threshold, adder_amount, description)
                            VALUES (:family, :material, :type, :threshold, :amount, :desc)
                        """),
                        {
                            "family": product_family,
                            "material": material_code,
                            "type": adder_type,
                            "threshold": first_threshold,
                            "amount": adder_amount,
                            "desc": description
                        }
                    )
                    print(f"     ✓ Added new rule")
            
            # Commit changes
            conn.commit()
            print("\n2. All changes committed successfully!")
            
            # Verify the additions
            print("\n3. Verifying the additions...")
            result = conn.execute(text("SELECT * FROM length_adder_rules WHERE material_code IN ('U', 'T') ORDER BY product_family, material_code"))
            rows = result.fetchall()
            
            print(f"Found {len(rows)} U and T length adder rules:")
            for row in rows:
                rule_id, family, material, adder_type, threshold, amount, desc = row
                print(f"  {rule_id}: {family} - {material} - {adder_type} - ${amount} at {threshold}\" - {desc}")
            
            print("\n=== MISSING LENGTH ADDERS ADDED ===")
            
    except Exception as e:
        print(f"Error adding missing length adders: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_missing_length_adders() 