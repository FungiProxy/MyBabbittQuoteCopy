"""
Material options configuration.
Defines material options and pricing for all product families.
"""

from src.core.models.option import Option

def init_material_options(db):
    """Initialize material options for all product families."""
    options = [
        # Material Options for LS2000
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["S", "H", "TS", "U", "T", "C"],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "U": 20,  # UHMWPE Blind End
                "T": 60,  # Teflon Blind End
                "C": 80,  # Cable
            },
            product_families="LS2000",
        ),
        # Material Options for LS2100
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["S", "H", "TS", "U", "T", "C"],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "U": 20,  # UHMWPE Blind End
                "T": 60,  # Teflon Blind End
                "C": 80,  # Cable
            },
            product_families="LS2100",
        ),
        # Material Options for LS6000
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["S", "H", "TS", "U", "T", "C", "CPVC"],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "U": 20,  # UHMWPE Blind End
                "T": 60,  # Teflon Blind End
                "C": 80,  # Cable
                "CPVC": 400,  # CPVC Blind End
            },
            product_families="LS6000",
        ),
        # Material Options for LS7000
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["S", "H", "TS", "T", "U", "CPVC"],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "U": 20,  # UHMWPE Blind End
                "T": 60,  # Teflon Blind End
                "C": 80,  # Cable
                "CPVC": 400,  # CPVC Blind End
            },
            product_families="LS7000",
        ),
        # Material Options for LS7000/2
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["H", "TS"],
            adders={
                "H": 0,  # Halar Coated
                "TS": 0,  # Teflon Sleeve
            },
            product_families="LS7000/2",
        ),
        # Material Options for LS8000
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["S", "H", "TS", "C"],
            adders={
                "S": 0,  # 316 Stainless Steel
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
                "C": 80,  # Cable
            },
            product_families="LS8000",
        ),
        # Material Options for LS8000/2
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["H", "TS"],
            adders={
                "H": 110,  # Halar Coated
                "TS": 110,  # Teflon Sleeve
            },
            product_families="LS8000/2",
        ),
        # Material Options for LT9000
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["H", "TS"],
            adders={
                "H": 0,  # Halar Coated
                "TS": 0,  # Teflon Sleeve
            },
            product_families="LT9000",
        ),
        # Material Options for FS10000
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["S"],
            adders={
                "S": 0,  # 316 Stainless Steel
            },
            product_families="FS10000",
        ),
        # Material Options for Presence/Absence Switches
        Option(
            name="Material",
            description="Probe material selection", 
            price=0.0,
            price_type="fixed",
            category="Material",
            choices=["S"],
            adders={
                "S": 0,  # 316 Stainless Steel
            },
            product_families="LS7500,LS8500",
        ),
    ]
    
    for option in options:
        exists = (
            db.query(Option)
            .filter_by(name=option.name, category=option.category)
            .first()
        )
        if not exists:
            db.add(option)
