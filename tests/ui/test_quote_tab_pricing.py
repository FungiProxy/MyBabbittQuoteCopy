"""
Test suite for QuoteTab pricing functionality.

This module tests the pricing calculations and updates in the QuoteTab UI component.
"""

import pytest
from unittest.mock import MagicMock, patch
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src.ui.quote_tab import QuoteTab
from src.core.models import Product, Material, ConnectionOption


@pytest.fixture
def app():
    """Create a QApplication instance for testing."""
    return QApplication([])


@pytest.fixture
def quote_tab(app):
    """Create a QuoteTab instance for testing."""
    return QuoteTab()


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock()


def test_update_pricing_base_price(quote_tab, mock_db):
    """Test base price update in QuoteTab."""
    # Set up test data
    quote_tab.specs = {
        "model": "LS2000",
        "voltage": "120V",
        "material": "S",
    }

    # Mock product query
    product = Product(
        id=1,
        model_number="LS2000-120-S",
        base_price=500.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = product

    # Update pricing
    with patch("src.ui.quote_tab.SessionLocal", return_value=mock_db):
        quote_tab.update_pricing()

    # Verify base price
    assert quote_tab.pricing["base_price"] == 500.0
    assert quote_tab.base_price_label.text() == "$500.00"


def test_update_pricing_with_length(quote_tab, mock_db):
    """Test price update with length adjustment."""
    # Set up test data
    quote_tab.specs = {
        "model": "LS2000",
        "voltage": "120V",
        "material": "S",
        "probe_length": 24.0,  # 24 inches
    }

    # Mock product query
    product = Product(
        id=1,
        model_number="LS2000-120-S",
        base_price=500.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = product

    # Update pricing
    with patch("src.ui.quote_tab.SessionLocal", return_value=mock_db):
        quote_tab.update_pricing()

    # Verify price with length adjustment
    # Base price: $500.0
    # Extra length (24" - 10" = 14"): 14 * $8.0 = $112.0
    expected_price = 500.0 + (14.0 * 8.0)
    assert quote_tab.pricing["base_price"] == expected_price
    assert quote_tab.base_price_label.text() == f"${expected_price:,.2f}"


def test_update_pricing_with_connection(quote_tab, mock_db):
    """Test price update with connection option."""
    # Set up test data
    quote_tab.specs = {
        "model": "LS2000",
        "voltage": "120V",
        "material": "S",
        "connection_type": "Flange",
        "flange_rating": "150#",
        "flange_size": '1"',
    }

    # Mock product and connection option queries
    product = Product(
        id=1,
        model_number="LS2000-120-S",
        base_price=500.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    connection_option = ConnectionOption(
        type="Flange",
        rating="150#",
        size='1"',
        price=100.0,
    )
    mock_db.query().filter().first.side_effect = [product, connection_option]

    # Update pricing
    with patch("src.ui.quote_tab.SessionLocal", return_value=mock_db):
        quote_tab.update_pricing()

    # Verify price with connection option
    assert quote_tab.pricing["base_price"] == 500.0
    assert quote_tab.pricing["options_price"] == 100.0
    assert quote_tab.pricing["total_price"] == 600.0
    assert quote_tab.total_price_label.text() == "$600.00"


def test_update_pricing_with_cable_length(quote_tab, mock_db):
    """Test price update with cable length adjustment."""
    # Set up test data
    quote_tab.specs = {
        "model": "LS2000",
        "voltage": "120V",
        "material": "S",
        "cable_length": 20.0,  # 20 feet
    }

    # Mock product query
    product = Product(
        id=1,
        model_number="LS2000-120-S",
        base_price=500.0,
        base_length=10.0,
        material="S",
        voltage="120V",
    )
    mock_db.query().filter().first.return_value = product

    # Update pricing
    with patch("src.ui.quote_tab.SessionLocal", return_value=mock_db):
        quote_tab.update_pricing()

    # Verify price with cable length adjustment
    # Base price: $500.0
    # Extra cable (20' - 10' = 10'): 10 * $5.0 = $50.0
    expected_options_price = (20.0 - 10.0) * 5.0
    assert quote_tab.pricing["base_price"] == 500.0
    assert quote_tab.pricing["options_price"] == expected_options_price
    assert quote_tab.pricing["total_price"] == 500.0 + expected_options_price


def test_update_items_table_prices(quote_tab):
    """Test price formatting in items table."""
    # Set up test data
    quote_tab.items_table.setRowCount(2)

    # Add test items
    for row in range(2):
        quote_tab.items_table.setItem(row, 0, MagicMock())
        quote_tab.items_table.setItem(row, 1, MagicMock())
        quote_tab.items_table.setItem(row, 2, MagicMock())
        quote_tab.items_table.setItem(row, 3, MagicMock())

    # Set test prices
    quote_tab.items_table.item(0, 2).setText("1000.5")
    quote_tab.items_table.item(0, 3).setText("2001")
    quote_tab.items_table.item(1, 2).setText("500.75")
    quote_tab.items_table.item(1, 3).setText("1001.5")

    # Update price formatting
    quote_tab.update_items_table_prices()

    # Verify formatted prices
    assert quote_tab.items_table.item(0, 2).text() == "$1,000.50"
    assert quote_tab.items_table.item(0, 3).text() == "$2,001.00"
    assert quote_tab.items_table.item(1, 2).text() == "$500.75"
    assert quote_tab.items_table.item(1, 3).text() == "$1,001.50"


def test_update_total_pricing(quote_tab):
    """Test total price calculation including items."""
    # Set up test data
    quote_tab.pricing = {
        "base_price": 500.0,
        "options_price": 100.0,
    }

    # Set up items table
    quote_tab.items_table.setRowCount(2)

    # Add test items with quantities and prices
    for row in range(2):
        item_data = {"price": 50.0 * (row + 1)}  # $50 and $100
        item = MagicMock()
        item.data.return_value = item_data

        quote_tab.items_table.setItem(row, 0, item)
        quote_tab.items_table.setItem(row, 1, MagicMock())
        quote_tab.items_table.setItem(row, 2, MagicMock())
        quote_tab.items_table.setItem(row, 3, MagicMock())

    # Set quantities
    quote_tab.items_table.item(0, 1).setText("2")  # 2 units of $50 item
    quote_tab.items_table.item(1, 1).setText("3")  # 3 units of $100 item

    # Update total pricing
    quote_tab.update_total_pricing()

    # Verify total price calculation
    # Base price: $500.0
    # Options price: $100.0
    # Items price: (2 * $50) + (3 * $100) = $400.0
    expected_total = 500.0 + 100.0 + 400.0
    assert quote_tab.pricing["total_price"] == expected_total
    assert quote_tab.total_price_label.text() == f"${expected_total:,.2f}"
