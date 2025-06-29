from src.core.database import SessionLocal
from src.core.models.option import Option

db = SessionLocal()
seen = set()
duplicates = []

options = db.query(Option).filter(Option.product_families.like("%TRAN-EX%")).all()
for opt in options:
    key = (opt.name, opt.category)
    if key in seen:
        print(f"Deleting duplicate: {opt.name} | {opt.category} | {opt.choices}")
        duplicates.append(opt)
    else:
        seen.add(key)

for dup in duplicates:
    db.delete(dup)
db.commit()
print(f"Removed {len(duplicates)} duplicate options for TRAN-EX.")

db.close() 