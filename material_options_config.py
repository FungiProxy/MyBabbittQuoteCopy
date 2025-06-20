#!/usr/bin/env python3
"""
Material Options Configuration
Defines the correct material options for each product family.
"""

MATERIAL_OPTIONS_CONFIG = {
    'LS2000': {
        'choices': ['S', 'H', 'TS', 'U', 'T', 'C', 'A', 'HC', 'HB', 'TT'],
        'adders': {
            'S': 0,
            'H': 110,
            'TS': 110,
            'U': 20,
            'T': 60,
            'C': 80,
            'A': 0,
            'HC': 0,
            'HB': 0,
            'TT': 0,
        },
    },
    'LS2100': {
        'choices': ['S', 'H', 'TS', 'U', 'T', 'C', 'A', 'HC', 'HB', 'TT'],
        'adders': {
            'S': 0,
            'H': 110,
            'TS': 110,
            'U': 20,
            'T': 60,
            'C': 80,
            'A': 0,
            'HC': 0,
            'HB': 0,
            'TT': 0,
        },
    },
    'LS6000': {
        'choices': ['S', 'H', 'TS', 'U', 'T', 'C', 'CPVC', 'A', 'HC', 'HB', 'TT'],
        'adders': {
            'S': 0,
            'H': 110,
            'TS': 110,
            'U': 20,
            'T': 60,
            'C': 80,
            'CPVC': 400,
            'A': 0,
            'HC': 0,
            'HB': 0,
            'TT': 0,
        },
    },
    'LS7000': {
        'choices': ['S', 'H', 'TS', 'U', 'T', 'C', 'CPVC', 'A', 'HC', 'HB', 'TT'],
        'adders': {
            'S': 0,
            'H': 110,
            'TS': 110,
            'U': 20,
            'T': 60,
            'C': 80,
            'CPVC': 400,
            'A': 0,
            'HC': 0,
            'HB': 0,
            'TT': 0,
        },
    },
    'LS7000/2': {
        'choices': ['H', 'TS', 'A', 'HC', 'HB', 'TT'],
        'adders': {'H': 0, 'TS': 0, 'A': 0, 'HC': 0, 'HB': 0, 'TT': 0},
    },
    'LS8000': {
        'choices': ['S', 'H', 'TS', 'U', 'T', 'C', 'A', 'HC', 'HB', 'TT'],
        'adders': {
            'S': 0,
            'H': 110,
            'TS': 110,
            'U': 20,
            'T': 60,
            'C': 80,
            'A': 0,
            'HC': 0,
            'HB': 0,
            'TT': 0,
        },
    },
    'LS8000/2': {
        'choices': ['H', 'TS', 'A', 'HC', 'HB', 'TT'],
        'adders': {'H': 0, 'TS': 0, 'A': 0, 'HC': 0, 'HB': 0, 'TT': 0},
    },
    'LT9000': {
        'choices': ['H', 'TS', 'A', 'HC', 'HB', 'TT'],
        'adders': {'H': 0, 'TS': 0, 'A': 0, 'HC': 0, 'HB': 0, 'TT': 0},
    },
    'FS10000': {
        'choices': ['S', 'A', 'HC', 'HB', 'TT'],
        'adders': {'S': 0, 'A': 0, 'HC': 0, 'HB': 0, 'TT': 0},
    },
    'LS7500': {
        'choices': ['S', 'A', 'HC', 'HB', 'TT'],
        'adders': {'S': 0, 'A': 0, 'HC': 0, 'HB': 0, 'TT': 0},
    },
    'LS8500': {
        'choices': ['S', 'A', 'HC', 'HB', 'TT'],
        'adders': {'S': 0, 'A': 0, 'HC': 0, 'HB': 0, 'TT': 0},
    },
}

# Material code descriptions for reference
MATERIAL_DESCRIPTIONS = {
    'S': 'S - 316 Stainless Steel',
    'H': 'H - Halar Coated',
    'TS': 'TS - Teflon Sleeve',
    'U': 'U - UHMWPE Blind End',
    'T': 'T - Teflon Blind End',
    'C': 'C - Cable',
    'CPVC': 'CPVC - CPVC Blind End',
    'A': 'A - Alloy 20',
    'HC': 'HC - Hastelloy-C-276',
    'HB': 'HB - Hastelloy-B',
    'TT': 'TT - Titanium',
}

# Exotic metals list
EXOTIC_METALS = ['A', 'HC', 'HB', 'TT']
