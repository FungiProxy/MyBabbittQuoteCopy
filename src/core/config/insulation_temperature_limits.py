"""
Insulation temperature limits configuration.
Defines maximum temperature limits for each insulator type.
"""

from src.core.models.option import Option


def init_insulation_temperature_limits(db):
    """Initialize insulation temperature limits in the database."""
    options = [
        Option(
            name='Insulator Temperature Limits',
            description='Maximum temperature limits for each insulator type',
            price=0.0,
            price_type='fixed',
            category='Insulation',
            choices=['Delrin', 'Teflon', 'PEEK', 'Ceramic'],
            adders={
                'Delrin': 250,  # 250F
                'Teflon': 450,  # 450F
                'PEEK': 550,  # 550F
                'Ceramic': 1400,  # 1400F (dry materials only)
            },
            product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000',
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
