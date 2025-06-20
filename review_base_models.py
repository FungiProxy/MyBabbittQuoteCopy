#!/usr/bin/env python3
"""
Review Base Models for Product Families
Shows the single base model needed for each product family for dynamic configuration.
"""


def show_base_models():
    """Show the single base model needed for each product family."""

    # Base prices for each family (from price list)
    base_prices = {
        'LS2000': 425.0,
        'LS2100': 460.0,
        'LS6000': 550.0,
        'LS7000': 680.0,
        'LS7000/2': 770.0,
        'LS7500': 800.0,
        'LS8000': 715.0,
        'LS8000/2': 950.0,
        'LS8500': 1050.0,
        'LT9000': 1200.0,
        'FS10000': 1500.0,
    }

    # Standard base configuration for each family
    base_configs = {
        'LS2000': {
            'model_number': 'LS2000-BASE',
            'description': 'LS2000 Level Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'S',
        },
        'LS2100': {
            'model_number': 'LS2100-BASE',
            'description': 'LS2100 Level Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '24VDC',
            'material': 'S',
        },
        'LS6000': {
            'model_number': 'LS6000-BASE',
            'description': 'LS6000 Level Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'S',
        },
        'LS7000': {
            'model_number': 'LS7000-BASE',
            'description': 'LS7000 Level Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'S',
        },
        'LS7000/2': {
            'model_number': 'LS7000/2-BASE',
            'description': 'LS7000/2 Level Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'H',
        },
        'LS7500': {
            'model_number': 'LS7500-BASE',
            'description': 'LS7500 Presence/Absence Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'S',
        },
        'LS8000': {
            'model_number': 'LS8000-BASE',
            'description': 'LS8000 Level Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'S',
        },
        'LS8000/2': {
            'model_number': 'LS8000/2-BASE',
            'description': 'LS8000/2 Level Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'H',
        },
        'LS8500': {
            'model_number': 'LS8500-BASE',
            'description': 'LS8500 Presence/Absence Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'S',
        },
        'LT9000': {
            'model_number': 'LT9000-BASE',
            'description': 'LT9000 Level Transmitter - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'H',
        },
        'FS10000': {
            'model_number': 'FS10000-BASE',
            'description': 'FS10000 Flow Switch - Base Configuration',
            'base_length': 10.0,
            'voltage': '115VAC',
            'material': 'S',
        },
    }

    print('=' * 80)
    print('BASE MODELS FOR EACH PRODUCT FAMILY')
    print('(One per family for dynamic configuration)')
    print('=' * 80)

    total_models = 0

    for family_name in sorted(base_prices.keys()):
        base_price = base_prices[family_name]
        config = base_configs[family_name]

        print(f'\n{family_name}')
        print('-' * 60)
        print(f"  Model Number: {config['model_number']}")
        print(f"  Description: {config['description']}")
        print(f'  Base Price: ${base_price}')
        print(f"  Base Length: {config['base_length']}\"")
        print(f"  Base Voltage: {config['voltage']}")
        print(f"  Base Material: {config['material']}")
        print()

        total_models += 1

    print('=' * 80)
    print(f'TOTAL BASE MODELS TO CREATE: {total_models}')
    print('=' * 80)

    print('\nDYNAMIC CONFIGURATION APPROACH:')
    print('-' * 40)
    print('1. User selects a product family from the left panel')
    print('2. System loads the base model for that family')
    print('3. User configures options (materials, voltages, etc.)')
    print('4. System applies adders to the base price')
    print('5. Final price = Base Price + Material Adder + Voltage Adder + etc.')
    print()
    print('Example for LS2000:')
    print('  Base Price: $425')
    print('  + Halar Material: +$110')
    print('  + 24VDC Voltage: +$0')
    print('  + Extra Static Protection: +$30')
    print('  Final Price: $565')


if __name__ == '__main__':
    show_base_models()
