#!/usr/bin/env python3
"""
Fix Material Options in Database
Ensures only one Material option per family, with exotic metals included in choices/adders.
"""

from src.core.database import SessionLocal
from src.core.models import Option, ProductFamily

def fix_material_options():
    db = SessionLocal()
    try:
        print("🔧 Fixing material options in database...")

        # Define all possible material codes
        exotic_codes = ['A', 'HC', 'HB', 'TT']
        exotic_names = {
            'A': 'Alloy 20',
            'HC': 'Hastelloy-C-276',
            'HB': 'Hastelloy-B',
            'TT': 'Titanium',
        }
        # Standard material codes for each family
        material_config = {
            'LS2000': ['S', 'H', 'TS', 'U', 'T', 'C'],
            'LS2100': ['S', 'H', 'TS', 'U', 'T', 'C'],
            'LS6000': ['S', 'H', 'TS', 'U', 'T', 'C', 'CPVC'],
            'LS7000': ['S', 'H', 'TS', 'U', 'T', 'CPVC', 'C'],
            'LS7000/2': ['H', 'TS'],
            'LS8000': ['S', 'H', 'TS', 'C'],
            'LS8000/2': ['H', 'TS'],
            'LT9000': ['H', 'TS'],
            'FS10000': ['S'],
            'LS7500': ['S'],
            'LS8500': ['S'],
        }
        # Add exotic metals to each family (if not already present)
        for fam in material_config:
            if fam == 'LS7000' and 'C' not in material_config[fam]:
                material_config[fam].append('C')
            material_config[fam] = material_config[fam] + exotic_codes
        # Adders for all materials (exotic metals = 0)
        base_adders = {
            'S': 0, 'H': 110, 'TS': 110, 'U': 20, 'T': 60, 'C': 80, 'CPVC': 400,
            'A': 0, 'HC': 0, 'HB': 0, 'TT': 0
        }
        # Remove all Material and Exotic Metal options
        n_material = db.query(Option).filter(Option.category.in_(['Material', 'Materials', 'Exotic Metal'])).delete(synchronize_session=False)
        db.commit()
        print(f"🗑️  Removed {n_material} old material/exotic options.")
        # Get all product families
        product_families = db.query(ProductFamily).all()
        family_map = {pf.name: pf.id for pf in product_families}
        # Add one Material option per family
        for fam, codes in material_config.items():
            if fam in family_map:
                # Only include adders for codes present in this family
                adders = {code: base_adders[code] for code in codes if code in base_adders}
                option = Option(
                    name='Material',
                    description='Probe material selection (including exotic metals)',
                    price=0.0,
                    price_type='fixed',
                    category='Material',
                    choices=codes,
                    adders=adders,
                    product_families=fam,
                    excluded_products=None,
                    rules=None
                )
                db.add(option)
                print(f"  ✅ Added Material option for {fam}: {codes}")
        db.commit()
        print("\n✅ Material options fixed: one per family, with exotic metals included.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error fixing material options: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_material_options() 