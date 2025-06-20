"""
Insulation options configuration.
Defines insulation types and pricing for all product families.
"""

from src.core.models.option import Option


def init_insulation_options(db):
    """Initialize insulation options for all product families."""
    options = [
        # Insulation Options for SS Probes (Standard is Delrin)
        Option(
            name="Insulator Type",
            description="Probe insulator material selection for SS probes",
            price=0.0,
            price_type="fixed",
            category="Insulation",
            choices=["Standard Delrin", "Teflon", "PEEK", "Ceramic"],
            adders={
                "Standard Delrin": 0,  # Standard for SS probes
                "Teflon": 40.0,  # Instead of Delrin
                "PEEK": 340.0,  # Higher temperature option
                "Ceramic": 470.0,  # For dry materials only
            },
            product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
            material_dependency="S",  # Only for SS probes
        ),
        # Insulation Options for Halar and TS Probes (Standard is Teflon)
        Option(
            name="Insulator Type",
            description="Probe insulator material selection for Halar and TS probes",
            price=0.0,
            price_type="fixed",
            category="Insulation",
            choices=["Standard Teflon", "PEEK", "Ceramic"],
            adders={
                "Standard Teflon": 0,  # Standard for Halar and TS probes
                "PEEK": 340.0,  # Higher temperature option
                "Ceramic": 470.0,  # For dry materials only
            },
            product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
            material_dependency="H,TS",  # Only for Halar and Teflon Sleeve probes
        ),
        # Insulation Options for Other Materials (No standard)
        Option(
            name="Insulator Type",
            description="Probe insulator material selection for other materials",
            price=0.0,
            price_type="fixed",
            category="Insulation",
            choices=["Teflon", "PEEK", "Ceramic"],
            adders={
                "Teflon": 40.0,
                "PEEK": 340.0,  # Higher temperature option
                "Ceramic": 470.0,  # For dry materials only
            },
            product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
            material_dependency="U,T,C,CPVC",  # For other materials
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
