"""
Insulation application notes configuration.
Defines important notes and restrictions for each insulator type.
"""

from src.core.models.option import Option


def init_insulation_application_notes(db):
    """Initialize insulation application notes in the database."""
    options = [
        Option(
            name="Insulator Application Notes",
            description="Important notes about insulator applications",
            price=0.0,
            price_type="fixed",
            category="Insulation",
            choices=["Standard Delrin", "Standard Teflon", "PEEK", "Ceramic"],
            adders={
                "Standard Delrin": 0,  # Standard for SS probes
                "Standard Teflon": 0,  # Standard for Halar and TS probes
                "PEEK": 0,  # Higher temperature option
                "Ceramic": 0,  # Dry materials only
            },
            product_families="LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000",
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
