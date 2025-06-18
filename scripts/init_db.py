"""
Database initialization orchestrator.
This script coordinates the initialization of business configuration.
"""

import os
import sys
from pathlib import Path

# Add both the project root and src directory to the Python path
project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_dir))

from scripts.data.init.init_business_config import init_business_config


def init_database():
    """Initialize the database with business configuration."""
    print("Initializing database...")
    print("\nInitializing business configuration...")
    init_business_config()
    print("\nDatabase initialization complete!")


if __name__ == "__main__":
    init_database()
