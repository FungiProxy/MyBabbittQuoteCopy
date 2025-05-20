import pytest
import sys
from pathlib import Path

# Add the src directory to Python path for test imports
src_path = str(Path(__file__).parent.parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Common fixtures can be added here
@pytest.fixture
def app_config():
    """Fixture for test configuration"""
    return {
        'test_mode': True,
        'db_url': 'sqlite:///:memory:'
    } 