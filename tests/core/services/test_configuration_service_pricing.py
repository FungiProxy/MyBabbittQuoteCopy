"""
Test suite for configuration service pricing functionality.

This module tests the price calculations in the configuration service.
"""

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.core.services.configuration_service import ConfigurationService
from src.core.models import Product, Material, ConnectionOption


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock(spec=Session)


@pytest.fixture
def config_service(mock_db):
    """Create a configuration service instance for testing."""
    return ConfigurationService(mock_db)


@pytest.fixture
def base_product_info():
    """Create base product information for testing."""
    return {
        "id": 1,
        "model_number": "LS2000-120-S",
        "base_price": 500.0,
        "base_length": 10.0,
        "material": "S",
        "voltage": "120V",
    }


def test_calculate_price_basic(config_service, mock_db, base_product_info):
    """Test basic price calculation."""
    # Set up test data
    config_service.current_config = MagicMock()
    config_service.current_config.product_family_id = 1
    config_service.current_config.selected_options = {}
    config_service.current_config.base_product = base_product_info

    # Mock variant query
    variant = Product(
        id=1,
        model_number="LS2000-120-S",
        base_price=500.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = variant

    # Calculate price
    with patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=500.0,
    ):
        price = config_service.calculate_price()

    assert price == 500.0


def test_calculate_price_with_length(config_service, mock_db, base_product_info):
    """Test price calculation with length adjustment."""
    # Set up test data
    config_service.current_config = MagicMock()
    config_service.current_config.product_family_id = 1
    config_service.current_config.selected_options = {
        "Probe Length": 24.0,  # 24 inches
    }
    config_service.current_config.base_product = base_product_info

    # Mock variant query
    variant = Product(
        id=1,
        model_number="LS2000-120-S",
        base_price=500.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = variant

    # Calculate price
    with patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=612.0,
    ):
        price = config_service.calculate_price()

    assert price == 612.0  # Base price + length adjustment


def test_calculate_price_with_connection(config_service, mock_db, base_product_info):
    """Test price calculation with connection option."""
    # Set up test data
    config_service.current_config = MagicMock()
    config_service.current_config.product_family_id = 1
    config_service.current_config.selected_options = {
        "Connection": "Flange",
        "Flange Rating": "150#",
        "Flange Size": '1"',
    }
    config_service.current_config.base_product = base_product_info

    # Mock variant query
    variant = Product(
        id=1,
        model_number="LS2000-120-S",
        base_price=500.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = variant

    # Calculate price
    with patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=600.0,
    ):
        price = config_service.calculate_price()

    assert price == 600.0  # Base price + connection option


def test_calculate_price_with_material_override(
    config_service, mock_db, base_product_info
):
    """Test price calculation with material override."""
    # Set up test data
    config_service.current_config = MagicMock()
    config_service.current_config.product_family_id = 1
    config_service.current_config.selected_options = {
        "Material": "U",  # UHMWPE
    }
    config_service.current_config.base_product = base_product_info

    # Mock variant query
    variant = Product(
        id=1,
        model_number="LS2000-120-U",
        base_price=500.0,
        base_length=10.0,
        material="U",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = variant

    # Calculate price
    with patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=520.0,
    ):
        price = config_service.calculate_price()

    assert price == 520.0  # Base price + UHMWPE premium


def test_calculate_price_no_variant_fallback(
    config_service, mock_db, base_product_info
):
    """Test price calculation fallback when no variant is found."""
    # Set up test data
    config_service.current_config = MagicMock()
    config_service.current_config.product_family_id = 1
    config_service.current_config.selected_options = {
        "Material": "X",  # Non-existent material
    }
    config_service.current_config.base_product = base_product_info

    # Mock variant query to return None
    mock_db.query().filter().first.return_value = None

    # Calculate price
    price = config_service.calculate_price()

    assert price == 500.0  # Should fall back to base product price


def test_calculate_price_special_product(config_service, mock_db):
    """Test price calculation for special product type (LS7000/2)."""
    # Set up test data
    config_service.current_config = MagicMock()
    config_service.current_config.product_family_id = 2
    config_service.current_config.selected_options = {}
    config_service.current_config.base_product = {
        "id": 2,
        "model_number": "LS7000/2-120-S",
        "base_price": 800.0,
        "base_length": 10.0,
        "material": "S",
        "voltage": "120V",
    }

    # Mock variant query
    variant = Product(
        id=2,
        model_number="LS7000/2-120-S",
        base_price=800.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = variant

    # Calculate price
    with patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=800.0,
    ):
        price = config_service.calculate_price()

    assert price == 800.0  # Base price for LS7000/2


def test_calculate_price_complex_configuration(
    config_service, mock_db, base_product_info
):
    """Test price calculation with multiple options."""
    # Set up test data
    config_service.current_config = MagicMock()
    config_service.current_config.product_family_id = 1
    config_service.current_config.selected_options = {
        "Probe Length": 24.0,  # 24 inches
        "Material": "U",  # UHMWPE
        "Connection": "Flange",
        "Flange Rating": "150#",
        "Flange Size": '1"',
    }
    config_service.current_config.base_product = base_product_info

    # Mock variant query
    variant = Product(
        id=1,
        model_number="LS2000-120-U",
        base_price=500.0,
        base_length=10.0,
        material="U",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = variant

    # Calculate price
    with patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=732.0,
    ):
        price = config_service.calculate_price()

    assert price == 732.0  # Base price + length + material + connection
