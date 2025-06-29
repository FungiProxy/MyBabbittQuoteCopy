from src.core.database import SessionLocal
from src.core.models.product import Product

db = SessionLocal()

# Check if TRAN-EX base product already exists
tran_ex_product = db.query(Product).filter(Product.model_number == "LS8000/2-TRAN-EX-S-10").first()
if not tran_ex_product:
    tran_ex_product = Product(
        model_number="LS8000/2-TRAN-EX-S-10",
        description="TRAN-EX base product for LS8000/2 family (fixed 115VAC, S/H material only)",
        category="Multi-Point Level Switch",
        base_price=540.0,
        base_length=10,
        voltage="115VAC",
        material="S"
    )
    db.add(tran_ex_product)
    db.commit()
    print("Created TRAN-EX base product: LS8000/2-TRAN-EX-S-10 with base price $540.00")
else:
    print("TRAN-EX base product already exists.")

db.close() 