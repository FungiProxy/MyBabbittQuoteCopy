#!/usr/bin/env python3
"""
Complete the database migration to unified options structure.

This script works with the actual tables in your database to complete
the migration that was started but never finished.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.database import engine, get_db
from src.core.models import Option, ProductFamily
from sqlalchemy import text

def get_existing_tables():
    """Get list of tables that actually exist in the database."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        return [row[0] for row in result.fetchall()]

def clear_options_table():
    """Clear the existing options table."""
    print("Clearing existing options table...")
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM options"))
        conn.commit()

def migrate_materials():
    """Migrate materials from material_options table."""
    print("Migrating materials...")
    
    db = next(get_db())
    try:
        # Get all material options
        query = text("""
            SELECT DISTINCT material_code, display_name, base_price 
            FROM material_options 
            WHERE is_available = 1
            ORDER BY material_code
        """)
        
        result = db.execute(query)
        material_options = result.fetchall()
        
        # Group by material code
        materials = {}
        for row in material_options:
            code = row.material_code
            if code not in materials:
                materials[code] = {
                    'choices': [],
                    'adders': {},
                    'families': set()
                }
            
            materials[code]['choices'].append(code)
            materials[code]['adders'][code] = row.base_price or 0.0
        
        # Get product families for each material
        for code in materials:
            query = text("""
                SELECT DISTINCT pf.name 
                FROM material_options mo
                JOIN product_families pf ON mo.product_family_id = pf.id
                WHERE mo.material_code = :code AND mo.is_available = 1
            """)
            result = db.execute(query, {'code': code})
            families = [row[0] for row in result.fetchall()]
            materials[code]['families'] = families
        
        # Create unified material option
        if materials:
            all_choices = []
            all_adders = {}
            all_families = set()
            
            for code, data in materials.items():
                all_choices.extend(data['choices'])
                all_adders.update(data['adders'])
                all_families.update(data['families'])
            
            option = Option(
                name="Material",
                description="Material selection for the probe",
                price=0.0,
                price_type="fixed",
                category="material",
                product_families=",".join(sorted(all_families)),
                excluded_products="",
                choices=all_choices,
                adders=all_adders,
                rules=None
            )
            db.add(option)
            print(f"Created material option with {len(all_choices)} choices")
        
        db.commit()
        
    finally:
        db.close()

def migrate_voltages():
    """Migrate voltages from voltage_options table."""
    print("Migrating voltages...")
    
    db = next(get_db())
    try:
        # Get all voltage options
        query = text("""
            SELECT DISTINCT voltage 
            FROM voltage_options 
            WHERE is_available = 1
            ORDER BY voltage
        """)
        
        result = db.execute(query)
        voltage_options = result.fetchall()
        
        if voltage_options:
            choices = []
            adders = {}
            
            for row in voltage_options:
                voltage = row.voltage
                choices.append(voltage)
                adders[voltage] = 0.0  # No price adder for voltages
            
            # Get product family ids
            query = text("SELECT DISTINCT product_family_id FROM voltage_options WHERE is_available = 1")
            result = db.execute(query)
            family_ids = [row[0] for row in result.fetchall() if row[0] is not None]
            
            families = []
            for fid in family_ids:
                query = text("SELECT name FROM product_families WHERE id = :fid")
                result = db.execute(query, {'fid': fid})
                row = result.fetchone()
                if row:
                    families.append(row[0])
            
            option = Option(
                name="Voltage",
                description="Voltage configuration",
                price=0.0,
                price_type="fixed",
                category="voltage",
                product_families=",".join(sorted(families)),
                excluded_products="",
                choices=choices,
                adders=adders,
                rules=None
            )
            db.add(option)
            print(f"Created voltage option with {len(choices)} choices")
        
        db.commit()
        
    finally:
        db.close()

def migrate_connections():
    """Migrate connections from connection_options table."""
    print("Migrating connections...")
    
    db = next(get_db())
    try:
        # Get all connection options
        query = text("""
            SELECT DISTINCT type, rating, size, price 
            FROM connection_options 
            ORDER BY type, rating, size
        """)
        
        result = db.execute(query)
        connection_options = result.fetchall()
        
        if connection_options:
            choices = []
            adders = {}
            
            for row in connection_options:
                # Create choice name
                if row.rating:
                    choice = f"{row.type} {row.rating} {row.size}"
                else:
                    choice = f"{row.type} {row.size}"
                
                choices.append(choice)
                adders[choice] = row.price or 0.0
            
            # Get product family ids
            query = text("SELECT DISTINCT product_family_id FROM connection_options WHERE product_family_id IS NOT NULL")
            result = db.execute(query)
            family_ids = [row[0] for row in result.fetchall() if row[0] is not None]
            
            families = []
            for fid in family_ids:
                query = text("SELECT name FROM product_families WHERE id = :fid")
                result = db.execute(query, {'fid': fid})
                row = result.fetchone()
                if row:
                    families.append(row[0])
            
            option = Option(
                name="Connection",
                description="Connection type and size",
                price=0.0,
                price_type="fixed",
                category="connection",
                product_families=",".join(sorted(families)),
                excluded_products="",
                choices=choices,
                adders=adders,
                rules=None
            )
            db.add(option)
            print(f"Created connection option with {len(choices)} choices")
        
        db.commit()
        
    finally:
        db.close()

def create_probe_length_option():
    """Create probe length option."""
    print("Creating probe length option...")
    
    db = next(get_db())
    try:
        # Get all product families
        families = db.query(ProductFamily).all()
        family_names = [f.name for f in families]
        
        option = Option(
            name="Probe Length",
            description="Probe length in inches",
            price=0.0,
            price_type="per_inch",
            category="length",
            product_families=",".join(family_names),
            excluded_products="",
            choices=[],  # Dynamic based on user input
            adders={},   # Calculated based on length
            rules=None
        )
        db.add(option)
        print("Created probe length option")
        
        db.commit()
        
    finally:
        db.close()

def main():
    """Run the complete migration."""
    print("=== COMPLETING DATABASE MIGRATION ===")
    
    tables = get_existing_tables()
    print(f"Found {len(tables)} tables: {', '.join(sorted(tables))}")
    
    # Clear existing options
    clear_options_table()
    
    # Migrate each option type
    migrate_materials()
    migrate_voltages()
    migrate_connections()
    create_probe_length_option()
    
    # Verify results
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM options"))
        count = result.scalar()
        print(f"\nMigration complete! Created {count} unified options")
        
        # Show what was created
        result = conn.execute(text("SELECT name, category FROM options"))
        for row in result.fetchall():
            print(f"  - {row[0]} ({row[1]})")

if __name__ == "__main__":
    main() 