"""
Script to reorganize the project structure.
This script creates the new directory structure and moves files to their new locations.
"""

import os
import shutil
from pathlib import Path


def create_directory_structure():
    """Create the new directory structure."""
    directories = [
        # Core structure
        'src/core/models',
        'src/core/services',
        'src/core/config',

        # API structure
        'src/api',

        # UI structure
        'src/ui/components',
        'src/ui/views',
        'src/ui/dialogs',

        # Utils and Export
        'src/utils',
        'src/export',

        # Scripts structure
        'scripts/data/config',
        'scripts/data/seeds',
        'scripts/data/init',
        'scripts/tools',

        # Tests structure
        'tests/unit',
        'tests/integration',
        'tests/fixtures',

        # Config structure
        'config/development',
        'config/production',
        'config/testing',
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f'Created directory: {directory}')

def move_files():
    """Move files to their new locations."""
    moves = [
        # Move configuration files
        ('scripts/data/config/*', 'src/core/config/'),
        ('scripts/data/init/*', 'scripts/data/init/'),
        ('scripts/data/seeds/*', 'scripts/data/seeds/'),

        # Move test files
        ('tests/*.py', 'tests/unit/'),

        # Move UI components
        ('src/ui/*.py', 'src/ui/views/'),
    ]

    for src_pattern, dest_dir in moves:
        for src_file in Path('.').glob(src_pattern):
            if src_file.is_file():
                dest_file = Path(dest_dir) / src_file.name
                shutil.move(str(src_file), str(dest_file))
                print(f'Moved {src_file} to {dest_file}')

def create_init_files():
    """Create __init__.py files in all Python packages."""
    for root, _dirs, _files in os.walk('src'):
        if '__pycache__' not in root:
            init_file = Path(root) / '__init__.py'
            if not init_file.exists():
                init_file.touch()
                print(f'Created {init_file}')

def main():
    """Main function to reorganize the project."""
    print('Starting project reorganization...')

    # Create new directory structure
    print('\nCreating directory structure...')
    create_directory_structure()

    # Move files to new locations
    print('\nMoving files...')
    move_files()

    # Create __init__.py files
    print('\nCreating __init__.py files...')
    create_init_files()

    print('\nProject reorganization complete!')

if __name__ == '__main__':
    main()
