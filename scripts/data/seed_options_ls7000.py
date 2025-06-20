from src.core.models.option import Option

Option(
    name="Exotic Metals",
    description="Exotic metal selection",
    product_families=FAMILY_NAME,
    price=0.0,
    price_type="fixed",
    category="Mechanical",
    choices=["Alloy 20", "Hastelloy C", "Hastelloy B", "Titanium"],
    adders={"Alloy 20": 0, "Hastelloy C": 0, "Hastelloy B": 0, "Titanium": 0},
    rules=None,
    excluded_products="",
),
