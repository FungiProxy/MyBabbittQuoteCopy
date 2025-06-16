"""
Pytest configuration file.

This file sets up the test environment and provides common fixtures.
"""

import sys
from pathlib import Path

import pytest

# Add the project root directory to the Python path
project_root = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, project_root)

# Add the src directory to Python path for test imports
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)


# Common fixtures can be added here
@pytest.fixture
def app_config():
    """Fixture for test configuration"""
    return {'test_mode': True, 'db_url': 'sqlite:///:memory:'}
