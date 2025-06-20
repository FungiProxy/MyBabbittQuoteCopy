"""
Connection options configuration.
Defines connection types and sizes for all product families.
"""

from src.core.models.option import Option


def init_connection_options(db):
    """Initialize connection options for all product families."""
    options = [
        # Primary Connection Type Selection (Common for all families)
        Option(
            name='Connection Type',
            description='Primary connection type selection',
            price=0.0,
            price_type='fixed',
            category='Mechanical',
            choices=['NPT', 'Flange', 'Tri-clamp'],
            adders={
                'NPT': 0,  # Standard
                'Flange': 0,  # Base price for flange
                'Tri-clamp': 0,  # Base price for tri-clamp
            },
            product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
        ),
        # NPT Size Options for 3/4" Standard Models
        Option(
            name='NPT Size',
            description='NPT connection size selection',
            price=0.0,
            price_type='fixed',
            category='Mechanical',
            choices=['3/4"'],
            adders={
                '3/4"': 0,
            },
            product_families='LS2000,LS2100,FS10000',
        ),
        # NPT Size Options for 1" Standard Models with free 3/4" option
        Option(
            name='NPT Size',
            description='NPT connection size selection',
            price=0.0,
            price_type='fixed',
            category='Mechanical',
            choices=['1"', '3/4"'],
            adders={
                '1"': 0,
                '3/4"': 0,
            },
            product_families='LS6000,LS7000,LS7000/2,LT9000',
        ),
        # NPT Size Options for 3/4" Standard with free 1" option
        Option(
            name='NPT Size',
            description='NPT connection size selection',
            price=0.0,
            price_type='fixed',
            category='Mechanical',
            choices=['3/4"', '1"'],
            adders={
                '3/4"': 0,
                '1"': 0,
            },
            product_families='LS8000,LS8000/2',
        ),
        # Flange Options
        Option(
            name='Flange Type',
            description='Flange type selection',
            price=0.0,
            price_type='fixed',
            category='Mechanical',
            choices=['150#', '300#'],
            adders={
                '150#': 0,  # Consult factory
                '300#': 0,  # Consult factory
            },
            product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
        ),
        Option(
            name='Flange Size',
            description='Flange size selection',
            price=0.0,
            price_type='fixed',
            category='Mechanical',
            choices=['1"', '1.5"', '2"', '3"', '4"'],
            adders={
                '1"': 0,  # Consult factory
                '1.5"': 0,  # Consult factory
                '2"': 0,  # Consult factory
                '3"': 0,  # Consult factory
                '4"': 0,  # Consult factory
            },
            product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
        ),
        # Tri-clamp Options
        Option(
            name='Tri-clamp',
            description='Tri-clamp selection',
            price=0.0,
            price_type='fixed',
            category='Mechanical',
            choices=[
                '1.5" Tri-clamp Process Connection',
                '1.5" Tri-clamp Spud',
                '2" Tri-clamp Process Connection',
                '2" Tri-clamp Spud',
            ],
            adders={
                '1.5" Tri-clamp Process Connection': 280.0,
                '1.5" Tri-clamp Spud': 170.0,
                '2" Tri-clamp Process Connection': 330.0,
                '2" Tri-clamp Spud': 220.0,
            },
            product_families='LS2000,LS2100,LS6000,LS7000,LS7000/2,LS8000,LS8000/2,LT9000,FS10000,LS7500,LS8500',
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
