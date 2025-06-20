#!/usr/bin/env python3
"""
Analyze current option categories and suggest better naming.
"""

import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.core.database import SessionLocal
from src.core.models.option import Option


def analyze_categories():
    """Analyze current categories and suggest better names."""
    print('=== CATEGORY ANALYSIS AND NAMING SUGGESTIONS ===')

    db = SessionLocal()
    try:
        # Get all categories
        categories = db.query(Option.category).distinct().all()

        print('Current categories and suggested improvements:')
        print('-' * 60)

        for cat in categories:
            category_name = cat[0]
            options = db.query(Option).filter_by(category=category_name).all()

            print(f"\nCurrent: '{category_name}' ({len(options)} options)")

            # Analyze what's in this category
            option_names = [opt.name for opt in options]
            print(f'  Contains: {option_names}')

            # Suggest better name
            suggested_name = suggest_better_category_name(category_name, option_names)
            print(f"  Suggested: '{suggested_name}'")

            # Show reasoning
            reasoning = get_category_reasoning(category_name, option_names)
            print(f'  Reasoning: {reasoning}')

    finally:
        db.close()


def suggest_better_category_name(current_name, option_names):
    """Suggest a better category name based on the options it contains."""

    # Map current names to better names
    category_mapping = {
        'Material': 'Materials',
        'Electrical': 'Voltages',  # Since it's mostly voltage options
        'Mechanical': 'Connections',  # Since it's mostly connection options
        'Exotic Metal': 'Exotic Metals',
        'O-ring Material': 'O-Ring Materials',
    }

    # Check if we have a direct mapping
    if current_name in category_mapping:
        return category_mapping[current_name]

    # Analyze option names to suggest better category
    if any('voltage' in name.lower() for name in option_names):
        return 'Voltages'
    elif any(
        'connection' in name.lower()
        or 'npt' in name.lower()
        or 'flange' in name.lower()
        for name in option_names
    ):
        return 'Connections'
    elif any('material' in name.lower() for name in option_names):
        return 'Materials'
    elif any('o-ring' in name.lower() for name in option_names):
        return 'O-Ring Materials'
    elif any('exotic' in name.lower() for name in option_names):
        return 'Exotic Metals'
    else:
        return current_name


def get_category_reasoning(current_name, option_names):
    """Get reasoning for the category name suggestion."""

    if current_name == 'Electrical':
        voltage_count = sum(1 for name in option_names if 'voltage' in name.lower())
        total_count = len(option_names)
        if voltage_count == total_count:
            return "All options are voltage-related, so 'Voltages' is more specific"
        else:
            return f'Contains {voltage_count}/{total_count} voltage options, plus other electrical options'

    elif current_name == 'Mechanical':
        connection_count = sum(
            1
            for name in option_names
            if any(
                x in name.lower() for x in ['connection', 'npt', 'flange', 'tri-clamp']
            )
        )
        total_count = len(option_names)
        if connection_count == total_count:
            return (
                "All options are connection-related, so 'Connections' is more specific"
            )
        else:
            return f'Contains {connection_count}/{total_count} connection options, plus other mechanical options'

    elif current_name == 'Material':
        return "Should be plural 'Materials' for consistency"

    elif current_name == 'Exotic Metal':
        return "Should be plural 'Exotic Metals' for consistency"

    elif current_name == 'O-ring Material':
        return "Should be 'O-Ring Materials' (plural and proper capitalization)"

    else:
        return 'No specific reasoning'


def show_proposed_category_structure():
    """Show the proposed new category structure."""
    print('\n' + '=' * 60)
    print('PROPOSED NEW CATEGORY STRUCTURE')
    print('=' * 60)

    proposed_categories = {
        'Materials': 'Probe material selection (S, H, TS, U, T, C, CPVC)',
        'Voltages': 'Supply voltage selection (115VAC, 24VDC, etc.)',
        'Connections': 'Connection type and size selection (NPT, Flange, Tri-clamp)',
        'O-Ring Materials': 'O-Ring material selection (Viton, Silicon, etc.)',
        'Exotic Metals': 'Exotic metal selection (Alloy 20, Hastelloy, etc.)',
        'Accessories': 'Additional features (Bent Probe, Stainless Steel Tag, etc.)',
    }

    for category, description in proposed_categories.items():
        print(f'\n{category}:')
        print(f'  {description}')


def main():
    """Run the category analysis."""
    analyze_categories()
    show_proposed_category_structure()

    print('\n' + '=' * 60)
    print('RECOMMENDATIONS:')
    print('=' * 60)
    print("1. Change 'Electrical' → 'Voltages' (more specific)")
    print("2. Change 'Mechanical' → 'Connections' (more specific)")
    print("3. Change 'Material' → 'Materials' (plural)")
    print("4. Change 'Exotic Metal' → 'Exotic Metals' (plural)")
    print("5. Change 'O-ring Material' → 'O-Ring Materials' (proper format)")
    print("6. Consider adding 'Accessories' category for non-core options")


if __name__ == '__main__':
    main()
