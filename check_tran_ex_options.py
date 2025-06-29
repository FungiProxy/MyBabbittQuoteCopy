from src.core.database import SessionLocal
from src.core.models.option import Option

db = SessionLocal()
options = db.query(Option).filter(Option.product_families.like("%TRAN-EX%")).all()
for opt in options:
    print(f"{opt.name} | {opt.category} | {opt.choices}")
db.close() 