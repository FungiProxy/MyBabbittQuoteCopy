"""
Test suite for configuration service pricing functionality.

This module tests the price calculations in the configuration service.
"""

from collections import namedtuple
from unittest.mock import MagicMock

import pytest

from src.core.models.configuration import Configuration
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService

Variant = namedtuple('Variant', ['model_number', 'base_price', 'material', 'voltage', 'length'])
MaterialOption = namedtuple('MaterialOption', ['adder'])
ConnectionOption = namedtuple('ConnectionOption', ['price'])


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    db = MagicMock()
    return db


@pytest.fixture
def mock_product_service():
    """Create a mock product service."""
    service = MagicMock(spec=ProductService)
    return service


@pytest.fixture
def config_service(mock_db, mock_product_service):
    """Create a ConfigurationService instance for testing."""
    return ConfigurationService(mock_db, mock_product_service)


@pytest.fixture
def base_product_info():
    """Create base product information for testing."""
    return {
        'id': 1,
        'model_number': 'LS2000-120-S',
        'base_price': 500.0,
        'base_length': 10.0,
        'material': 'S',
        'voltage': '120V',
    }


def test_calculate_price_basic(config_service, mock_db):
    """Test basic price calculation."""
    # Set up test data
    config_service.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name='LS2000',
        base_product={
            'id': 1,
            'name': 'LS2000',
            'base_price': 500.0,
            'base_length': 10.0,
            'category': 'Level Switch'
        },
        selected_options={},
        final_price=0.0,
        final_description='',
        model_number='',
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock variant query with proper base_price configuration
    variant = MagicMock()
    variant.model_number = 'LS2000-120-S'
    variant.base_price = 500.0
    variant.material = 'S'
    variant.voltage = '120V'
    variant.length = 10.0
    config_service.product_service.find_variant.return_value = variant

    # Calculate price
    config_service._update_price()

    # Verify price calculation
    assert config_service.current_config.final_price == 500.0


def test_calculate_price_with_length(config_service, mock_db):
    """Test price calculation with length adjustment."""
    # Set up test data
    config_service.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name='LS2000',
        base_product={
            'id': 1,
            'name': 'LS2000',
            'base_price': 500.0,
            'base_length': 10.0,
            'category': 'Level Switch'
        },
        selected_options={'Probe Length': 24.0},  # 24 inches
        final_price=0.0,
        final_description='',
        model_number='',
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock variant with base_price=500.0 and length=10.0
    variant = MagicMock()
    variant.model_number = 'LS2000-120-S-24'
    variant.base_price = 500.0
    variant.material = 'S'
    variant.voltage = '120V'
    variant.length = 10.0
    config_service.product_service.find_variant.return_value = variant

    # Calculate price
    config_service._update_price()

    # Verify price with length adjustment
    # Base price: $500.0
    # Extra length (24" - 10" = 14"): 14 * $8.0 = $112.0
    expected_price = 500.0 + (14.0 * 8.0)
    assert config_service.current_config.final_price == expected_price


def test_calculate_price_with_connection(config_service, mock_db):
    """Test price calculation with connection option."""
    # Set up test data
    config_service.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name='LS2000',
        base_product={
            'id': 1,
            'name': 'LS2000',
            'base_price': 500.0,
            'base_length': 10.0,
            'category': 'Level Switch'
        },
        selected_options={
            'Connection Type': 'Flange',
            'Flange Rating': '150#',
            'Flange Size': '1"'
        },
        final_price=0.0,
        final_description='',
        model_number='',
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock connection option query
    connection = MagicMock()
    connection.type = 'Flange'
    connection.rating = '150#'
    connection.size = '1"'
    connection.price = 150.0
    variant = Variant('LS2000-120-S-F150-1', 500.0, 'S', '120V', 10.0)

    # Set up the mock query chain
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_filter
    mock_filter.first.return_value = connection

    # Mock product service find_variant
    config_service.product_service.find_variant.return_value = variant

    # Calculate price
    config_service._update_price()

    # Verify price with connection option
    # Base price: $500.0
    # Connection option: $150.0
    expected_price = 500.0 + 150.0
    assert config_service.current_config.final_price == expected_price
    assert config_service.current_config.model_number == 'LS2000-120-S-F150-1'


def test_calculate_price_with_material_override(config_service, mock_db):
    """Test price calculation with material override."""
    # Set up test data
    config_service.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name='LS2000',
        base_product={
            'id': 1,
            'name': 'LS2000',
            'base_price': 500.0,
            'base_length': 10.0,
            'category': 'Level Switch'
        },
        selected_options={'Material': 'Halar'},
        final_price=0.0,
        final_description='',
        model_number='',
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock material option query
    material = MagicMock()
    material.material_code = 'Halar'
    material.adder = 110.0
    variant = Variant('LS2000-120-H', 500.0, 'H', '120V', 10.0)

    # Set up the mock query chain
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_filter
    mock_filter.first.return_value = material

    # Mock product service find_variant
    config_service.product_service.find_variant.return_value = variant

    # Calculate price
    config_service._update_price()

    # Verify price with material override
    # Base price: $500.0
    # Material adder: $110.0
    expected_price = 500.0 + 110.0
    assert config_service.current_config.final_price == expected_price
    assert config_service.current_config.model_number == 'LS2000-120-H'


def test_calculate_price_no_variant_fallback(config_service, mock_db):
    """Test price calculation when no variant is found."""
    # Set up test data
    config_service.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name='LS2000',
        base_product={
            'id': 1,
            'name': 'LS2000',
            'base_price': 500.0,
            'base_length': 10.0,
            'category': 'Level Switch'
        },
        selected_options={'Voltage': '24VDC'},
        final_price=0.0,
        final_description='',
        model_number='',
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock variant query to return None
    mock_db.query().filter().first.return_value = None
    config_service.product_service.find_variant.return_value = None

    # Calculate price
    config_service._update_price()

    # Verify fallback to base price
    assert config_service.current_config.final_price == 500.0
    assert config_service.current_config.model_number == ''


def test_calculate_price_special_product(config_service, mock_db):
    """Test price calculation for special product."""
    # Set up test data
    config_service.current_config = Configuration(
        db=mock_db,
        product_family_id=2,
        product_family_name='Special',
        base_product={
            'id': 2,
            'name': 'Special',
            'base_price': 1000.0,
            'base_length': 10.0,
            'category': 'Special'
        },
        selected_options={},
        final_price=0.0,
        final_description='',
        model_number='',
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock variant query
    variant = Variant('SPECIAL-120-S', 1000.0, 'S', '120V', 10.0)
    mock_db.query().filter().first.return_value = variant
    config_service.product_service.find_variant.return_value = variant

    # Calculate price
    config_service._update_price()

    # Verify special product price
    assert config_service.current_config.final_price == 1000.0
    assert config_service.current_config.model_number == 'SPECIAL-120-S'


def test_calculate_price_complex_configuration(config_service, mock_db):
    """Test price calculation for complex configuration."""
    # Set up test data
    config_service.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name='LS2000',
        base_product={
            'id': 1,
            'name': 'LS2000',
            'base_price': 500.0,
            'base_length': 10.0,
            'category': 'Level Switch'
        },
        selected_options={
            'Voltage': '24VDC',
            'Material': 'Halar',
            'Probe Length': 24.0,
            'Connection Type': 'Flange',
            'Flange Rating': '150#',
            'Flange Size': '1"'
        },
        final_price=0.0,
        final_description='',
        model_number='',
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock material option query
    material = MagicMock()
    material.material_code = 'Halar'
    material.adder = 110.0

    # Mock connection option query
    connection = MagicMock()
    connection.type = 'Flange'
    connection.rating = '150#'
    connection.size = '1"'
    connection.price = 150.0

    variant = Variant('LS2000-24-H-24-F150-1', 500.0, 'H', '24VDC', 24.0)

    # Set up the mock query chain so each filter_by returns a new mock with the correct first()
    def filter_by_side_effect(**kwargs):
        mock_filter = MagicMock()
        if kwargs.get('material_code') == 'Halar':
            mock_filter.first.return_value = material
        elif kwargs.get('type') == 'Flange' and kwargs.get('rating') == '150#' and kwargs.get('size') == '1"':
            mock_filter.first.return_value = connection
        else:
            mock_filter.first.return_value = None
        return mock_filter

    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter_by.side_effect = filter_by_side_effect

    # Mock product service find_variant
    config_service.product_service.find_variant.return_value = variant

    # Calculate price
    config_service._update_price()

    # Verify complex configuration price
    # Base price: $500.0
    # Material adder: $110.0
    # Connection option: $150.0
    # Extra length (24" - 10" = 14"): 14 * $8.0 = $112.0
    expected_price = 500.0 + 110.0 + 150.0 + (14.0 * 8.0)
    assert config_service.current_config.final_price == expected_price
    assert config_service.current_config.model_number == 'LS2000-24-H-24-F150-1'
