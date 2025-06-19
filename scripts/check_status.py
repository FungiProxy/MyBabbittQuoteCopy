from src.core.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    result = db.execute(text("SELECT COUNT(*) FROM options")).scalar()
    print(f"Options table still has {result} records")
except Exception as e:
    print("Options table does not exist - migration completed")

try:
    mech = db.execute(text("SELECT COUNT(*) FROM mechanical_options")).scalar()
    print(f"mechanical_options: {mech} records")
except:
    print("mechanical_options table does not exist yet")

db.close()
