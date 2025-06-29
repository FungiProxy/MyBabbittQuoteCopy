from src.core.database import SessionLocal
from src.core.models.option import Option

db = SessionLocal()

# Check if Probe Length already exists for TRAN-EX
existing = db.query(Option).filter_by(name="Probe Length", product_families="TRAN-EX").first()
if not existing:
    probe_length_option = Option(
        name="Probe Length",
        description="Probe length in inches",
        price=0.0,
        price_type="fixed",
        category="Mechanical",
        choices=[str(x) for x in [10, 12, 18, 24, 36, 48, 60, 72, 84, 96, 108, 120]],
        adders={},
        product_families="TRAN-EX"
    )
    db.add(probe_length_option)
    db.commit()
    print("Added Probe Length option for TRAN-EX.")
else:
    print("Probe Length option for TRAN-EX already exists.")

db.close() 