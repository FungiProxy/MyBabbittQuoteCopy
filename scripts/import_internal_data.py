import json
from pathlib import Path
from src.core.database import SessionLocal
from src.core.models import ProductFamily, Product, Option, SparePart
from sqlalchemy.orm import Session
import re

DATA_FILE = Path('data/internal_data_import.json')

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-').lower()

def infer_option_category(option_name):
    name = option_name.lower()
    if 'material' in name:
        return 'material'
    if 'mount' in name or 'flange' in name or 'tri-clamp' in name:
        return 'mounting'
    if 'length' in name:
        return 'length'
    if 'insulator' in name:
        return 'insulator'
    if 'probe' in name:
        return 'probe'
    if 'tag' in name:
        return 'tag'
    if 'enclosure' in name or 'housing' in name:
        return 'enclosure'
    if 'cable' in name:
        return 'cable'
    if 'card' in name:
        return 'electronics'
    return None

def import_internal_data(db: Session):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    families = data.get('families', [])
    for fam in families:
        # Create ProductFamily
        pf = ProductFamily(
            name=fam['name'],
            description=fam['base_model']['description'],
            category=fam.get('category', fam['name'])
        )
        db.add(pf)
        db.flush()  # Get pf.id
        # Create base Product (as canonical variant)
        bm = fam['base_model']
        product = Product(
            model_number=bm['model_number'],
            description=bm['description'],
            category=fam.get('category', fam['name']),
            base_price=bm['base_price'] or 0.0,
            base_length=bm.get('base_length'),
            voltage=bm.get('voltage'),
            material=bm.get('material')
        )
        db.add(product)
        db.flush()
        # Create Options
        used_categories = set()
        for opt in fam.get('options', []):
            base_category = opt.get('category') or infer_option_category(opt['name']) or 'feature'
            category = base_category
            suffix = 2
            # Ensure uniqueness of category within this family
            while category in used_categories:
                category = f"{base_category}_{suffix}"
                suffix += 1
            used_categories.add(category)
            option = Option(
                name=opt['name'],
                description=opt.get('notes'),
                choices=opt.get('choices'),
                adders=opt.get('adders'),
                rules=opt.get('rules'),
                category=category
            )
            db.add(option)
        # Create Spare Parts
        for sp in fam.get('spare_parts', []):
            part_number = slugify(sp['name'])
            spare = SparePart(
                part_number=part_number,
                name=sp['name'],
                description=sp.get('notes'),
                price=sp.get('price', 0.0),
                product_family_id=pf.id
            )
            db.add(spare)
        db.commit()
    print(f"Imported {len(families)} product families from {DATA_FILE}")

def main():
    db = SessionLocal()
    try:
        import_internal_data(db)
    finally:
        db.close()

if __name__ == '__main__':
    main() 