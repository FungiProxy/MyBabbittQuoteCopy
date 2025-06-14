"""
Test suite for QuoteTab pricing functionality.

This module tests the pricing calculations and updates in the QuoteTab UI component.
"""

import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from collections import namedtuple
from PySide6.QtCore import Qt

from src.ui.quote_tab import QuoteTab
from src.core.models import Product, Material, ConnectionOption
from src.core.models.configuration import Configuration

Product = namedtuple("Product", ["id", "name", "base_price", "base_length", "category"])
Variant = namedtuple("Variant", ["model_number", "base_price", "material", "voltage", "length"])
MaterialOption = namedtuple("MaterialOption", ["adder"])
ConnectionOption = namedtuple("ConnectionOption", ["price"])


@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    db = MagicMock()
    return db


@pytest.fixture
def quote_tab(qapp, mock_db):
    """Create a QuoteTab instance for testing."""
    parent = QWidget()
    tab = QuoteTab(parent)
    tab.db = mock_db
    yield tab
    # Clean up
    parent.deleteLater()
    QApplication.processEvents()


def test_update_pricing_base_price(quote_tab, mock_db):
    """Test updating pricing with base price only."""
    # Set up test data
    product_info = {
        "model": "LS2000",
        "application": "Test Application",
        "base_price": 500.0,
    }
    quote_tab.update_product_info(product_info)
    quote_tab.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name="LS2000",
        base_product={
            "id": 1,
            "name": "LS2000",
            "base_price": 500.0,
            "base_length": 10.0,
            "category": "Level Switch"
        },
        selected_options={},
        final_price=500.0,
        final_description="",
        model_number="",
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock product query
    product = Product(1, "LS2000", 500.0, 10.0, "Level Switch")
    mock_db.query().filter().first.return_value = product

    # Update pricing
    quote_tab.update_pricing()

    # Verify price display
    assert quote_tab.base_price_label.text() == "$800.00"
    assert quote_tab.total_price_label.text() == "Total Price: $800.00"


def test_update_pricing_with_length(quote_tab, mock_db):
    """Test updating pricing with length adjustment."""
    # Set up test data
    product_info = {
        "model": "LS2000",
        "application": "Test Application",
        "base_price": 500.0,
    }
    quote_tab.update_product_info(product_info)
    quote_tab.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name="LS2000",
        base_product={
            "id": 1,
            "name": "LS2000",
            "base_price": 500.0,
            "base_length": 10.0,
            "category": "Level Switch"
        },
        selected_options={"Probe Length": 24.0},  # 24 inches
        final_price=612.0,  # Base + length adjustment
        final_description="",
        model_number="",
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock product query
    product = Product(1, "LS2000", 500.0, 10.0, "Level Switch")
    mock_db.query().filter().first.return_value = product

    # Update pricing
    quote_tab.update_pricing()

    # Verify price display
    assert quote_tab.base_price_label.text() == "$800.00"
    assert quote_tab.total_price_label.text() == "Total Price: $912.00"


def test_update_pricing_with_connection(quote_tab, mock_db):
    """Test updating pricing with connection option."""
    # Set up test data
    product_info = {
        "model": "LS2000",
        "application": "Test Application",
        "base_price": 500.0,
    }
    quote_tab.update_product_info(product_info)
    quote_tab.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name="LS2000",
        base_product={
            "id": 1,
            "name": "LS2000",
            "base_price": 500.0,
            "base_length": 10.0,
            "category": "Level Switch"
        },
        selected_options={
            "Connection Type": "Flange",
            "Flange Rating": "150#",
            "Flange Size": "1\""
        },
        final_price=650.0,  # Base + connection
        final_description="",
        model_number="",
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock product query
    product = Product(1, "LS2000", 500.0, 10.0, "Level Switch")
    mock_db.query().filter().first.return_value = product

    # Update pricing
    quote_tab.update_pricing()

    # Verify price display
    assert quote_tab.base_price_label.text() == "$800.00"
    assert quote_tab.total_price_label.text() == "Total Price: $950.00"


def test_update_pricing_with_material(quote_tab, mock_db):
    """Test updating pricing with material option."""
    # Set up test data
    product_info = {
        "model": "LS2000",
        "application": "Test Application",
        "base_price": 500.0,
    }
    quote_tab.update_product_info(product_info)
    quote_tab.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name="LS2000",
        base_product={
            "id": 1,
            "name": "LS2000",
            "base_price": 500.0,
            "base_length": 10.0,
            "category": "Level Switch"
        },
        selected_options={"Material": "Halar"},
        final_price=610.0,  # Base + material
        final_description="",
        model_number="",
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock product query
    product = Product(1, "LS2000", 500.0, 10.0, "Level Switch")
    mock_db.query().filter().first.return_value = product

    # Update pricing
    quote_tab.update_pricing()

    # Verify price display
    assert quote_tab.base_price_label.text() == "$800.00"
    assert quote_tab.total_price_label.text() == "Total Price: $910.00"


def test_update_pricing_with_cable_length(quote_tab, mock_db):
    """Test updating pricing with cable length adjustment."""
    # Set up test data
    product_info = {
        "model": "LS2000",
        "application": "Test Application",
        "base_price": 500.0,
    }
    quote_tab.update_product_info(product_info)
    quote_tab.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name="LS2000",
        base_product={
            "id": 1,
            "name": "LS2000",
            "base_price": 500.0,
            "base_length": 10.0,
            "category": "Level Switch"
        },
        selected_options={"Cable Length": 20.0},  # 20 feet
        final_price=700.0,  # Base + cable length
        final_description="",
        model_number="",
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock product query
    product = Product(1, "LS2000", 500.0, 10.0, "Level Switch")
    mock_db.query().filter().first.return_value = product

    # Update pricing
    quote_tab.update_pricing()

    # Verify price display
    assert quote_tab.base_price_label.text() == "$800.00"
    assert quote_tab.total_price_label.text() == "Total Price: $1000.00"


def test_update_pricing_complex_configuration(quote_tab, mock_db):
    """Test updating pricing for complex configuration."""
    # Set up test data
    product_info = {
        "model": "LS2000",
        "application": "Test Application",
        "base_price": 500.0,
    }
    quote_tab.update_product_info(product_info)
    quote_tab.current_config = Configuration(
        db=mock_db,
        product_family_id=1,
        product_family_name="LS2000",
        base_product={
            "id": 1,
            "name": "LS2000",
            "base_price": 500.0,
            "base_length": 10.0,
            "category": "Level Switch"
        },
        selected_options={
            "Voltage": "24VDC",
            "Material": "Halar",
            "Probe Length": 24.0,
            "Connection Type": "Flange",
            "Flange Rating": "150#",
            "Flange Size": "1\"",
            "Cable Length": 20.0
        },
        final_price=872.0,  # Base + all options
        final_description="",
        model_number="",
        quantity=1,
        is_valid=False,
        validation_errors=[]
    )

    # Mock product query
    product = Product(1, "LS2000", 500.0, 10.0, "Level Switch")
    mock_db.query().filter().first.return_value = product

    # Update pricing
    quote_tab.update_pricing()

    # Verify price display
    assert quote_tab.base_price_label.text() == "$800.00"
    assert quote_tab.total_price_label.text() == "Total Price: $1172.00"


def test_update_items_table_prices(quote_tab):
    """Test price formatting in items table."""
    # Set up test data
    product_info = {
        "model": "LS2000",
        "application": "Test Application",
        "base_price": 500.0,
    }
    quote_tab.update_product_info(product_info)
    quote_tab.items_table.setRowCount(2)
    quote_tab.items_table.setItem(0, 2, QTableWidgetItem("100.00"))
    quote_tab.items_table.setItem(1, 2, QTableWidgetItem("50.50"))

    # Update items table prices
    quote_tab.update_items_table_prices()

    # Verify price formatting
    assert quote_tab.items_table.item(0, 2).text() == "$100.00"
    assert quote_tab.items_table.item(1, 2).text() == "$50.50"


def test_update_total_pricing(quote_tab):
    """Test total price calculation including items."""
    # Set up test data
    product_info = {
        "model": "LS2000",
        "application": "Test Application",
        "base_price": 500.0,
    }
    quote_tab.update_product_info(product_info)
    quote_tab.pricing = {
        "base_price": 500.0,
        "options_price": 100.0,
    }

    # Set up items table
    quote_tab.items_table.setRowCount(2)
    quote_tab.items_table.setItem(0, 3, QTableWidgetItem("$600.00"))
    quote_tab.items_table.setItem(1, 3, QTableWidgetItem("$50.50"))

    # Update total pricing
    quote_tab.update_total_pricing()

    # Verify total price label
    assert quote_tab.total_price_label.text() == "Total Price: $650.50"
