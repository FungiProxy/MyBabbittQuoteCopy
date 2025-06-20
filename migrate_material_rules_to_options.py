from src.core.database import SessionLocal
from src.core.models import Material, Option
import json

def migrate_material_rules_to_options():
    db = SessionLocal()
    try:
        # Get all materials from materials table
        materials = db.query(Material).all()
        print(f'Found {len(materials)} materials to migrate rules from:')
        
        updated_count = 0
        
        for material in materials:
            print(f'\n  {material.code}: {material.name}')
            
            # Find ALL material options that include this material code in their choices
            material_options = db.query(Option).filter(
                Option.category == 'Materials',
                Option.choices.contains([material.code])
            ).all()
            
            if not material_options:
                print(f'    ❌ No matching options found in options table')
                continue
                
            print(f'    ✅ Found {len(material_options)} matching options')
            
            # Create rules JSON with material pricing logic
            rules = {
                'length_adder_per_inch': material.length_adder_per_inch,
                'length_adder_per_foot': material.length_adder_per_foot,
                'nonstandard_length_surcharge': material.nonstandard_length_surcharge,
                'has_nonstandard_length_surcharge': material.has_nonstandard_length_surcharge,
                'base_length': material.base_length,
                'base_price_adder': material.base_price_adder
            }
            
            # Update the rules field for each matching option
            for option in material_options:
                print(f'      📝 Updating {option.product_families}: {option.choices}')
                
                # If rules already exist, merge with new rules
                if option.rules:
                    existing_rules = option.rules
                    # Add material-specific rules with material code as key
                    existing_rules[f'material_{material.code}'] = rules
                    option.rules = existing_rules
                else:
                    # Create new rules with material-specific key
                    option.rules = {f'material_{material.code}': rules}
                
                updated_count += 1
            
            print(f'    📋 Rules: {json.dumps(rules, indent=8)}')
        
        db.commit()
        print(f'\n✅ Successfully updated {updated_count} material options with pricing rules!')
        print('📋 Length adders and non-standard surcharge logic now stored in options table rules field.')
        
    except Exception as e:
        db.rollback()
        print(f'❌ Error migrating material rules: {e}')
        raise
    finally:
        db.close()

if __name__ == '__main__':
    migrate_material_rules_to_options() 