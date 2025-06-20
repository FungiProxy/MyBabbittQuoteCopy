import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.core.database import SessionLocal
from src.core.models.material_option import MaterialOption
from src.core.models.product_variant import ProductFamily

# Standard adders for each material code
STANDARD_ADDERS = {
    "S": 0.0,  # 316 Stainless Steel
    "H": 110.0,  # Halar Coated
    "TS": 110.0,  # Teflon Sleeve
    "U": 20.0,  # UHMWPE Blind End
    "T": 60.0,  # Teflon Blind End
    "C": 80.0,  # Cable
    "CPVC": 400.0,  # CPVC Blind End
}


def update_material_adders():
    db = SessionLocal()
    try:
        families = db.query(ProductFamily).all()
        for fam in families:
            print(f"Processing {fam.name} (ID: {fam.id})")
            options = db.query(MaterialOption).filter_by(product_family_id=fam.id).all()
            for opt in options:
                code = opt.material_code
                if code in STANDARD_ADDERS:
                    old_price = opt.base_price
                    opt.base_price = STANDARD_ADDERS[code]
                    print(f"  [UPDATE] {code}: {old_price} -> {opt.base_price}")
        db.commit()
        print("Material adders updated for all product families.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    update_material_adders()
