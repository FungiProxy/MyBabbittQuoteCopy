from unittest.mock import MagicMock, patch

import pytest

from src.core.services.configuration_service import ConfigurationService
from src.core.services.product_service import ProductService


@pytest.fixture
def mock_db_session():
    """Fixture for a mocked database session."""
    return MagicMock()


@pytest.fixture
def mock_product_service():
    """Fixture for a mocked product service."""
    return MagicMock(spec=ProductService)


@pytest.fixture
def base_product_info():
    """Provides a sample base product dictionary."""
    return {
        "id": 1,
        "name": "LS2000",
        "base_price": 500.0,
        "base_length": 10.0,
        "category": "Level Switch",
    }


@pytest.fixture
def config_service(mock_db_session, mock_product_service):
    """Fixture for a ConfigurationService instance with mocks."""
    return ConfigurationService(mock_db_session, mock_product_service)


@patch(
    "src.core.services.configuration_service.calculate_product_price",
    return_value=500.0,
)
def test_start_configuration(mock_calculate_price, config_service, base_product_info):
    """Test that a configuration session can be started correctly."""
    config = config_service.start_configuration(
        product_family_id=1,
        product_family_name="LS2000",
        base_product_info=base_product_info,
    )
    assert config is not None
    assert config_service.current_config is not None
    assert config.product_family_name == "LS2000"
    assert config.base_product["base_price"] == 500.0
    mock_calculate_price.assert_called_once()
    assert config.final_price == 500.0


class TestVoltageSelection:
    @patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=550.0,
    )
    def test_select_voltage_updates_configuration(
        self, mock_calculate_price, config_service, base_product_info
    ):
        """Test that selecting a voltage updates the current_config object and price."""
        # Arrange: Start a configuration, which calls the mock once
        with patch(
            "src.core.services.configuration_service.calculate_product_price",
            return_value=500.0,
        ):
            config_service.start_configuration(
                product_family_id=1,
                product_family_name="LS2000",
                base_product_info=base_product_info,
            )

        # Act: Select a voltage
        selected_voltage = "24VDC"
        config_service.select_option("Voltage", selected_voltage)

        # Assert: Check that the configuration was updated
        assert config_service.current_config is not None
        assert "Voltage" in config_service.current_config.selected_options
        assert (
            config_service.current_config.selected_options["Voltage"]
            == selected_voltage
        )

        # Assert that price was recalculated and updated
        mock_calculate_price.assert_called_once()
        assert config_service.current_config.final_price == 550.0


class TestMaterialSelection:
    @patch(
        "src.core.services.configuration_service.calculate_product_price",
        return_value=600.0,
    )
    def test_select_material_updates_configuration(
        self, mock_calculate_price, config_service, base_product_info
    ):
        """Test that selecting a material updates the current_config object and price."""
        # Arrange: Start a configuration
        with patch(
            "src.core.services.configuration_service.calculate_product_price",
            return_value=500.0,
        ):
            config_service.start_configuration(
                product_family_id=1,
                product_family_name="LS2000",
                base_product_info=base_product_info,
            )

        # Act: Select a material
        selected_material = "Halar"
        config_service.select_option("Material", selected_material)

        # Assert: Check that the configuration was updated
        assert config_service.current_config is not None
        assert "Material" in config_service.current_config.selected_options
        assert (
            config_service.current_config.selected_options["Material"]
            == selected_material
        )

        # Assert that price was recalculated and updated
        mock_calculate_price.assert_called_once()
        assert config_service.current_config.final_price == 600.0
