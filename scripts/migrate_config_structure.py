"""
Migration script to restructure the business configuration and seeding logic.
This script will:
1. Create new directory structure
2. Move files to their new locations
3. Update import paths
4. Create new configuration modules
"""

import shutil
from pathlib import Path


def create_directory_structure():
    """Create the new directory structure for configuration and seeds."""
    base_dir = Path(__file__).parent

    # Define new directory structure
    new_dirs = [
        base_dir / 'data' / 'config',
        base_dir / 'data' / 'init',
    ]

    # Create directories
    for dir_path in new_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        # Create __init__.py files
        init_file = dir_path / '__init__.py'
        init_file.touch()


def create_config_modules():
    """Create the new configuration module files."""
    base_dir = Path(__file__).parent / 'data' / 'config'

    # Define module files and their content
    modules = {
        'product_families.py': '''"""
Product family configurations.
Defines all product families and their basic properties.
"""

from src.core.models.product_family import ProductFamily

def init_product_families(db):
    """Initialize product families in the database."""
    product_families = [
        ProductFamily(
            name="LS2000",
            description="LS2000 Level Switch",
            category="Point Level Switch",
        ),
        # ... other product families
    ]
    db.add_all(product_families)
''',
        'materials.py': '''"""
Material options configuration.
Defines material options and pricing for all product families.
"""

from src.core.models.option import Option

def init_material_options(db):
    """Initialize material options for all product families."""
    options = [
        # Material options will be moved here
    ]

    for option in options:
        exists = (
            db.query(Option)
            .filter_by(name=option.name, category=option.category)
            .first()
        )
        if not exists:
            db.add(option)
''',
        'voltages.py': '''"""
Voltage options configuration.
Defines voltage options for all product families.
"""

from src.core.models.option import Option

def init_voltage_options(db):
    """Initialize voltage options for all product families."""
    options = [
        # Voltage options will be moved here
    ]

    for option in options:
        exists = (
            db.query(Option)
            .filter_by(name=option.name, category=option.category)
            .first()
        )
        if not exists:
            db.add(option)
''',
        'connections.py': '''"""
Connection options configuration.
Defines connection types and sizes for all product families.
"""

from src.core.models.option import Option

def init_connection_options(db):
    """Initialize connection options for all product families."""
    options = [
        # Connection options will be moved here
    ]

    for option in options:
        exists = (
            db.query(Option)
            .filter_by(name=option.name, category=option.category)
            .first()
        )
        if not exists:
            db.add(option)
''',
        'standard_lengths.py': '''"""
Standard length configurations.
Defines standard lengths for different materials.
"""

from src.core.models.standard_length import StandardLength

def init_standard_lengths(db):
    """Initialize standard lengths in the database."""
    standard_lengths = [
        StandardLength(material_code="H", length=6.0),
        StandardLength(material_code="H", length=10.0),
        StandardLength(material_code="H", length=12.0),
        StandardLength(material_code="H", length=18.0),
        StandardLength(material_code="H", length=24.0),
        StandardLength(material_code="H", length=36.0),
        StandardLength(material_code="H", length=48.0),
        StandardLength(material_code="H", length=60.0),
        StandardLength(material_code="H", length=72.0),
        StandardLength(material_code="H", length=84.0),
        StandardLength(material_code="H", length=96.0),
    ]
    db.add_all(standard_lengths)
''',
        'misc_options.py': '''"""
Miscellaneous options configuration.
Defines various additional options like warranty, shipping, etc.
"""

from src.core.models.option import Option

def init_misc_options(db):
    """Initialize miscellaneous options in the database."""
    options = [
        # Miscellaneous options will be moved here
    ]

    for option in options:
        exists = (
            db.query(Option)
            .filter_by(name=option.name, category=option.category)
            .first()
        )
        if not exists:
            db.add(option)
''',
    }

    # Create module files
    for filename, content in modules.items():
        file_path = base_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)


def move_init_files():
    """Move initialization files to their new locations."""
    base_dir = Path(__file__).parent

    # Move init_business_config.py
    shutil.move(
        base_dir / 'init_business_config.py',
        base_dir / 'data' / 'init' / 'init_business_config.py',
    )

    # Move init_sample_data.py
    shutil.move(
        base_dir / 'init_sample_data.py',
        base_dir / 'data' / 'init' / 'init_sample_data.py',
    )


def update_imports():
    """Update import statements in affected files."""
    base_dir = Path(__file__).parent

    # Update init_db.py
    init_db_path = base_dir / 'init_db.py'
    if init_db_path.exists():
        with open(init_db_path) as f:
            content = f.read()

        # Update import statement
        content = content.replace(
            'from init_business_config import init_business_config',
            'from scripts.data.init.init_business_config import init_business_config',
        )

        with open(init_db_path, 'w') as f:
            f.write(content)


def main():
    """Run the migration process."""
    print('Starting configuration structure migration...')

    try:
        # Create new directory structure
        print('Creating new directory structure...')
        create_directory_structure()

        # Create configuration modules
        print('Creating configuration modules...')
        create_config_modules()

        # Move initialization files
        print('Moving initialization files...')
        move_init_files()

        # Update imports
        print('Updating import statements...')
        update_imports()

        print('Migration completed successfully!')

    except Exception as e:
        print(f'Error during migration: {e}')
        raise


if __name__ == '__main__':
    main()
