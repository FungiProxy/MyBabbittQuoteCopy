from unittest.mock import MagicMock, patch

import pytest

from src.core.models.configuration import Configuration
from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService


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
    """Create base product info for testing."""
    return {
        "id": 1,
        "name": "LS2000",
        "base_price": 500.0,
        "base_length": 10.0,
        "category": "Level Switch",
    }


@patch(
    "src.core.services.configuration_service.calculate_product_price",
    return_value=500.0,
)
def test_start_configuration(
    mock_calculate_price, config_service, base_product_info, mock_db
):
    """Test starting a new configuration."""
    # Mock the product_service.find_variant to return a variant with base_price=500.0
    variant = MagicMock()
    variant.base_price = 500.0
    variant.model_number = "LS2000-120-S"
    config_service.product_service.find_variant.return_value = variant

    # Start configuration
    config_service.start_configuration(
        product_family_id=1,
        product_family_name="LS2000",
        base_product_info=base_product_info,
    )

    # Verify configuration was created correctly
    assert config_service.current_config.product_family_id == 1
    assert config_service.current_config.product_family_name == "LS2000"
    assert config_service.current_config.base_product == base_product_info
    assert config_service.current_config.selected_options == {}
    assert config_service.current_config.final_price == 500.0
    assert config_service.current_config.final_description == ""
    assert config_service.current_config.model_number == "LS2000-120-S"
    assert config_service.current_config.quantity == 1
    assert not config_service.current_config.is_valid
    assert config_service.current_config.validation_errors == []


class TestVoltageSelection:
    @patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=550.0,
    )
    def test_select_voltage_updates_configuration(
        self, mock_calculate_price, config_service, base_product_info, mock_db
    ):
        """Test selecting voltage updates configuration."""
        # Set up test data
        config_service.current_config = Configuration(
            db=mock_db,
            product_family_id=1,
            product_family_name="LS2000",
            base_product=base_product_info,
            selected_options={},
            final_price=0.0,
            final_description="",
            model_number="",
            quantity=1,
            is_valid=False,
            validation_errors=[],
        )

        # Mock variant
        variant = MagicMock()
        variant.model_number = "LS2000-120-S"
        variant.base_price = 500.0
        variant.material = "S"
        variant.voltage = "120V"
        variant.length = 10.0
        config_service.product_service.find_variant.return_value = variant

        # Mock VoltageOption query to return a real price_multiplier
        voltage_option = MagicMock()
        voltage_option.price_multiplier = 1.1  # 10% increase

        def query_filter_by(**kwargs):
            return MagicMock(first=MagicMock(return_value=voltage_option))

        mock_db.query.return_value.filter_by = query_filter_by

        # Select voltage using select_option
        config_service.select_option("Voltage", "120V")

        # Verify configuration was updated
        assert config_service.current_config.selected_options["Voltage"] == "120V"
        assert config_service.current_config.final_price == 550.0
        assert config_service.current_config.model_number == "LS2000-120-S"


class TestMaterialSelection:
    @patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=600.0,
    )
    def test_select_material_updates_configuration(
        self, mock_calculate_price, config_service, base_product_info, mock_db
    ):
        """Test selecting material updates configuration."""
        # Set up test data
        config_service.current_config = Configuration(
            db=mock_db,
            product_family_id=1,
            product_family_name="LS2000",
            base_product=base_product_info,
            selected_options={},
            final_price=0.0,
            final_description="",
            model_number="",
            quantity=1,
            is_valid=False,
            validation_errors=[],
        )

        # Mock variant
        variant = MagicMock()
        variant.model_number = "LS2000-120-H"
        variant.base_price = 500.0
        variant.material = "H"
        variant.voltage = "120V"
        variant.length = 10.0
        config_service.product_service.find_variant.return_value = variant

        # Mock MaterialOption query to return a real adder
        material_option = MagicMock()
        material_option.adder = 100.0  # $100 adder

        def query_filter_by(**kwargs):
            return MagicMock(first=MagicMock(return_value=material_option))

        mock_db.query.return_value.filter_by = query_filter_by

        # Select material using select_option
        config_service.select_option("Material", "Halar")

        # Verify configuration was updated
        assert config_service.current_config.selected_options["Material"] == "Halar"
        assert config_service.current_config.final_price == 600.0
        assert config_service.current_config.model_number == "LS2000-120-H"
