"""
Script to create a backup of the database before making changes.
The backup will be stored in the legacy folder with a timestamp.
"""

import shutil
from datetime import datetime
from pathlib import Path


def backup_database():
    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent.parent

    # Define source and destination paths
    db_path = project_root / "data" / "quotes.db"
    legacy_dir = project_root / "legacy"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = legacy_dir / f"quotes_backup_{timestamp}.db"

    # Create legacy directory if it doesn't exist
    legacy_dir.mkdir(exist_ok=True)

    # Copy the database file
    if db_path.exists():
        shutil.copy2(db_path, backup_path)
        print(f"Database backed up to: {backup_path}")
    else:
        print(f"Error: Database file not found at {db_path}")


if __name__ == "__main__":
    backup_database()
