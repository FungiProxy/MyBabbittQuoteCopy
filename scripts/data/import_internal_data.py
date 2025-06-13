import json
from src.core.database import SessionLocal
from src.core.models.product_variant import ProductFamily
from src.core.models.voltage_option import VoltageOption
from src.core.models.material_option import MaterialOption
from src.core.models.option import Option

DATA_FILE = "data/internal_data_import.json"


def main():
    db = SessionLocal()
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    families = data.get("families", [])
    for fam in families:
        # Create or get ProductFamily
        pf = db.query(ProductFamily).filter_by(name=fam["name"]).first()
        if not pf:
            pf = ProductFamily(
                name=fam["name"],
                description=fam.get("base_model", {}).get("description", ""),
                category=None,
            )
            db.add(pf)
            db.commit()
            db.refresh(pf)
        # Import VoltageOption and MaterialOption using product_family_id
        for opt in fam.get("options", []):
            if opt["name"].lower() == "voltage":
                for v in opt.get("choices", []):
                    exists = (
                        db.query(VoltageOption)
                        .filter_by(product_family_id=pf.id, voltage=v)
                        .first()
                    )
                    if not exists:
                        db.add(
                            VoltageOption(
                                product_family_id=pf.id, voltage=v, is_available=1
                            )
                        )
            if opt["name"].lower() == "material":
                for m in opt.get("choices", []):
                    exists = (
                        db.query(MaterialOption)
                        .filter_by(product_family_id=pf.id, material_code=m)
                        .first()
                    )
                    if not exists:
                        db.add(
                            MaterialOption(
                                product_family_id=pf.id,
                                material_code=m,
                                display_name=m,
                                base_price=opt.get("adders", {}).get(m, 0),
                                is_available=1,
                            )
                        )
            # Import all options into Option table
            exists = (
                db.query(Option)
                .filter_by(name=opt["name"], product_families=fam["name"])
                .first()
            )
            if not exists:
                db.add(
                    Option(
                        name=opt["name"],
                        description=opt.get("notes", ""),
                        price=0.0,
                        price_type="fixed",
                        category=None,
                        product_families=fam["name"],
                        choices=opt.get("choices", []),
                        adders=opt.get("adders", {}),
                        rules=opt.get("rules", None),
                    )
                )
        db.commit()
    db.close()
    print("Import complete.")


if __name__ == "__main__":
    main()
