from src.core.database import SessionLocal
from src.core.models.option import Option

db = SessionLocal()
options = db.query(Option).filter(Option.product_families.like("%TRAN-EX%")).all()
for opt in options:
    print(f"NAME: {opt.name} | CATEGORY: {opt.category} | CHOICES: {opt.choices} | FAMILIES: {opt.product_families}")
db.close() 