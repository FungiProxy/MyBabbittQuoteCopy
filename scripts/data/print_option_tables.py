from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.core.models.product_variant import ProductFamily


def print_options():
    db = SessionLocal()
    ps = ProductService()
    families = db.query(ProductFamily).all()
    if not families:
        print("No product families found.")
        return
    for fam in families:
        print(f"\nProduct Family: {fam.name} (ID: {fam.id})")
        voltage = ps.get_voltage_options(db, fam.id)
        material = ps.get_material_options(db, fam.id)
        connection = ps.get_connection_options(db, fam.id)
        additional = ps.get_additional_options(db, fam.name)
        conn_labels = (
            [f"{c['type']} {c['size']} {c['rating']}" for c in connection]
            if connection
            else "None"
        )
        print(
            f"  Voltage Options: {[v['voltage'] for v in voltage] if voltage else 'None'}"
        )
        print(
            f"  Material Options: {[m['display_name'] for m in material] if material else 'None'}"
        )
        print(f"  Connection Options: {conn_labels}")
        print(
            f"  Additional Options: {[a['name'] for a in additional] if additional else 'None'}"
        )
    db.close()


if __name__ == "__main__":
    print_options()
